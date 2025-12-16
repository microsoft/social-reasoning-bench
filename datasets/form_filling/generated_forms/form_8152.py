from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class GeneralFarmQuestions(BaseModel):
    """Basic information about the farm and its operations"""

    certified_sc_grown_yes: BooleanLike = Field(
        default="",
        description=(
            "Check if you are a member of the SC Department of Agriculture’s Certified SC "
            "Grown program."
        ),
    )

    certified_sc_grown_no: BooleanLike = Field(
        default="",
        description=(
            "Check if you are not a member of the SC Department of Agriculture’s Certified "
            "SC Grown program."
        ),
    )

    how_large_is_your_farm_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total size of your farm in acres."
    )

    farm_location_urban: BooleanLike = Field(
        default="", description="Check if your farm is located in an urban area."
    )

    farm_location_suburban: BooleanLike = Field(
        default="", description="Check if your farm is located in a suburban area."
    )

    farm_location_rural: BooleanLike = Field(
        default="", description="Check if your farm is located in a rural area."
    )

    owner_other_job_yes: BooleanLike = Field(
        default="", description="Check if the farm owner currently holds another job."
    )

    owner_other_job_no: BooleanLike = Field(
        default="", description="Check if the farm owner does not currently hold another job."
    )

    methods_of_sale_on_farm: BooleanLike = Field(
        default="", description="Check if you sell products on the farm."
    )

    methods_of_sale_u_pick: BooleanLike = Field(
        default="", description="Check if you offer U-pick sales."
    )

    methods_of_sale_farmers_markets: BooleanLike = Field(
        default="", description="Check if you sell products at farmers markets."
    )

    methods_of_sale_online: BooleanLike = Field(
        default="", description="Check if you sell products online."
    )

    methods_of_sale_wholesale: BooleanLike = Field(
        default="", description="Check if you sell products wholesale."
    )

    farm_certified_organic_yes: BooleanLike = Field(
        default="", description="Check if your farm is certified organic."
    )

    farm_certified_organic_no: BooleanLike = Field(
        default="", description="Check if your farm is not certified organic."
    )

    use_organic_practices_yes: BooleanLike = Field(
        default="", description="Check if you use organic farming practices."
    )

    use_organic_practices_no: BooleanLike = Field(
        default="", description="Check if you do not use organic farming practices."
    )

    type_of_farming_line_1: str = Field(
        default="",
        description=(
            "Describe the types of farming you are involved in (first line). .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    type_of_farming_line_2: str = Field(
        default="",
        description=(
            "Describe the types of farming you are involved in (second line). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    type_of_farming_line_3: str = Field(
        default="",
        description=(
            "Describe the types of farming you are involved in (third line). .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class AgritourismProfile(BaseModel):
    """Information about agritourism activities, visitors, and events"""

    yearly_visitors: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Approximate number of visitors to your farm per year."
    )

    open_for_business_line_1: str = Field(
        default="",
        description=(
            "List dates and times when your farm is open for business (first line). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    open_for_business_line_2: str = Field(
        default="",
        description=(
            "List dates and times when your farm is open for business (second line). .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    open_for_business_line_3: str = Field(
        default="",
        description=(
            "List dates and times when your farm is open for business (third line). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    special_events_line_1: str = Field(
        default="",
        description=(
            "List special events and their dates/times (first line). .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    special_events_line_2: str = Field(
        default="",
        description=(
            "List special events and their dates/times (second line). .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    special_events_line_3: str = Field(
        default="",
        description=(
            "List special events and their dates/times (third line). .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ScAgritourismFarmProfile(BaseModel):
    """SC Agritourism Farm Profile"""

    general_farm_questions: GeneralFarmQuestions = Field(..., description="General Farm Questions")
    agritourism_profile: AgritourismProfile = Field(..., description="Agritourism Profile")
