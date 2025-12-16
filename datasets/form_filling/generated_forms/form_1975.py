from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MilitaryService(BaseModel):
    """
    MILITARY SERVICE

    Please introduce us to your story of your service in the post 9/11 Global War on Terror. How and when were you injured? What were your dates of service?
    """

    military_service_please_introduce_us_to_your_story_of_your_service_in_the_post_9_11_global_war_on_terror_how_and_when_were_you_injured_what_were_your_dates_of_service: str = Field(
        ...,
        description=(
            "Describe your post-9/11 military service, including your role, how and when "
            "you were injured, and your dates of service. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )
