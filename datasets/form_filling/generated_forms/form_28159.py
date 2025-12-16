from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class HealthSafety(BaseModel):
    """Health issues, disabilities, and reasonable adjustments"""

    health_issues_or_disabilities_difficulty_carrying_out_functions: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you have any health issues or disabilities that may affect "
            "your ability to perform essential functions of the role."
        ),
    )

    yes_health_issues_or_disabilities: BooleanLike = Field(
        ...,
        description=(
            "Select this option if you do have health issues or disabilities affecting "
            "essential job functions."
        ),
    )

    no_health_issues_or_disabilities: BooleanLike = Field(
        ...,
        description=(
            "Select this option if you do not have health issues or disabilities affecting "
            "essential job functions."
        ),
    )

    health_issues_or_disabilities_details: str = Field(
        default="",
        description=(
            "Provide details of any health issues or disabilities that may affect your "
            "ability to perform essential job functions. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reasonable_adjustments_needs: str = Field(
        default="",
        description=(
            "Describe any reasonable adjustments or accommodations you may need to perform "
            'the role. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    acknowledge_requirement_to_notify_kinetic: BooleanLike = Field(
        ...,
        description=(
            "Acknowledgement that you must notify Kinetic if your health or disability "
            "circumstances change."
        ),
    )

    yes_acknowledge_requirement_to_notify_kinetic: BooleanLike = Field(
        ...,
        description=(
            "Confirm that you acknowledge the requirement to notify Kinetic if your "
            "circumstances change."
        ),
    )


class EmploymentHistoryEmployer1(BaseModel):
    """Details of previous employment for the past 5 years (most recent first)"""

    name_of_employer_1: str = Field(
        ...,
        description=(
            "Name of your most recent employer within the past 5 years. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Postal address of Employer 1. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    post_code: str = Field(..., description="Post code for Employer 1's address.")

    start_date: str = Field(
        ..., description="Date you started working for Employer 1."
    )  # YYYY-MM-DD format

    end_date: str = Field(
        ..., description="Date you finished working for Employer 1."
    )  # YYYY-MM-DD format

    position_held: str = Field(
        ...,
        description=(
            "Job title or position you held with Employer 1. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_leaving: str = Field(
        ...,
        description=(
            'Explain why you left Employer 1. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    manager_name: str = Field(
        ...,
        description=(
            "Name of your direct line manager at Employer 1. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    manager_email_address: str = Field(
        ...,
        description=(
            "Email address of your direct line manager at Employer 1. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    salary_for_post: str = Field(
        default="",
        description=(
            "Salary you received for the position with Employer 1 (include currency and "
            'frequency if applicable). .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    notice_period: str = Field(
        default="",
        description=(
            "Length of notice period required for the role with Employer 1. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    consent_to_obtain_reference: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you consent to Kinetic obtaining a reference from your direct "
            "line manager."
        ),
    )

    yes_consent_to_obtain_reference: BooleanLike = Field(
        ..., description="Select if you give consent for Kinetic to obtain a reference."
    )

    no_consent_to_obtain_reference: BooleanLike = Field(
        ..., description="Select if you do not give consent for Kinetic to obtain a reference."
    )

    no_consent_reason: str = Field(
        default="",
        description=(
            "If you do not consent to a reference being obtained, explain your reasons. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class HealthSafety(BaseModel):
    """
    Health & Safety

    The following questions on Health & Safety are asked in order to find out your needs in terms of reasonable adjustments that may be required in order to enable you to carry put your work accordingly.
    """

    health__safety: HealthSafety = Field(..., description="Health & Safety")
    employment_history___employer_1: EmploymentHistoryEmployer1 = Field(
        ..., description="Employment History - Employer 1"
    )
