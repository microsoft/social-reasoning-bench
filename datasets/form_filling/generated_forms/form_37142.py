from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FundraisingInformation(BaseModel):
    """Details about the proposed event or fundraiser and applicant signatures"""

    nature_of_the_event_or_fundraiser: str = Field(
        ...,
        description=(
            "Describe the type and nature of the event or fundraiser you are planning. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    fundraising_goal: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Dollar amount you aim to raise through this event or fundraiser."
    )

    how_the_event_or_fundraiser_will_be_advertised: str = Field(
        ...,
        description=(
            "Explain the advertising and promotion methods (e.g., TV, radio, flyers, "
            'website, social media). .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    how_participants_or_donors_will_receive_gift_acknowledgment_thank_you_letters: str = Field(
        ...,
        description=(
            "Describe the process for sending acknowledgments or thank you letters to "
            'participants or donors. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    how_funds_will_be_tracked_or_reported: str = Field(
        ...,
        description=(
            "Explain how you will record, track, and report funds raised from the event. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    whether_the_placer_spca_is_the_sole_beneficiary_of_the_event_and_other_beneficiaries: str = (
        Field(
            ...,
            description=(
                "Indicate if Placer SPCA is the only beneficiary; if not, list all other "
                'beneficiaries. .If you cannot fill this, write "N/A". If this field should '
                "not be filled by you (for example, it belongs to another person or office), "
                'leave it blank (empty string "").'
            ),
        )
    )

    applicant_signature: str = Field(
        ...,
        description=(
            "Signature of the applicant organizing the event. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    applicant_signature_date: str = Field(
        ..., description="Date the applicant signed the form."
    )  # YYYY-MM-DD format

    placer_spca_representative_signature: str = Field(
        ...,
        description=(
            "Signature of the Placer SPCA representative reviewing the application. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    placer_spca_representative_signature_date: str = Field(
        ..., description="Date the Placer SPCA representative signed the form."
    )  # YYYY-MM-DD format


class ForPlacerSPCAStaffOnly(BaseModel):
    """Internal review, decision, and staff assignment"""

    approved: BooleanLike = Field(
        default="", description="Indicates that the event or fundraiser has been approved by staff."
    )

    declined_at_this_time_because: str = Field(
        default="",
        description=(
            "Reason the event or fundraiser was declined, if applicable. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    staff_assigned: str = Field(
        default="",
        description=(
            "Name of the staff member assigned to this event or fundraiser. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    placer_spca_representative_signature_staff_only: str = Field(
        default="",
        description=(
            "Signature of the Placer SPCA representative completing the staff-only section. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    placer_spca_representative_signature_staff_only_date: str = Field(
        default="", description="Date the Placer SPCA representative signed the staff-only section."
    )  # YYYY-MM-DD format


class FundraisingInformation(BaseModel):
    """
    Fundraising Information

    Please complete the following form to provide more information about the type of fundraiser or event you are interested in planning. **Submit the completed form prior to any planning of the event.** Once the application has been submitted, we will review it and notify you of any questions concerns, and/or approval. Federal tax ID: #94-2607682
    """

    fundraising_information: FundraisingInformation = Field(
        ..., description="Fundraising Information"
    )
    for_placer_spca_staff_only: ForPlacerSPCAStaffOnly = Field(
        ..., description="For Placer SPCA Staff Only"
    )
