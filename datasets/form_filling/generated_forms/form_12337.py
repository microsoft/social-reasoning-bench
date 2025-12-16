from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PainRow(BaseModel):
    """Single row in Pain"""

    pain: str = Field(default="", description="Pain")
    offer: str = Field(default="", description="Offer")
    outline: str = Field(default="", description="Outline")


class OfferRow(BaseModel):
    """Single row in Offer"""

    pain: str = Field(default="", description="Pain")
    offer: str = Field(default="", description="Offer")
    outline: str = Field(default="", description="Outline")


class OutlineRow(BaseModel):
    """Single row in Outline"""

    pain: str = Field(default="", description="Pain")
    offer: str = Field(default="", description="Offer")
    outline: str = Field(default="", description="Outline")


class CourseOfferWorksheet(BaseModel):
    """
    Course Offer Worksheet

    Course Offer Worksheet from the free Teachable course profitablecourseidea.com. Use this worksheet to develop a profitable course idea by: (1) capturing exact pain, hopes, and fears expressed by your target or community audience about your topic; (2) defining and “stacking” offers, including content, resources, and websites you can provide to solve this painful challenge and estimating the financial value of each offering; and (3) creating a descriptive course name that explains the painful problem and your solution, outlining 3–8 modules, and drafting a “course page” that serves as your course sales page.
    """

    pain: List[PainRow] = Field(
        default="",
        description=(
            "Table column to capture exact statements from your target audience about their "
            "pains, hopes, and fears related to your topic."
        ),
    )  # List of table rows

    offer: List[OfferRow] = Field(
        default="",
        description=(
            "Table column to describe the offers you can stack to solve the identified "
            "pain, including content, resources, and estimated financial value."
        ),
    )  # List of table rows

    outline: List[OutlineRow] = Field(
        default="",
        description=(
            "Table column to outline the course: name, 3–8 modules, and a section labeled "
            "as the course sales page."
        ),
    )  # List of table rows
