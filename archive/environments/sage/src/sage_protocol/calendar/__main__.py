"""Entry point for the Calendar marketplace CLI.

Run with: python -m mm_environments.calendar
"""

import asyncio

from .cli import main

asyncio.run(main())
