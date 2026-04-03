from pydantic import BaseModel, ConfigDict, Field


class AndForm(BaseModel):
    """and"""

    model_config = ConfigDict(extra="forbid")