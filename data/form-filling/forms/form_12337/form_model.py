from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProfitableCourseIdea(BaseModel):
    """
    PROFITABLE COURSE IDEA

    The worksheet is from the free Teachable course profitablecourseidea.com
    """

    pain: str = Field(
        ...,
        description=(
            "Copy-paste exact statements from your target or community audience about their "
            'pain, hopes, and fears on this topic. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    offer: str = Field(
        ...,
        description=(
            "Describe the offer(s) you can stack to solve the painful challenge, including "
            "any content, resources, or websites you can provide and the financial value of "
            'each offering. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    outline: str = Field(
        ...,
        description=(
            "Create a descriptive course name that explains the painful problem and how you "
            "solve it, then list 3–8 modules and a section labeled as your course sales "
            'page. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )
