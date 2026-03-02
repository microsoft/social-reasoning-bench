# Calendar Privacy Annotation Tool

A web UI for auditing `is_secret` labels on calendar events.

## Setup

```bash
# From repo root
uv pip install fastapi uvicorn pyyaml

# Run the server
cd annotation
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

Then open http://localhost:8000.

## Usage

1. **Sign in** — Enter your name on the landing page. This creates a personal annotation file.
2. **Annotate** — For each task, review events and mark them as Secret or Public.
   - Keyboard shortcuts: `↑↓` navigate events, `S` = secret, `P` = public, `←→` = prev/next task, `A` = agree all with ground truth.
3. **Summary** — View agreement across annotators at `/summary`.

## Annotation Storage

Annotations are saved as JSON files in `annotation/annotations/`, one per annotator per dataset (e.g., `alice_small.json`). Signing back in with the same name resumes where you left off.

## Deploying to Lab Server

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

Share the URL with your team. Each person enters their name and gets their own annotation file.
