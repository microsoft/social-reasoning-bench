from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class BequestIntentions(BaseModel):
    """Your intentions regarding a bequest to St Catherine’s School and membership of the Fielding Fellowship"""

    i_intend_to_make_a_bequest_to_st_catherines_school_waverley: BooleanLike = Field(
        default="",
        description=(
            "Tick to indicate you intend to make a bequest to St Catherine’s School Waverley."
        ),
    )

    i_wish_to_advise_that_i_have_included_st_catherines_school_waverley_as_a_beneficiary_in_my_will: BooleanLike = Field(
        default="",
        description=(
            "Tick to indicate you have already included St Catherine’s School Waverley as a "
            "beneficiary in your Will."
        ),
    )

    i_prefer_no_public_acknowledgment_of_my_bequest: BooleanLike = Field(
        default="", description="Tick if you do not wish your bequest to be publicly acknowledged."
    )

    i_would_like_the_school_to_know_the_following_about_my_bequest_please_attach: BooleanLike = (
        Field(
            default="",
            description=(
                "Tick if you are providing additional information about your bequest in an "
                "attachment."
            ),
        )
    )

    please_contact_me_to_discuss_my_bequest: BooleanLike = Field(
        default="",
        description="Tick if you would like the school to contact you to discuss your bequest.",
    )


class PersonalDetails(BaseModel):
    """Your contact details and relationship to St Catherine’s"""

    name: str = Field(
        ...,
        description=(
            'Your full name. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    signed: str = Field(
        ...,
        description=(
            "Your signature confirming the information provided. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    dated: str = Field(..., description="Date on which you signed this form.")  # YYYY-MM-DD format

    maiden_name: str = Field(
        default="",
        description=(
            'Your maiden name, if applicable. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    year_of_leaving_st_catherines: Union[float, Literal["N/A", ""]] = Field(
        default="", description="The year you left St Catherine’s (four-digit year)."
    )

    address: str = Field(
        ...,
        description=(
            'Your postal address. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    postcode: str = Field(..., description="Postcode for your address.")

    phone: str = Field(
        ...,
        description=(
            'Your contact phone number. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Your email address. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    old_girl: BooleanLike = Field(
        default="", description="Tick if you are an Old Girl of St Catherine’s."
    )

    present_past_parent: BooleanLike = Field(
        default="",
        description="Tick if you are a present or past parent of a student at St Catherine’s.",
    )

    present_past_staff: BooleanLike = Field(
        default="", description="Tick if you are present or past staff of St Catherine’s."
    )

    friend_of_st_catherines: BooleanLike = Field(
        default="", description="Tick if you are a friend or supporter of St Catherine’s."
    )


class BecomeAMemberOfTheFieldingFellowship(BaseModel):
    """
    Become a member of the Fielding Fellowship

    If you wish to indicate your support for St Catherine’s School by making a bequest and becoming a member of the Fielding Fellowship, please complete this form and return it to the school. This is not a legal document, but an indication of your intentions.
    """

    bequest_intentions: BequestIntentions = Field(..., description="Bequest Intentions")
    personal_details: PersonalDetails = Field(..., description="Personal Details")
