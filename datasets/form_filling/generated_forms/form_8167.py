from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ContentProvision(BaseModel):
    """What content you can provide vs what needs to be sourced"""

    copy_we_can_provide: BooleanLike = Field(
        default="", description="Select if you will provide the written copy for the website."
    )

    photography_we_can_provide: BooleanLike = Field(
        default="", description="Select if you will provide photography assets for the website."
    )

    videos_animation_we_can_provide: BooleanLike = Field(
        default="",
        description="Select if you will provide video or animation assets for the website.",
    )

    logos_and_graphics_we_can_provide: BooleanLike = Field(
        default="",
        description="Select if you will provide logo files and other graphic assets for the website.",
    )

    copy_well_need_you_to_source: BooleanLike = Field(
        default="",
        description="Select if you need the agency to create or source the written copy.",
    )

    photography_well_need_you_to_source: BooleanLike = Field(
        default="", description="Select if you need the agency to create or source photography."
    )

    videos_animation_well_need_you_to_source: BooleanLike = Field(
        default="",
        description="Select if you need the agency to create or source video or animation assets.",
    )

    logos_and_graphics_well_need_you_to_source: BooleanLike = Field(
        default="",
        description="Select if you need the agency to create or source logo and graphic assets.",
    )


class WebsiteFunctionality(BaseModel):
    """Required features and functionality for the new website"""

    team_page: BooleanLike = Field(
        default="", description="Select if the new website should include a team or staff page."
    )

    social_media_feeds: BooleanLike = Field(
        default="", description="Select if the website should display live social media feeds."
    )

    document_library: BooleanLike = Field(
        default="",
        description="Select if the website should include a document library or downloads area.",
    )

    image_gallery: BooleanLike = Field(
        default="", description="Select if the website should include an image gallery."
    )

    enquiry_form_or_other_types_of_form: BooleanLike = Field(
        default="",
        description="Select if the website should include enquiry or other types of forms.",
    )

    data_capture_and_export: BooleanLike = Field(
        default="",
        description="Select if the website should capture user data and allow exporting it.",
    )

    location_maps: BooleanLike = Field(
        default="",
        description="Select if the website should display location maps (e.g. Google Maps).",
    )

    password_protected_areas: BooleanLike = Field(
        default="",
        description="Select if parts of the website should be restricted behind login or passwords.",
    )

    news_blog: BooleanLike = Field(
        default="", description="Select if the website should include a news or blog section."
    )

    live_chat: BooleanLike = Field(
        default="", description="Select if the website should include live chat functionality."
    )

    email_newsletter_signup: BooleanLike = Field(
        default="",
        description="Select if the website should include an email newsletter signup form.",
    )

    other_please_specify_below: BooleanLike = Field(
        default="",
        description=(
            "Select if you need additional functionality not listed and will describe it below."
        ),
    )

    additional_functionality_details: str = Field(
        default="",
        description=(
            "Describe any other website functionality or details not covered by the "
            'checkboxes above. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class SystemIntegrations(BaseModel):
    """External systems the new website needs to integrate with"""

    systems_our_new_website_needs_to_integrate_with: str = Field(
        default="",
        description=(
            "List any third-party systems, platforms, or tools the website must integrate "
            'with. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class WebsiteDesignBrief(BaseModel):
    """
    Website design brief

    ''
    """

    content_provision: ContentProvision = Field(..., description="Content Provision")
    website_functionality: WebsiteFunctionality = Field(..., description="Website Functionality")
    system_integrations: SystemIntegrations = Field(..., description="System Integrations")
