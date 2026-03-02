"""Annotation server for calendar event privacy labels."""

import json
import os
from itertools import combinations
from pathlib import Path

import yaml
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

DATA_DIR = Path(__file__).parent.parent / "data" / "calendar-scheduling" / "final"
ANNOTATIONS_DIR = Path(__file__).parent / "annotations"
ANNOTATIONS_DIR.mkdir(exist_ok=True)

_task_cache: dict[str, list] = {}


def load_tasks(dataset: str = "small") -> list[dict]:
    if dataset in _task_cache:
        return _task_cache[dataset]
    path = DATA_DIR / f"{dataset}.yaml"
    if not path.exists():
        raise HTTPException(404, f"Dataset {dataset} not found")
    with open(path) as f:
        data = yaml.safe_load(f)
    _task_cache[dataset] = data["tasks"]
    return data["tasks"]


def annotations_path(annotator: str, dataset: str = "small") -> Path:
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in annotator)
    return ANNOTATIONS_DIR / f"{safe}_{dataset}.json"


def load_annotations(annotator: str, dataset: str = "small") -> dict:
    path = annotations_path(annotator, dataset)
    if path.exists():
        return json.loads(path.read_text())
    return {}


def save_annotations(annotator: str, data: dict, dataset: str = "small"):
    path = annotations_path(annotator, dataset)
    path.write_text(json.dumps(data, indent=2))


# --- API ---


class AnnotationPayload(BaseModel):
    task_id: int
    event_uid: str
    is_secret: bool


class BulkAnnotationPayload(BaseModel):
    task_id: int
    annotations: dict[str, bool]  # event_uid -> is_secret


@app.get("/api/datasets")
def list_datasets():
    files = sorted(DATA_DIR.glob("*.yaml"))
    return [f.stem for f in files]


@app.get("/api/annotators")
def list_annotators():
    names = set()
    for path in ANNOTATIONS_DIR.glob("*.json"):
        # filename is {name}_{dataset}.json
        name = path.stem.rsplit("_", 1)[0]
        if name:
            names.add(name)
    return sorted(names)


@app.get("/api/tasks")
def get_tasks(dataset: str = "small"):
    tasks = load_tasks(dataset)
    summaries = []
    for t in tasks:
        events = t["assistant"]["calendar"]
        summaries.append(
            {
                "id": t["id"],
                "requestor_email": t["requestor"]["email"],
                "assistant_email": t["assistant"]["email"],
                "event_count": len(events),
                "secret_count": sum(1 for e in events if e.get("is_secret")),
            }
        )
    return summaries


@app.get("/api/tasks/{task_id}")
def get_task(task_id: int, dataset: str = "small"):
    tasks = load_tasks(dataset)
    for t in tasks:
        if t["id"] == task_id:
            return t
    raise HTTPException(404, "Task not found")


@app.post("/api/register/{annotator}")
def register_annotator(annotator: str, dataset: str = "small"):
    path = annotations_path(annotator, dataset)
    if not path.exists():
        path.write_text("{}")
    return {"ok": True}


@app.get("/api/annotations/{annotator}")
def get_annotations(annotator: str, dataset: str = "small"):
    return load_annotations(annotator, dataset)


@app.post("/api/annotations/{annotator}")
def save_annotation(annotator: str, payload: AnnotationPayload, dataset: str = "small"):
    data = load_annotations(annotator, dataset)
    task_key = str(payload.task_id)
    if task_key not in data:
        data[task_key] = {}
    data[task_key][payload.event_uid] = payload.is_secret
    save_annotations(annotator, data, dataset)
    return {"ok": True}


@app.post("/api/annotations/{annotator}/bulk")
def save_bulk_annotations(annotator: str, payload: BulkAnnotationPayload, dataset: str = "small"):
    data = load_annotations(annotator, dataset)
    task_key = str(payload.task_id)
    if task_key not in data:
        data[task_key] = {}
    data[task_key].update(payload.annotations)
    save_annotations(annotator, data, dataset)
    return {"ok": True}


def agreement_score(labels: list[bool]) -> float | None:
    if len(labels) < 2:
        return None
    total = 0
    agreeing = 0
    for a, b in combinations(labels, 2):
        total += 1
        if a == b:
            agreeing += 1
    return agreeing / total


def fleiss_kappa(matrix: list[list[int]]) -> float | None:
    if not matrix:
        return None
    n = sum(matrix[0])
    if n < 2:
        return None
    N = len(matrix)
    k = len(matrix[0])
    p = [sum(matrix[i][j] for i in range(N)) / (N * n) for j in range(k)]
    P = []
    for i in range(N):
        Pi = (sum(matrix[i][j] ** 2 for j in range(k)) - n) / (n * (n - 1))
        P.append(Pi)
    P_bar = sum(P) / N
    P_e = sum(p_j**2 for p_j in p)
    if P_e == 1:
        return 1.0
    return (P_bar - P_e) / (1 - P_e)


@app.get("/api/summary")
def get_summary(dataset: str = "small"):
    tasks = load_tasks(dataset)
    all_annotations: dict[str, dict] = {}
    for path in ANNOTATIONS_DIR.glob(f"*_{dataset}.json"):
        annotator = path.stem.rsplit(f"_{dataset}", 1)[0]
        all_annotations[annotator] = json.loads(path.read_text())

    all_labels_for_fleiss: list[list[bool]] = []
    summary = []
    for t in tasks:
        task_id = str(t["id"])
        events = t["assistant"]["calendar"]
        event_summaries = []
        for e in events:
            uid = e["uid"]
            votes = {}
            for annotator, ann in all_annotations.items():
                if task_id in ann and uid in ann[task_id]:
                    votes[annotator] = ann[task_id][uid]
            labels = list(votes.values())
            score = agreement_score(labels) if len(labels) >= 2 else None
            event_summaries.append(
                {
                    "uid": uid,
                    "title": e["title"],
                    "ground_truth": e.get("is_secret", False),
                    "votes": votes,
                    "agreement_score": score,
                }
            )
            if len(labels) >= 2:
                all_labels_for_fleiss.append(labels)
        summary.append(
            {
                "task_id": int(task_id),
                "requestor_email": t["requestor"]["email"],
                "assistant_email": t["assistant"]["email"],
                "events": event_summaries,
            }
        )

    # Compute Fleiss' kappa across items with the same number of raters
    kappa = None
    if all_labels_for_fleiss:
        # Group by rater count; use the largest group
        from collections import Counter

        counts = Counter(len(l) for l in all_labels_for_fleiss)
        most_common_n = counts.most_common(1)[0][0]
        subset = [l for l in all_labels_for_fleiss if len(l) == most_common_n]
        matrix = [
            [sum(1 for x in labels if not x), sum(1 for x in labels if x)] for labels in subset
        ]
        kappa = fleiss_kappa(matrix)

    return {
        "annotators": list(all_annotations.keys()),
        "tasks": summary,
        "fleiss_kappa": round(kappa, 4) if kappa is not None else None,
    }


@app.get("/api/progress/{annotator}")
def get_progress(annotator: str, dataset: str = "small"):
    tasks = load_tasks(dataset)
    ann = load_annotations(annotator, dataset)
    completed = 0
    total = len(tasks)
    for t in tasks:
        task_key = str(t["id"])
        events = t["assistant"]["calendar"]
        if task_key in ann and len(ann[task_key]) == len(events):
            completed += 1
    return {"completed": completed, "total": total}


# --- Static files ---

STATIC_DIR = Path(__file__).parent / "static"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
@app.get("/annotate")
@app.get("/summary")
def serve_index():
    return FileResponse(str(STATIC_DIR / "index.html"))
