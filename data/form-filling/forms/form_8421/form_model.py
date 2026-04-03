from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
    """Basic information about the member requesting a loan"""

    name: str = Field(
        ...,
        description=(
            'Applicant\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date_of_request: str = Field(
        ..., description="Date this application is being submitted"
    )  # YYYY-MM-DD format

    address: str = Field(
        ...,
        description=(
            'Applicant\'s mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    home_phone: str = Field(
        ...,
        description=(
            'Applicant\'s home phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    school_phone: str = Field(
        default="",
        description=(
            "Applicant's school or work phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    school_dept: str = Field(
        ...,
        description=(
            "Name of the school or department where the applicant works .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    position: str = Field(
        ...,
        description=(
            'Applicant\'s job title or position .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    amount_requested: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Dollar amount of the loan requested (up to $1,000)"
    )


class ReasonforRequest(BaseModel):
    """Details about the financial need and extenuating circumstances"""

    coronavirus_pandemic_extenuating_circumstances: str = Field(
        ...,
        description=(
            "Detailed description of how the coronavirus pandemic has specifically caused "
            'the applicant\'s financial need .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    other_reason_for_request_extenuating_circumstances: str = Field(
        default="",
        description=(
            "Detailed description of any other extenuating circumstances causing financial "
            'need .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class ApplicantAuthorization(BaseModel):
    """Applicant signature and date confirming the request"""

    signature: str = Field(
        ...,
        description=(
            "Applicant's signature agreeing to the terms of the Solidarity Fund loan .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date: str = Field(..., description="Date the application is signed")  # YYYY-MM-DD format


class ForSolidarityFundCommitteeUseOnly(BaseModel):
    """Committee review and decision information"""

    request_approved: BooleanLike = Field(
        default="", description="Indicates whether the committee approved the request"
    )

    request_denied: BooleanLike = Field(
        default="", description="Indicates whether the committee denied the request"
    )

    mti_member: BooleanLike = Field(
        ..., description="Indicates whether the applicant is a member of MTI"
    )

    outstanding_balance: Literal["Y", "N", "N/A", ""] = Field(
        default="",
        description="Indicates whether the applicant currently has an outstanding loan balance",
    )

    request_approved_for_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount of the loan approved by the committee"
    )


class SolidarityFundApplication(BaseModel):
    """
    Solidarity Fund Application

    MTI has taken immediate action to deploy union resources to provide financial support to members impacted by the pandemic. Commencing immediately, the MTI Solidarity Fund is available to provide no interest loans of up to $1,000 for MTI members who suffer a financial impact due to the pandemic.
    MTI’s Solidarity Fund is made up of donated contributions from Union members to assist Union brothers and sisters in need. No interest is charged. To assure that the Union has funds to assist other MTI members in need, it is required that one receiving a loan from the MTI Solidarity Fund sign an agreement to repay, via payroll deduction, the borrowed amount in equal deductions over thirty (30) months or less. Deductions will begin six (6) months after receipt of the loan.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    reason_for_request: ReasonforRequest = Field(..., description="Reason for Request")
    applicant_authorization: ApplicantAuthorization = Field(
        ..., description="Applicant Authorization"
    )
    for_solidarity_fund_committee_use_only: ForSolidarityFundCommitteeUseOnly = Field(
        ..., description="For Solidarity Fund Committee Use Only"
    )
