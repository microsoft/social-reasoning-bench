from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RequestType(BaseModel):
    """Indicates whether this is a new interim assignment request or an extension and related initial term information"""

    initial_request: BooleanLike = Field(
        ..., description="Check if this is an initial interim assignment request."
    )

    request_for_extension: BooleanLike = Field(
        ...,
        description="Check if this request is for an extension of an existing interim assignment.",
    )

    initial_term_of_the_original_interim_assignment: str = Field(
        default="",
        description=(
            "Describe the initial term (start and end dates or duration) of the original "
            "interim assignment, if this is an extension. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProposedInterimAssignmentPositionDetails(BaseModel):
    """Core details about the proposed interim assignment position"""

    title: str = Field(
        ...,
        description=(
            "Job title of the proposed interim assignment position. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    grade: str = Field(
        ...,
        description=(
            "Pay or classification grade for the interim assignment position. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    rate_of_pay: str = Field(
        ...,
        description=(
            "Rate of pay for the interim assignment (e.g., hourly, bi-weekly, or annual "
            'rate). .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    position_id: str = Field(
        ...,
        description=(
            "Unique identifier or position number for the interim assignment role. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class VacancyInformation(BaseModel):
    """Information about the vacancy, its cause, timing, and status of the previous incumbent"""

    reason_position_is_currently_vacant: str = Field(
        ...,
        description=(
            "Explain why the position is currently vacant (e.g., resignation, promotion, "
            'leave of absence). .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date_vacancy_began_if_known: str = Field(
        default="",
        description="Date on which the position became vacant, if this information is available.",
    )  # YYYY-MM-DD format

    estimated_date_vacancy_is_expected_to_end: str = Field(
        default="", description="Estimated date when the vacancy is expected to be filled or end."
    )  # YYYY-MM-DD format

    yes_employee_on_loa_expected_to_return: BooleanLike = Field(
        ...,
        description=(
            "Select 'Yes' if the previous incumbent is on a leave of absence and is "
            "expected to return."
        ),
    )

    no_employee_on_loa_expected_to_return: BooleanLike = Field(
        ...,
        description=(
            "Select 'No' if the previous incumbent is not on a leave of absence or is not "
            "expected to return."
        ),
    )

    if_yes_when_is_return_anticipated: str = Field(
        default="",
        description=(
            "If the previous employee is expected to return, provide the anticipated return date."
        ),
    )  # YYYY-MM-DD format


class RecruitmentandSupportingInformation(BaseModel):
    """Steps taken to fill the position and any additional supporting details for the request"""

    steps_that_have_been_taken_to_fill_the_position: str = Field(
        default="",
        description=(
            "Describe any recruitment or other actions already taken to fill the vacant "
            'position. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    additional_information_in_support_of_this_request: str = Field(
        default="",
        description=(
            "Provide any additional context or justification supporting this interim "
            'assignment request. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class CookCountyBureauOfHumanResourcesInterimAssignmentRequestForm(BaseModel):
    """
        COOK COUNTY BUREAU OF HUMAN RESOURCES
    INTERIM ASSIGNMENT REQUEST FORM

        ''
    """

    request_type: RequestType = Field(..., description="Request Type")
    proposed_interim_assignment_position_details: ProposedInterimAssignmentPositionDetails = Field(
        ..., description="Proposed Interim Assignment Position Details"
    )
    vacancy_information: VacancyInformation = Field(..., description="Vacancy Information")
    recruitment_and_supporting_information: RecruitmentandSupportingInformation = Field(
        ..., description="Recruitment and Supporting Information"
    )
