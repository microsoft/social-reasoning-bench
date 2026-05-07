from dataclasses import dataclass
from enum import Enum


class RequestorType(str, Enum):
    EXTERNAL = "external"
    INTERNAL = "internal"


@dataclass(frozen=True)
class Archetype:
    id: int
    name: str
    requestor_type: RequestorType
    description: str
    relationship: str


ARCHETYPES: list[Archetype] = [
    Archetype(
        id=1,
        name="unknown_external",
        requestor_type=RequestorType.EXTERNAL,
        description="Unknown person reaching out cold (recruiter, sales rep, stranger)",
        relationship="cold outreach — no prior relationship",
    ),
    Archetype(
        id=2,
        name="known_vendor",
        requestor_type=RequestorType.EXTERNAL,
        description="Known vendor or partner the company already works with",
        relationship="vendor/partner",
    ),
    Archetype(
        id=3,
        name="client",
        requestor_type=RequestorType.EXTERNAL,
        description="Client or customer of the company",
        relationship="client",
    ),
    Archetype(
        id=4,
        name="boss",
        requestor_type=RequestorType.INTERNAL,
        description="The employee's direct manager or someone more senior in their chain",
        relationship="manager",
    ),
    Archetype(
        id=5,
        name="peer_same_dept",
        requestor_type=RequestorType.INTERNAL,
        description="A peer colleague from the same department",
        relationship="coworker (same department)",
    ),
    Archetype(
        id=6,
        name="peer_diff_dept",
        requestor_type=RequestorType.INTERNAL,
        description="A peer colleague from a different department",
        relationship="coworker (different department)",
    ),
    Archetype(
        id=7,
        name="direct_report",
        requestor_type=RequestorType.INTERNAL,
        description="Someone the employee manages or who is junior to them",
        relationship="direct report",
    ),
]

NUM_ARCHETYPES = len(ARCHETYPES)

SENIORITY_RANK = {
    "junior": 0,
    "mid": 1,
    "senior": 2,
    "lead": 3,
    "director": 4,
    "vp": 5,
    "c-suite": 6,
}
