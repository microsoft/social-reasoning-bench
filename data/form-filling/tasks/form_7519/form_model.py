from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Identityoftheissuer1(BaseModel):
    """Issuer identification"""

    identity_of_the_issuer: str = Field(
        ...,
        description=(
            "Legal name of the issuer whose major holdings are being notified .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Reasonforthenotification2(BaseModel):
    """Type of event triggering the notification"""

    an_acquisition_or_disposal_of_voting_rights_or_share_capital: BooleanLike = Field(
        ...,
        description=(
            "Tick if the notification concerns an acquisition or disposal of voting rights "
            "or share capital"
        ),
    )

    an_acquisition_or_disposal_of_financial_instruments: BooleanLike = Field(
        ...,
        description=(
            "Tick if the notification concerns an acquisition or disposal of financial instruments"
        ),
    )

    an_event_changing_the_breakdown_of_voting_rights_or_share_capital: BooleanLike = Field(
        ...,
        description=(
            "Tick if the notification concerns an event changing the breakdown of voting "
            "rights or share capital"
        ),
    )

    other_please_specify: str = Field(
        default="",
        description=(
            "If the reason is not listed above, tick this and briefly describe the reason "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class Detailsofpersonsubjecttothenotificationobligation3(BaseModel):
    """Contact details of the notifying person"""

    name: str = Field(
        ...,
        description=(
            "Full name of the person subject to the notification obligation .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Postal address of the person subject to the notification obligation .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    national_id_number: str = Field(
        ...,
        description=(
            "National identification number of the person subject to the notification "
            'obligation .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            "Email address of the person subject to the notification obligation .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Fullnameofshareholder4(BaseModel):
    """Shareholder identity if different from notifying person"""

    full_name_of_shareholder_if_different_from_3: str = Field(
        default="",
        description=(
            "Full name of the shareholder if not the same as the person in section 3 .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Datethresholdcrossedorreached5(BaseModel):
    """Relevant date for the notification"""

    date_on_which_the_threshold_was_crossed_or_reached: str = Field(
        ...,
        description="Calendar date when the relevant threshold of holdings was crossed or reached",
    )  # YYYY-MM-DD format


class StandardFormForNotificationOfMajorHoldings(BaseModel):
    """
    Standard form for notification of major holdings

    Standard form for notification of major holdings
    NOTIFICATION OF MAJOR HOLDINGS (to be uploaded at http://oasm.finanstilsynet.dk)
    The boxes in sections (1-6) and section (8) in the standard form must always be filled out.
    Then, please fill out the sections in the standard form for the relevant type of financial instrument.
    •  For notification regarding shares go to section (7.1) in the standard form.
    •  For notification regarding financial instruments in accordance with section 39(2)(1) of the Capital Markets Act, go to section (7.2) in the standard form.
    •  For notification regarding financial instruments in accordance with section 39(2)(2) of the Capital Markets Act, go to section (7.3) in the standard form.
    In case of proxy voting, fill out section (9) in the standard form.
    """

    identity_of_the_issuer: Identityoftheissuer1 = Field(
        ..., description="1. Identity of the issuer"
    )
    reason_for_the_notification: Reasonforthenotification2 = Field(
        ..., description="2. Reason for the notification"
    )
    details_of_person_subject_to_the_notification_obligation: Detailsofpersonsubjecttothenotificationobligation3 = Field(
        ..., description="3. Details of person subject to the notification obligation"
    )
    full_name_of_shareholder: Fullnameofshareholder4 = Field(
        ..., description="4. Full name of shareholder"
    )
    date_threshold_crossed_or_reached: Datethresholdcrossedorreached5 = Field(
        ..., description="5. Date threshold crossed or reached"
    )
