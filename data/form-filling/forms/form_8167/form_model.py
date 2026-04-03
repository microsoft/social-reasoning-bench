from typing import Literal, Optional, List, Union
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
        default="", description="Check if your team will provide the website copy/content."
    )

    photography_we_can_provide: BooleanLike = Field(
        default="", description="Check if your team will provide photography for the website."
    )

    videos_animation_we_can_provide: BooleanLike = Field(
        default="",
        description="Check if your team will provide videos or animations for the website.",
    )

    logos_and_graphics_we_can_provide: BooleanLike = Field(
        default="", description="Check if your team will provide logos and graphic assets."
    )

    copy_well_need_you_to_source: BooleanLike = Field(
        default="", description="Check if you need the agency to create or source the website copy."
    )

    photography_well_need_you_to_source: BooleanLike = Field(
        default="", description="Check if you need the agency to source or create photography."
    )

    videos_animation_well_need_you_to_source: BooleanLike = Field(
        default="",
        description="Check if you need the agency to source or create videos/animations.",
    )

    logos_and_graphics_well_need_you_to_source: BooleanLike = Field(
        default="",
        description="Check if you need the agency to create or source logos and graphics.",
    )


class WebsiteFunctionalityRequirements(BaseModel):
    """Required features and functionality for the new website"""

    team_page: BooleanLike = Field(
        default="", description="Check if the new website should include a team or staff page."
    )

    social_media_feeds: BooleanLike = Field(
        default="", description="Check if the site should display live social media feeds."
    )

    document_library: BooleanLike = Field(
        default="",
        description="Check if the site should include a document library or downloads area.",
    )

    image_gallery: BooleanLike = Field(
        default="", description="Check if the site should include an image gallery."
    )

    enquiry_form_or_other_types_of_form: BooleanLike = Field(
        default="", description="Check if the site should include enquiry or other web forms."
    )

    data_capture_and_export: BooleanLike = Field(
        default="",
        description="Check if the site should capture data and allow export (e.g. to CSV/CRM).",
    )

    location_maps: BooleanLike = Field(
        default="", description="Check if the site should include location maps (e.g. Google Maps)."
    )

    password_protected_areas: BooleanLike = Field(
        default="",
        description="Check if the site should include password-protected or members-only areas.",
    )

    news_blog: BooleanLike = Field(
        default="", description="Check if the site should include a news or blog section."
    )

    live_chat: BooleanLike = Field(
        default="", description="Check if the site should include live chat functionality."
    )

    email_newsletter_signup: BooleanLike = Field(
        default="", description="Check if the site should include an email newsletter signup form."
    )

    other_please_specify_below: BooleanLike = Field(
        default="",
        description="Check if you need other functionality not listed and describe it below.",
    )

    other_functionality_details_line_1: str = Field(
        default="",
        description=(
            "First line describing any other required website functionality. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    other_functionality_details_line_2: str = Field(
        default="",
        description=(
            "Second line describing any other required website functionality. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other_functionality_details_line_3: str = Field(
        default="",
        description=(
            "Third line describing any other required website functionality. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    other_functionality_details_line_4: str = Field(
        default="",
        description=(
            "Fourth line describing any other required website functionality. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class SystemIntegrations(BaseModel):
    """External systems the new website needs to integrate with"""

    systems_to_integrate_with_line_1: str = Field(
        default="",
        description=(
            "First system or integration the new website needs to connect with. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    systems_to_integrate_with_line_2: str = Field(
        default="",
        description=(
            "Second system or integration the new website needs to connect with. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    systems_to_integrate_with_line_3: str = Field(
        default="",
        description=(
            "Third system or integration the new website needs to connect with. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    systems_to_integrate_with_line_4: str = Field(
        default="",
        description=(
            "Fourth system or integration the new website needs to connect with. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    systems_to_integrate_with_line_5: str = Field(
        default="",
        description=(
            "Fifth system or integration the new website needs to connect with. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class WebsiteDesignBrief(BaseModel):
    """
    Website design brief

    ''
    """

    content_provision: ContentProvision = Field(..., description="Content Provision")
    website_functionality_requirements: WebsiteFunctionalityRequirements = Field(
        ..., description="Website Functionality Requirements"
    )
    system_integrations: SystemIntegrations = Field(..., description="System Integrations")
