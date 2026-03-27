from typing import TypedDict

from sage_benchmark.calendar_scheduling.experiments import ExperimentConfig


def experiment_baseline():
    for prompt in ("default", "privacy-ci"):
        yield ExperimentConfig(
            paths=["data/calendar-scheduling/final/small.yaml"],
            model="trapi/gpt-4.1",
            assistant_system_prompt=prompt,
            expose_preferences=False,
            explicit_cot=False,
            variant=f"baseline-{prompt}",
        )


def experiment_whimsical():
    for prompt in ("default", "privacy-ci"):
        for i in range(5):
            yield ExperimentConfig(
                paths=[
                    f"data/calendar-scheduling/final/small-malicious-whimsical-privacy-{i + 1}.yaml"
                ],
                model="trapi/gpt-4.1",
                assistant_system_prompt=prompt,
                expose_preferences=False,
                explicit_cot=False,
                variant=f"whimsical-{prompt}-{i}",
            )
