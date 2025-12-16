from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ClientStage1(BaseModel):
    """Pain points, solutions, and content ideas for client stage 1"""

    client_stage_1_her_biggest_pain_points_row_1: str = Field(
        default="",
        description=(
            "First main pain point your client experiences at stage 1. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    client_stage_1_the_solution_you_provide_row_1: str = Field(
        default="",
        description=(
            "Primary solution you offer to address the first pain point at stage 1. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    client_stage_1_content_for_this_client_stage_row_1: str = Field(
        default="",
        description=(
            "Type of content you will create to support the first solution at stage 1. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    client_stage_1_her_biggest_pain_points_row_2: str = Field(
        default="",
        description=(
            "Second main pain point your client experiences at stage 1. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    client_stage_1_the_solution_you_provide_row_2: str = Field(
        default="",
        description=(
            "Solution you offer to address the second pain point at stage 1. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    client_stage_1_content_for_this_client_stage_row_2: str = Field(
        default="",
        description=(
            "Type of content you will create to support the second solution at stage 1. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ClientStage2(BaseModel):
    """Pain points, solutions, and content ideas for client stage 2"""

    client_stage_2_her_biggest_pain_points_row_1: str = Field(
        default="",
        description=(
            "First main pain point your client experiences at stage 2. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    client_stage_2_the_solution_you_provide_row_1: str = Field(
        default="",
        description=(
            "Primary solution you offer to address the first pain point at stage 2. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    client_stage_2_content_for_this_client_stage_row_1: str = Field(
        default="",
        description=(
            "Type of content you will create to support the first solution at stage 2. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    client_stage_2_her_biggest_pain_points_row_2: str = Field(
        default="",
        description=(
            "Second main pain point your client experiences at stage 2. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    client_stage_2_the_solution_you_provide_row_2: str = Field(
        default="",
        description=(
            "Solution you offer to address the second pain point at stage 2. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    client_stage_2_content_for_this_client_stage_row_2: str = Field(
        default="",
        description=(
            "Type of content you will create to support the second solution at stage 2. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ClientStage3(BaseModel):
    """Pain points, solutions, and content ideas for client stage 3"""

    client_stage_3_her_biggest_pain_points_row_1: str = Field(
        default="",
        description=(
            "First main pain point your client experiences at stage 3. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    client_stage_3_the_solution_you_provide_row_1: str = Field(
        default="",
        description=(
            "Primary solution you offer to address the first pain point at stage 3. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    client_stage_3_content_for_this_client_stage_row_1: str = Field(
        default="",
        description=(
            "Type of content you will create to support the first solution at stage 3. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    client_stage_3_her_biggest_pain_points_row_2: str = Field(
        default="",
        description=(
            "Second main pain point your client experiences at stage 3. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    client_stage_3_the_solution_you_provide_row_2: str = Field(
        default="",
        description=(
            "Solution you offer to address the second pain point at stage 3. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    client_stage_3_content_for_this_client_stage_row_2: str = Field(
        default="",
        description=(
            "Type of content you will create to support the second solution at stage 3. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ClientStage4(BaseModel):
    """Pain points, solutions, and content ideas for client stage 4"""

    client_stage_4_her_biggest_pain_points_row_1: str = Field(
        default="",
        description=(
            "First main pain point your client experiences at stage 4. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    client_stage_4_the_solution_you_provide_row_1: str = Field(
        default="",
        description=(
            "Primary solution you offer to address the first pain point at stage 4. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    client_stage_4_content_for_this_client_stage_row_1: str = Field(
        default="",
        description=(
            "Type of content you will create to support the first solution at stage 4. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    client_stage_4_her_biggest_pain_points_row_2: str = Field(
        default="",
        description=(
            "Second main pain point your client experiences at stage 4. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    client_stage_4_the_solution_you_provide_row_2: str = Field(
        default="",
        description=(
            "Solution you offer to address the second pain point at stage 4. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    client_stage_4_content_for_this_client_stage_row_2: str = Field(
        default="",
        description=(
            "Type of content you will create to support the second solution at stage 4. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ToolkitClientcontentMap(BaseModel):
    """
        TOOLKIT

    Client-Content Map

        Map out the stages of your client's journey and what content your client needs and wants at each stage. Revisit the blog post if you need additional guidance on this section.
    """

    client_stage_1: ClientStage1 = Field(..., description="Client Stage #1")
    client_stage_2: ClientStage2 = Field(..., description="Client Stage #2")
    client_stage_3: ClientStage3 = Field(..., description="Client Stage #3")
    client_stage_4: ClientStage4 = Field(..., description="Client Stage #4")
