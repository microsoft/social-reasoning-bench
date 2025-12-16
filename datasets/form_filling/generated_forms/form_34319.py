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
    """Basic information about the business/employer"""

    business_employer_entity_name: str = Field(
        ...,
        description=(
            "Legal name of the business or employer entity applying for the grant .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    industry: str = Field(
        ...,
        description=(
            "Primary industry or sector in which the business operates .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PrimaryPointofContact(BaseModel):
    """Contact details for the primary point of contact"""

    name: str = Field(
        ...,
        description=(
            "Name of the primary point of contact for this application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Street address for the primary point of contact or business .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    city_state_zip: str = Field(
        ...,
        description=(
            "City, state, and ZIP code corresponding to the address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Primary phone number for the point of contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            "Email address for the primary point of contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class BusinessInformation(BaseModel):
    """Details about the position, relocation, and grant request"""

    what_attempts_if_any_have_been_made_to_fill_this_position_locally: str = Field(
        ...,
        description=(
            "Describe efforts taken to recruit or hire locally for this position .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    are_there_specific_qualifications_or_certification_needed_for_this_position: str = Field(
        ...,
        description=(
            "List any required qualifications, skills, or certifications for the position "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    is_this_position_a_recurring_need_for_your_business: BooleanLike = Field(
        ..., description="Indicate whether this position is a recurring need for the business"
    )

    is_this_position_a_recurring_need_for_your_business_no: BooleanLike = Field(
        default="",
        description="Indicate whether this position is not a recurring need for the business",
    )

    how_many_individuals_do_you_wish_to_relocate: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of individuals the business intends to relocate"
    )

    does_the_business_currently_or_in_the_past_offered_a_relocation_incentive: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether the business currently offers or has previously offered "
            "relocation incentives"
        ),
    )

    does_the_business_currently_or_in_the_past_offered_a_relocation_incentive_no: BooleanLike = (
        Field(
            default="",
            description=(
                "Indicate that the business does not currently and has not previously offered "
                "relocation incentives"
            ),
        )
    )

    has_a_candidate_been_identified: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether a specific candidate for this position has already been identified"
        ),
    )

    has_a_candidate_been_identified_no: BooleanLike = Field(
        default="",
        description="Indicate that no specific candidate has yet been identified for this position",
    )

    what_position_will_this_individual_fill: str = Field(
        ...,
        description=(
            "Job title or role that the relocated individual will fill .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    what_is_the_salary_for_this_position_hourly: BooleanLike = Field(
        ..., description="Select if the salary for this position is paid on an hourly basis"
    )

    what_is_the_salary_for_this_position_annual: BooleanLike = Field(
        default="", description="Select if the salary for this position is paid on an annual basis"
    )

    what_is_the_total_relocation_amount_that_will_be_paid_per_individual: str = Field(
        ...,
        description=(
            "Dollar amount of relocation assistance to be paid per individual .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    will_you_provide_the_incentive_as_a_lump_sum_or_pay_over_a_period_of_time: str = Field(
        ...,
        description=(
            "Explain whether the relocation incentive will be paid as a lump sum or over "
            'time .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    total_amount_of_grant_funds_requested: str = Field(
        ...,
        description=(
            "Total dollar amount of grant funding being requested .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Authorization(BaseModel):
    """Signature and date of application"""

    signature: str = Field(
        ...,
        description=(
            'Authorized representative’s signature .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the application is signed")  # YYYY-MM-DD format


class ElevateRelocateGrant(BaseModel):
    """
    ELEVATE  |  RELOCATE GRANT

    ''
    """

    application_information: ApplicationInformation = Field(
        ..., description="Application Information"
    )
    primary_point_of_contact: PrimaryPointofContact = Field(
        ..., description="Primary Point of Contact"
    )
    business_information: BusinessInformation = Field(..., description="Business Information")
    authorization: Authorization = Field(..., description="Authorization")
