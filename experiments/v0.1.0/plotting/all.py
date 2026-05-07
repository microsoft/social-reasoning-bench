import logging

from finding1 import main as finding1
from finding3 import main as finding3
from finding4 import main as finding4
from finding5 import main as finding5

logger = logging.getLogger()

if __name__ == "__main__":
    for i, finding in enumerate([finding1, finding3, finding4, finding5]):
        try:
            finding()
        except Exception:
            logger.exception(f"Failed to plot finding {finding.__name__}")
