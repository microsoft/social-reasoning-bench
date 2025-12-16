from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FaxCoverInformation(BaseModel):
    """Header information for the fax transmission"""

    to: str = Field(
        ...,
        description=(
            "Recipient name or department to whom this fax is being sent .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    from_: str = Field(
        ...,
        description=(
            'Name or department sending this fax .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    pages: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of pages being faxed, including cover sheet"
    )

    phone: str = Field(
        ...,
        description=(
            'Contact phone number for the sender .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date this form or fax is being sent")  # YYYY-MM-DD format

    cc: str = Field(
        default="",
        description=(
            "Names or departments to receive a copy of this fax .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class MemberInformation(BaseModel):
    """Identifying information about the member"""

    first_name: str = Field(
        ...,
        description=(
            'Member\'s first name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            'Member\'s last name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    member_id: str = Field(
        ...,
        description=(
            "Health plan member identification number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dob: str = Field(..., description="Member's date of birth")  # YYYY-MM-DD format


class LabDataClinicalOutcomes(BaseModel):
    """Requested clinical measurements with dates and outcomes"""

    last_pcp_appointment_date: str = Field(
        default="", description="Date of the member's last primary care provider appointment"
    )  # YYYY-MM-DD format

    last_pcp_appointment_outcome: str = Field(
        default="",
        description=(
            "Outcome or key findings from the last primary care provider appointment .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    height_inches_date: str = Field(
        default="", description="Date the member's height was measured"
    )  # YYYY-MM-DD format

    height_inches_outcome: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Member's height in inches"
    )

    weight_lbs_date: str = Field(
        default="", description="Date the member's weight was measured"
    )  # YYYY-MM-DD format

    weight_lbs_outcome: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Member's weight in pounds"
    )

    bmi_date: str = Field(
        default="", description="Date the member's BMI was calculated"
    )  # YYYY-MM-DD format

    bmi_outcome: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Member's body mass index (BMI) value"
    )

    blood_pressure_date: str = Field(
        default="", description="Date the member's blood pressure was measured"
    )  # YYYY-MM-DD format

    blood_pressure_outcome: str = Field(
        default="",
        description=(
            "Member's blood pressure reading (e.g., systolic/diastolic) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    total_cholesterol_date: str = Field(
        default="", description="Date the member's total cholesterol was measured"
    )  # YYYY-MM-DD format

    total_cholesterol_outcome: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Member's total cholesterol level"
    )

    fasting_blood_glucose_date: str = Field(
        default="", description="Date the member's fasting blood glucose was measured"
    )  # YYYY-MM-DD format

    fasting_blood_glucose_outcome: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Member's fasting blood glucose level"
    )


class ProviderComments(BaseModel):
    """Optional comments from the provider"""

    provider_comments: str = Field(
        default="",
        description=(
            "Optional comments or additional information from the provider .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class WeightWatchersOutcomeForm(BaseModel):
    """
    Weight Watchers® Outcome Form

    PLEASE NOTE: At the time of enrollment, all HMO members sign a release of information form to grant the HMO access to their health care information.
    """

    fax_cover_information: FaxCoverInformation = Field(..., description="Fax Cover Information")
    member_information: MemberInformation = Field(..., description="Member Information")
    lab_data__clinical_outcomes: LabDataClinicalOutcomes = Field(
        ..., description="Lab Data / Clinical Outcomes"
    )
    provider_comments: ProviderComments = Field(..., description="Provider Comments")
