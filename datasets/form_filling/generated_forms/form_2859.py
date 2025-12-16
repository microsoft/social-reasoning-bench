from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicationInformation(BaseModel):
    """Application identifier and basic request details"""

    app_number: str = Field(
        ...,
        description=(
            "Application number assigned to this use permit request .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class IProposedUsePermitRequest(BaseModel):
    """Detailed description of the proposed use permit and parking district status"""

    proposed_use_permit_request_state_in_detail: str = Field(
        ...,
        description=(
            "Detailed description of the proposed use permit request .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    parking_district_checkbox: BooleanLike = Field(
        default="",
        description=(
            "Select if the subject property is located within the City of Pacific Grove "
            "Parking District"
        ),
    )


class IIOperationalDetails(BaseModel):
    """Operational characteristics related to the proposed use"""

    days_hours_of_operation: str = Field(
        default="",
        description=(
            "List the days of the week and hours during which the use will operate .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    number_of_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of employees associated with the proposed use"
    )

    what_if_any_retail_services_will_be_provided: str = Field(
        default="",
        description=(
            "Describe any retail services that will be offered, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    describe_any_other_pertinent_details: str = Field(
        default="",
        description=(
            "Provide any additional relevant information about the proposed use .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PacificGrovePlanningUsePermitRequest(BaseModel):
    """
        CITY OF PACIFIC GROVE
    Community Development Department   Planning Division
    Permit & Request Application
    for Use Permit (UP)

        Permit & Request Application for Use Permit (UP)
    """

    application_information: ApplicationInformation = Field(
        ..., description="Application Information"
    )
    i_proposed_use_permit_request: IProposedUsePermitRequest = Field(
        ..., description="I. Proposed Use Permit Request"
    )
    ii_operational_details: IIOperationalDetails = Field(..., description="II. Operational Details")
