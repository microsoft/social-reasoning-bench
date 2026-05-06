import logging

from claim1 import main as claim1
from claim3 import main as claim3
from claim4 import main as claim4
from claim5 import main as claim5

logger = logging.getLogger()

for i, claim in enumerate([claim1, claim3, claim4, claim5]):
    try:
        claim()
    except Exception:
        logger.exception(f"Failed to plot claim {claim.__name__}")
