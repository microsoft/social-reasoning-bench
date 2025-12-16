from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class JobStepsHazardsandControls(BaseModel):
    """Details on the steps to complete the job, associated risks or hazards, and controls"""

    step_1_describe_actions_to_complete_this_step: str = Field(
        ...,
        description=(
            "Describe the specific actions required to complete step 1 of the job. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    step_1_what_are_the_risks_or_hazards_to_complete_this_step: str = Field(
        ...,
        description=(
            "List the risks or hazards associated with performing step 1. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    step_1_actions_taken_to_eliminate_or_control_the_risks_or_hazards: str = Field(
        ...,
        description=(
            "Describe the controls or actions that will be used to eliminate or reduce the "
            'risks for step 1. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    step_2_describe_actions_to_complete_this_step: str = Field(
        ...,
        description=(
            "Describe the specific actions required to complete step 2 of the job. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    step_2_what_are_the_risks_or_hazards_to_complete_this_step: str = Field(
        ...,
        description=(
            "List the risks or hazards associated with performing step 2. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    step_2_actions_taken_to_eliminate_or_control_the_risks_or_hazards: str = Field(
        ...,
        description=(
            "Describe the controls or actions that will be used to eliminate or reduce the "
            'risks for step 2. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    step_3_describe_actions_to_complete_this_step: str = Field(
        ...,
        description=(
            "Describe the specific actions required to complete step 3 of the job. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    step_3_what_are_the_risks_or_hazards_to_complete_this_step: str = Field(
        ...,
        description=(
            "List the risks or hazards associated with performing step 3. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    step_3_actions_taken_to_eliminate_or_control_the_risks_or_hazards: str = Field(
        ...,
        description=(
            "Describe the controls or actions that will be used to eliminate or reduce the "
            'risks for step 3. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    step_4_describe_actions_to_complete_this_step: str = Field(
        ...,
        description=(
            "Describe the specific actions required to complete step 4 of the job. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    step_4_what_are_the_risks_or_hazards_to_complete_this_step: str = Field(
        ...,
        description=(
            "List the risks or hazards associated with performing step 4. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    step_4_actions_taken_to_eliminate_or_control_the_risks_or_hazards: str = Field(
        ...,
        description=(
            "Describe the controls or actions that will be used to eliminate or reduce the "
            'risks for step 4. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class AdditionalComments(BaseModel):
    """Space for any additional notes or comments"""

    additional_comments_line_1: str = Field(
        default="",
        description=(
            "First line for any additional comments or notes. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_comments_line_2: str = Field(
        default="",
        description=(
            "Second line for any additional comments or notes. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_comments_line_3: str = Field(
        default="",
        description=(
            "Third line for any additional comments or notes. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class TeamMembersandSignatures(BaseModel):
    """Team member names and corresponding signatures"""

    team_member_1_please_print: str = Field(
        ...,
        description=(
            "Printed name of the first team member. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    signature_1: str = Field(
        ...,
        description=(
            'Signature of the first team member. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    team_member_2_please_print: str = Field(
        default="",
        description=(
            "Printed name of the second team member. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    signature_2: str = Field(
        default="",
        description=(
            'Signature of the second team member. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    team_member_3_please_print: str = Field(
        default="",
        description=(
            "Printed name of the third team member. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    signature_3: str = Field(
        default="",
        description=(
            'Signature of the third team member. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    team_member_4_please_print: str = Field(
        default="",
        description=(
            "Printed name of the fourth team member. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    signature_4: str = Field(
        default="",
        description=(
            'Signature of the fourth team member. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    team_member_5_please_print: str = Field(
        default="",
        description=(
            "Printed name of the fifth team member. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    signature_5: str = Field(
        default="",
        description=(
            'Signature of the fifth team member. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class NavCanadaContractorSiteSpecificSafetyPlanAppendixB(BaseModel):
    """
    NAV CANADA CONTRACTOR SITE SPECIFIC SAFETY PLAN                   APPENDIX B

    Please provide details on the steps to complete this job, the risks or hazards involved with those steps and how the steps are going to be performed safely:
    """

    job_steps_hazards_and_controls: JobStepsHazardsandControls = Field(
        ..., description="Job Steps, Hazards and Controls"
    )
    additional_comments: AdditionalComments = Field(..., description="Additional Comments")
    team_members_and_signatures: TeamMembersandSignatures = Field(
        ..., description="Team Members and Signatures"
    )
