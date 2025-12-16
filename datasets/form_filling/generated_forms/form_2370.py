from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RelationshipRow(BaseModel):
    """Single row in Relationship"""

    relationship: str = Field(default="", description="Relationship")
    name_and_state_if_alive_or_deceased: str = Field(
        default="", description="Name_And_State_If_Alive_Or_Deceased"
    )
    age: str = Field(default="", description="Age")


class PersonalDetails(BaseModel):
    """Marital status and effective date"""

    status: Literal["Single", "Married", "Civil Partnership", "Widowed", "Divorced", "N/A", ""] = (
        Field(..., description="Current marital or partnership status")
    )

    effective_date: str = Field(
        ..., description="Date from which the stated status applies"
    )  # YYYY-MM-DD format

    single: BooleanLike = Field(default="", description="Tick if your current status is Single")

    married: BooleanLike = Field(default="", description="Tick if your current status is Married")

    civil_partnership: BooleanLike = Field(
        default="", description="Tick if your current status is in a Civil Partnership"
    )

    widowed: BooleanLike = Field(default="", description="Tick if your current status is Widowed")

    divorced: BooleanLike = Field(default="", description="Tick if your current status is Divorced")


class Children(BaseModel):
    """Information about any children, including names and ages"""

    do_you_have_children_yes: BooleanLike = Field(
        default="", description="Select Yes if you have children"
    )

    do_you_have_children_no: BooleanLike = Field(
        default="", description="Select No if you do not have children"
    )

    children_names_and_ages_line_1: str = Field(
        default="",
        description=(
            "First line to list children’s names and ages .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    children_names_and_ages_line_2: str = Field(
        default="",
        description=(
            "Second line to list additional children’s names and ages .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class FamilyBackground(BaseModel):
    """Details of close family members and their status"""

    relationship: List[RelationshipRow] = Field(
        default="",
        description="Table to record family members, whether alive or deceased, and their ages",
    )  # List of table rows

    name_and_state_if_alive_or_deceased: str = Field(
        default="",
        description=(
            "Name of the relative and whether they are alive or deceased .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    age: Union[float, Literal["N/A", ""]] = Field(default="", description="Age of the relative")

    father_name_and_state_if_alive_or_deceased: str = Field(
        default="",
        description=(
            "Father’s name and whether he is alive or deceased .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    father_age: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Father’s age (or age at death)"
    )

    mother_name_and_state_if_alive_or_deceased: str = Field(
        default="",
        description=(
            "Mother’s name and whether she is alive or deceased .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mother_age: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Mother’s age (or age at death)"
    )

    brother_name_and_state_if_alive_or_deceased: str = Field(
        default="",
        description=(
            "Brother’s name and whether he is alive or deceased .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    brother_age: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Brother’s age (or age at death)"
    )

    sister_name_and_state_if_alive_or_deceased: str = Field(
        default="",
        description=(
            "Sister’s name and whether she is alive or deceased .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    sister_age: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Sister’s age (or age at death)"
    )


class MordenCollegeInterestingPeopleLivingLifeToTheFull(BaseModel):
    """
        MORDEN COLLEGE
    Interesting People Living Life to the Full

        ''
    """

    personal_details: PersonalDetails = Field(..., description="Personal Details")
    children: Children = Field(..., description="Children")
    family_background: FamilyBackground = Field(..., description="Family Background")
