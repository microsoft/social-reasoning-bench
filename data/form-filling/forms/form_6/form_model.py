from pydantic import BaseModel, ConfigDict, Field


class NeighborhoodNotificationInitiativeNeighborhoodRegistrationForm(BaseModel):
    """Neighborhood Notification Initiative Neighborhood Registration Form

    Neighborhood organizations submit this form to register with Athens-Clarke County’s Neighborhood Notification Initiative so they can receive official neighborhood notifications and be recognized with defined neighborhood boundaries and a designated contact person. Planning Department staff intake and verify the registration materials, and the Mayor and Commission review the submission to approve the registration based on the provided organization details, contact information, and supporting documentation.
    """

    model_config = ConfigDict(extra="forbid")

    required_information_type_other_specify: str = Field(
        ...,
        description='Type other (specify). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    required_information_commission_districts: str = Field(
        ...,
        description='Commission districts. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    required_information_telephone_number: str = Field(
        ...,
        description='Telephone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    optional_information_website: str = Field(
        ...,
        description='Website. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    optional_information_newsletter_or_other_publication: str = Field(
        ...,
        description='Newsletter/other publication. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    optional_information_regularly_scheduled_meetings_details: str = Field(
        ...,
        description='Meetings date/time/location. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    optional_information_comments_questions_suggested_topics: str = Field(
        ...,
        description='Comments/questions/suggested topics. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
