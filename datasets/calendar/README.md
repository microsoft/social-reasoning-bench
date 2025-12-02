# CalendarScheduling Dataset

A benchmark for evaluating whether LLM agents leak sensitive information in calendar scheduling scenarios.

## Overview

CalendarScheduling contains 190 synthetic datapoints. 

**Key insight**: Though seemingly straightforward, models are actually terrible at protecting clients' private information.


Load programmatically:

```python
import json

with open("datasets/calendar/calendar_scheduling_data.json") as f:
    dataset = json.load(f)
```
