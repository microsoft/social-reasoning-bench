from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
    """Basic information about the scholarship applicant"""

    name: str = Field(
        ...,
        description=(
            'Applicant\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    phone_number: str = Field(
        ...,
        description=(
            "Primary phone number where you can be reached .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Street address, including apartment or unit number if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    city_state_zip: str = Field(
        ...,
        description=(
            "City, state, and ZIP code for your mailing address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    race_ethnicity_optional: str = Field(
        default="",
        description=(
            "Race or ethnicity (optional demographic information) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    gender_optional_male: BooleanLike = Field(
        default="", description="Check if your gender identity is male (optional)"
    )

    gender_optional_female: BooleanLike = Field(
        default="", description="Check if your gender identity is female (optional)"
    )

    email: str = Field(
        ...,
        description=(
            "Email address for contact regarding your application .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ScholarshipRequestDetails(BaseModel):
    """Reason for requesting the scholarship and eligibility confirmations"""

    reason_you_are_requesting_this_scholarship: str = Field(
        ...,
        description=(
            "Explanation of why you are requesting a National Testing Network fee "
            'scholarship .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    reviewed_minimum_requirements_and_assert_qualified: BooleanLike = Field(
        ...,
        description=(
            "Check to confirm you meet the minimum requirements and disqualifiers listed on "
            "the recruiting website"
        ),
    )

    no_four_year_degree_now_or_by_time_of_hire: BooleanLike = Field(
        ...,
        description=(
            "Check to confirm you do not have and do not plan to have a four-year degree by "
            "time of hire, acknowledging the NTN test requirement"
        ),
    )


class NationalTestingNetworkFeeScholarshipRequestForm(BaseModel):
    """
    National Testing Network Fee SCHOLARSHIP Request Form

    The Portland Police Bureau uses an interactive testing process to better evaluate an applicant’s ability to engage with people and make quality decisions through scenario-based videos.
    The National Test Network (NTN) provides this test and there is a $49 fee associated with the service. However, the Portland Police Bureau does not want a fee to prevent any interested person from testing to become a Community Police Officer. If you are interested in exploring this opportunity but discouraged by the fee, please complete this Scholarship Request Form.
    The Portland Police Bureau has scholarships available and if you have any questions please call the Personnel Division at (503) 823-0333. Receiving a scholarship has no bearing on your scoring or testing outcomes. Upon acceptance of this scholarship, the testing results are only valid for the Portland Police Bureau, and your test results will not be forwarded to other police agencies.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    scholarship_request_details: ScholarshipRequestDetails = Field(
        ..., description="Scholarship Request Details"
    )
