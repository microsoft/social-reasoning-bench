from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EmploymentExperience(BaseModel):
    """
    Employment Experience

    Start with your present or last job including any military service assignments and complete the below information fully. Give dates and reasons, excluding disabilities, for time not accounted for in your employment history as listed. If you need additional space, please continue on a separate sheet of paper.
    """

    employer: str = Field(
        ...,
        description=(
            "Name of the employer for this position .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    start_date: str = Field(
        ..., description="Date you started working for this employer"
    )  # YYYY-MM-DD format

    your_job_title_and_major_duties: str = Field(
        ...,
        description=(
            "Your job title and a brief summary of your main responsibilities .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street address of the employer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    end_date: str = Field(
        ..., description="Date you stopped working for this employer"
    )  # YYYY-MM-DD format

    city: str = Field(
        ...,
        description=(
            'City where the employer is located .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State where the employer is located")

    telephone_no: str = Field(
        ...,
        description=(
            'Employer’s telephone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    starting_salary: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Your salary when you began this job (specify amount and, if needed, per "
            "hour/week/year)"
        ),
    )

    supervisor: str = Field(
        ...,
        description=(
            "Name of your immediate supervisor at this job .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_leaving: str = Field(
        ...,
        description=(
            "Brief explanation of why you left this position .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ending_salary: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Your salary when you left this job (specify amount and, if needed, per hour/week/year)"
        ),
    )
