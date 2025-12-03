"""Entry point for the calendar scenario generation CLI.

Run with: python -m calendar_generator
"""

import asyncio

from .cli import main

asyncio.run(main())
