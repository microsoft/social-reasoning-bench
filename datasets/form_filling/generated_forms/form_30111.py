from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
    """Information about the applicant and their Scouting registration at the time of the action"""

    applicant_name: str = Field(
        ...,
        description=(
            'Applicant\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    applicant_age_at_time_of_action: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Applicant's age at the time of the action"
    )

    applicant_approximate_height: str = Field(
        default="",
        description=(
            "Applicant's approximate height (include units, e.g., feet/inches) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    applicant_approximate_weight: str = Field(
        default="",
        description=(
            "Applicant's approximate weight (include units, e.g., pounds) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    parents_name: str = Field(
        default="",
        description=(
            'Parent or guardian\'s full name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    applicant_phone_no: str = Field(
        ...,
        description=(
            "Applicant or parent/guardian phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    home_address: str = Field(
        ...,
        description=(
            'Applicant\'s street address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    applicant_city: str = Field(
        ...,
        description=(
            'City of applicant\'s home address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    applicant_state: str = Field(..., description="State or territory of applicant's home address")

    applicant_zip_code: str = Field(
        ..., description="ZIP or postal code of applicant's home address"
    )

    tiger_cub: BooleanLike = Field(
        default="", description="Check if the candidate is registered as a Tiger Cub"
    )

    cub_scout: BooleanLike = Field(
        default="", description="Check if the candidate is registered as a Cub Scout"
    )

    webelos_scout: BooleanLike = Field(
        default="", description="Check if the candidate is registered as a Webelos Scout"
    )

    boy_scout: BooleanLike = Field(
        default="", description="Check if the candidate is registered as a Boy Scout"
    )

    varsity_scout: BooleanLike = Field(
        default="", description="Check if the candidate is registered as a Varsity Scout"
    )

    venturer: BooleanLike = Field(
        default="", description="Check if the candidate is registered as a Venturer"
    )

    adult: BooleanLike = Field(
        default="", description="Check if the candidate is registered as an adult"
    )

    pack_number: str = Field(
        default="",
        description=(
            "Pack number if the candidate is registered in a Pack .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    troop_number: str = Field(
        default="",
        description=(
            "Troop number if the candidate is registered in a Troop .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    team_number: str = Field(
        default="",
        description=(
            "Team number if the candidate is registered in a Team .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    crew_number: str = Field(
        default="",
        description=(
            "Crew number if the candidate is registered in a Crew .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ship_number: str = Field(
        default="",
        description=(
            "Ship number if the candidate is registered in a Ship .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    rank_at_time_of_action: str = Field(
        default="",
        description=(
            "Scout rank held by the candidate at the time of the action .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    present_office_if_adult: str = Field(
        default="",
        description=(
            "Current Scouting position if the candidate is an adult .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class RescuedPersonInformation(BaseModel):
    """Details about the person who was rescued"""

    rescued_person_name: str = Field(
        ...,
        description=(
            'Rescued person\'s full name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    rescued_person_phone_no: str = Field(
        default="",
        description=(
            'Rescued person\'s phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    rescued_person_address: str = Field(
        default="",
        description=(
            'Rescued person\'s street address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    rescued_person_city: str = Field(
        default="",
        description=(
            'City of rescued person\'s address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    rescued_person_state: str = Field(
        default="", description="State or territory of rescued person's address"
    )

    rescued_person_zip_code: str = Field(
        default="", description="ZIP or postal code of rescued person's address"
    )

    rescued_person_age_at_time_of_action: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Rescued person's age at the time of the action"
    )

    rescued_person_approximate_height: str = Field(
        default="",
        description=(
            "Rescued person's approximate height (include units, e.g., feet/inches) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    rescued_person_approximate_weight: str = Field(
        default="",
        description=(
            "Rescued person's approximate weight (include units, e.g., pounds) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    place_where_action_occurred: str = Field(
        ...,
        description=(
            "Name and location of the place where the incident or action occurred .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_of_incident: str = Field(
        ..., description="Calendar date when the incident occurred"
    )  # YYYY-MM-DD format

    time_of_incident: str = Field(
        ...,
        description=(
            "Time of day when the incident occurred .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class SummaryandCertification(BaseModel):
    """Summary of the action and council committee certification"""

    summary_of_the_action: str = Field(
        ...,
        description=(
            "Short summary describing the incident or action based on the council "
            'committee’s study and interviews .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    council_committee_chairs_signature: str = Field(
        ...,
        description=(
            "Signature of the council committee chair .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    council_committee_signature_date: str = Field(
        ..., description="Date the council committee chair signed the form"
    )  # YYYY-MM-DD format


class ApplicantInformation(BaseModel):
    """
    Applicant Information

    A short summary describing the incident or action is required based on the council committee’s study of all aspects of the case and on interviews with the principals and witnesses.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    rescued_person_information: RescuedPersonInformation = Field(
        ..., description="Rescued Person Information"
    )
    summary_and_certification: SummaryandCertification = Field(
        ..., description="Summary and Certification"
    )
