from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class NomineeInformation(BaseModel):
    """Basic information about the Scoutmaster being nominated"""

    nominees_name_as_it_is_to_appear_on_certificate: str = Field(
        ...,
        description=(
            "Full name of the nominee exactly as it should appear on the certificate .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street mailing address of the nominee .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the nominee\'s mailing address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State or territory abbreviation for the nominee's address")

    zip: str = Field(..., description="ZIP or postal code for the nominee's address")

    inclusive_dates_of_service_as_scoutmaster_include_month_and_year: str = Field(
        ...,
        description=(
            "Range of dates (month and year) during which the nominee served as Scoutmaster "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    troop_no: str = Field(
        ...,
        description=(
            "Troop number with which the nominee is registered as Scoutmaster .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    commission_expiration_date: str = Field(
        ..., description="Month and day on which the Scoutmaster commission expires"
    )  # YYYY-MM-DD format

    commission_expiration_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Four-digit year in which the Scoutmaster commission expires"
    )


class UnitandTrainingHistory(BaseModel):
    """Unit recognition and nominee’s completed training"""

    dates_troop_received_quality_unit_award: str = Field(
        default="",
        description=(
            "All dates on which the troop received the Quality Unit Award during the "
            'nominee\'s tenure .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    date_nominee_completed_boy_scout_leader_fast_start_orientation: str = Field(
        default="", description="Completion date for Boy Scout Leader Fast Start Orientation"
    )  # YYYY-MM-DD format

    date_nominee_completed_new_leader_essentials: str = Field(
        default="", description="Completion date for New Leader Essentials training"
    )  # YYYY-MM-DD format

    date_nominee_completed_scoutmaster_and_assistant_scoutmaster_leader_specific_training: str = (
        Field(
            default="",
            description=(
                "Completion date for Scoutmaster and Assistant Scoutmaster Leader Specific Training"
            ),
        )
    )  # YYYY-MM-DD format

    date_nominee_completed_introduction_to_outdoor_leader_skills: str = Field(
        default="", description="Completion date for Introduction to Outdoor Leader Skills training"
    )  # YYYY-MM-DD format


class NominationandCouncilApproval(BaseModel):
    """Nomination, certification, and council approval signatures and date"""

    nominated_by: str = Field(
        ...,
        description=(
            "Name of the troop committee chair submitting the nomination .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    certified_by: str = Field(
        ...,
        description=(
            "Name of the unit or district commissioner certifying the nomination .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date: str = Field(..., description="Date the nomination form is signed")  # YYYY-MM-DD format

    approved_by_scout_executive: str = Field(
        ...,
        description=(
            "Name/signature of the Scout executive approving the award .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    approved_by_council_nesa_chair_or_council_commissioner: str = Field(
        ...,
        description=(
            "Name/signature of the council NESA chair or council commissioner approving the "
            'award .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class AwardCertificate(BaseModel):
    """Information and signatures appearing on the award certificate"""

    certificate_recipient_name_in_recognizing_the_devotion_of: str = Field(
        ...,
        description=(
            "Name of the individual being recognized on the certificate .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature_line_1: str = Field(
        default="",
        description=(
            "First certificate signature line (e.g., national or council officer) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    signature_line_2: str = Field(
        default="",
        description=(
            "Second certificate signature line (e.g., national or council officer) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    signature_line_3: str = Field(
        default="",
        description=(
            "Third certificate signature line (e.g., national or council officer) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ScoutmasterAwardOfMeritNomination(BaseModel):
    """
    SCOUTMASTER AWARD OF MERIT NOMINATION

    Submit to your local council service center.
    """

    nominee_information: NomineeInformation = Field(..., description="Nominee Information")
    unit_and_training_history: UnitandTrainingHistory = Field(
        ..., description="Unit and Training History"
    )
    nomination_and_council_approval: NominationandCouncilApproval = Field(
        ..., description="Nomination and Council Approval"
    )
    award_certificate: AwardCertificate = Field(..., description="Award Certificate")
