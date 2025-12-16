from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class TechnologyRequest(BaseModel):
    """
    Technology Request

    Please note:
    - Blue fields are mandatory
    - To fill in fields marked with asterisk (*) it is recommended to consider the related notes (see at the bottom of this form)
    - Fields to be ticked always have one selection unless differently specified under the field title
    """

    title: str = Field(
        ...,
        description=(
            'Short title of the technology request .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    summary: str = Field(
        ...,
        description=(
            "Brief summary of the technology request (1–500 characters) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    stage_of_development_already_on_the_market: BooleanLike = Field(
        ..., description="Select if the technology is already commercially available on the market"
    )

    stage_of_development_available_for_demonstration: BooleanLike = Field(
        ..., description="Select if the technology is available for demonstration"
    )

    stage_of_development_concept_stage: BooleanLike = Field(
        ..., description="Select if the technology is at a conceptual stage only"
    )

    stage_of_development_field_tested_evaluated: BooleanLike = Field(
        ..., description="Select if the technology has been field tested or evaluated"
    )

    stage_of_development_project_already_started: BooleanLike = Field(
        ..., description="Select if a project related to this technology has already started"
    )

    stage_of_development_project_in_negotiations_urgent: BooleanLike = Field(
        ..., description="Select if the project is currently in negotiations and is urgent"
    )

    stage_of_development_proposal_under_development: BooleanLike = Field(
        ..., description="Select if a proposal related to this technology is under development"
    )

    stage_of_development_prototype_available_for_demonstration: BooleanLike = Field(
        ..., description="Select if a prototype is available for demonstration"
    )

    stage_of_development_under_development_lab_tested: BooleanLike = Field(
        ..., description="Select if the technology is under development or has been lab tested"
    )

    comments_regarding_stage_of_development: str = Field(
        default="",
        description=(
            "Additional comments or clarifications about the stage of development .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    description: str = Field(
        ...,
        description=(
            "Detailed description of the technology request (100–4000 characters) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )
