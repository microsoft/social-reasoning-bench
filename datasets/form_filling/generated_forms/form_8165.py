from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class TypeofWebsiteRequired(BaseModel):
    """Select and describe the type of website needed"""

    information_brochure: BooleanLike = Field(
        default="",
        description="Select if the required website is primarily informational or brochure-style.",
    )

    ecommerce: BooleanLike = Field(
        default="",
        description=(
            "Select if the required website needs ecommerce functionality for selling "
            "products or services online."
        ),
    )

    lead_generation: BooleanLike = Field(
        default="",
        description=(
            "Select if the required website is primarily focused on generating leads or enquiries."
        ),
    )

    other_type_of_website_please_specify_below: BooleanLike = Field(
        default="",
        description=(
            "Select if the required website type is not listed and will be described in the "
            "text area below."
        ),
    )

    details_about_type_of_website_required: str = Field(
        default="",
        description=(
            "Describe in more detail the type of website you require, especially if you "
            "selected 'Other'. .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class WebsiteGoalsandRequirements(BaseModel):
    """What the new website should achieve and be able to do"""

    increase_sales_and_leads: BooleanLike = Field(
        default="",
        description=(
            "Select if one of the goals of the new website is to increase sales and lead "
            "generation."
        ),
    )

    provide_information_to_existing_customers: BooleanLike = Field(
        default="",
        description=(
            "Select if the website should focus on providing information to your existing "
            "customers."
        ),
    )

    have_a_better_design: BooleanLike = Field(
        default="",
        description="Select if improving the visual design of the website is a key objective.",
    )

    be_easy_to_update_in_house: BooleanLike = Field(
        default="",
        description="Select if the website should be simple for your team to update internally.",
    )

    improve_the_customer_experience: BooleanLike = Field(
        default="",
        description="Select if enhancing the overall customer experience on the site is a goal.",
    )

    other_website_needs_please_specify_below: BooleanLike = Field(
        default="",
        description="Select if you have other website needs not listed and will describe them below.",
    )

    capture_track_more_data_for_marketing: BooleanLike = Field(
        default="",
        description=(
            "Select if the website should better capture and track data for marketing purposes."
        ),
    )

    details_about_what_we_need_our_new_website_to_do: str = Field(
        default="",
        description=(
            "Provide more detailed information about the goals and functions you want the "
            'new website to achieve. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class ExistingWebsiteFeedback(BaseModel):
    """Likes and dislikes about the current website"""

    things_we_like_and_dislike_about_our_existing_website: str = Field(
        default="",
        description=(
            "Describe what you currently like and dislike about your existing website. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class WebsiteDesignBrief(BaseModel):
    """Website design brief"""

    type_of_website_required: TypeofWebsiteRequired = Field(
        ..., description="Type of Website Required"
    )
    website_goals_and_requirements: WebsiteGoalsandRequirements = Field(
        ..., description="Website Goals and Requirements"
    )
    existing_website_feedback: ExistingWebsiteFeedback = Field(
        ..., description="Existing Website Feedback"
    )
