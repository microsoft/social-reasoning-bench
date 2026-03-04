from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ParticipantInformation(BaseModel):
    """Personal contact details of the participant"""

    surname_first_name: str = Field(
        ...,
        description=(
            'Participant\'s surname and first name .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Participant\'s mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Participant\'s phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            'Participant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class ParticipationType(BaseModel):
    """Whether the participant is active or a passive listener"""

    active: BooleanLike = Field(..., description="Select if registering as an active participant")

    passive_listener: BooleanLike = Field(
        ..., description="Select if registering as a passive/listener participant"
    )


class CourseGroupSelection(BaseModel):
    """Selection of preferred study group(s)"""

    group_1_german_baroque_and_romantic_espinasse_gehring: BooleanLike = Field(
        default="",
        description="Check if you wish to register for Group 1: German Baroque and Romantic",
    )

    group_2_french_music_17th_18th_century_espinasse_simon: BooleanLike = Field(
        default="",
        description="Check if you wish to register for Group 2: French music 17th/18th century",
    )

    group_3_symphonic_modern_dubois_marle_ouvrard: BooleanLike = Field(
        default="", description="Check if you wish to register for Group 3: Symphonic - Modern"
    )

    group_4_improvisation_dubois_marle_ouvrard: BooleanLike = Field(
        default="", description="Check if you wish to register for Group 4: Improvisation"
    )

    group_5_harpsichord_clavichord_zylberjch_mondesert: BooleanLike = Field(
        default="",
        description="Check if you wish to register for Group 5: Harpsichord / Clavichord",
    )


class Repertoire(BaseModel):
    """Participant's repertoire information"""

    my_repertoire: str = Field(
        default="",
        description=(
            "List the repertoire you intend to work on during the academy .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class RegistrationForTheInternationalOrganAcademyStrasbourgAios2021(BaseModel):
    """Registration for the International Organ
    Academy Strasbourg AIOS 2021"""

    participant_information: ParticipantInformation = Field(
        ..., description="Participant Information"
    )
    participation_type: ParticipationType = Field(..., description="Participation Type")
    course_group_selection: CourseGroupSelection = Field(..., description="Course Group Selection")
    repertoire: Repertoire = Field(..., description="Repertoire")
