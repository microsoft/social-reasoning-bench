from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class IncidentDetails(BaseModel):
    """Date, time, location, train, and operating conditions at the time of the incident"""

    date_of_incident: str = Field(
        ..., description="Calendar date when the incident occurred"
    )  # YYYY-MM-DD format

    time_of_incident: str = Field(
        ...,
        description=(
            'Clock time when the incident occurred .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    railroad_mile_post_or_station_facility: str = Field(
        ...,
        description=(
            "Specific railroad mile post or station facility where the incident occurred "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    train_number: str = Field(
        ...,
        description=(
            "Identifier or number of the train involved in the incident .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    railroad_crossing_street: str = Field(
        default="",
        description=(
            "Name of the street at the railroad crossing involved, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    weather_conditions: str = Field(
        default="",
        description=(
            "Weather conditions at the time of the incident (e.g., clear, rain, snow) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    consist_locomotive_car_number: str = Field(
        default="",
        description=(
            "Description of the train consist, including locomotive and car numbers .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    condition_and_number_of_equipment_if_involved: str = Field(
        default="",
        description=(
            "Condition and number of any equipment involved in the incident .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    conductors: str = Field(
        default="",
        description=(
            "Name(s) of the conductor(s) involved or on duty .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    engineer: str = Field(
        default="",
        description=(
            "Name of the engineer involved or on duty .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ClaimantInformation(BaseModel):
    """Contact information for the person making the claim"""

    claimants_name_adress: str = Field(
        ...,
        description=(
            "Full name and mailing address of the claimant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number: str = Field(
        ...,
        description=(
            "Primary phone number for contacting the claimant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ClaimDescription(BaseModel):
    """Description of how the incident occurred, type of claim, and resulting injury or damage"""

    incident_description_fault: str = Field(
        ...,
        description=(
            "Detailed description of how the incident occurred and why you believe the "
            'State Agency is responsible .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    bodily_injury: BooleanLike = Field(
        ..., description="Indicate if this claim is for bodily injury"
    )

    property_damage: BooleanLike = Field(
        ..., description="Indicate if this claim is for property damage"
    )

    injury_or_damage_description: str = Field(
        ...,
        description=(
            "Description of the injuries sustained or property damage incurred .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Signature(BaseModel):
    """Signature of the claimant or lawful representative"""

    signature_of_claimant_or_lawful_representative: str = Field(
        ...,
        description=(
            "Signature of the claimant or their lawful representative .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class NewMexicoRailRunnerTortNoticeOfClaim(BaseModel):
    """
        New Mexico Rail Runner
    TORT NOTICE OF CLAIM

        Every person who claims damage or injuries from the state under the Tort Claim Act [41-4-1 to 41-4-27 NMSA 1978] shall cause to be presented to the Risk Management Division for claims against the state within ninety days after the occurrence giving rise to claim for which immunity has been waiver under the Tort Claims Act, a written notice stating the time, place and circumstance of loss of injury.
    """

    incident_details: IncidentDetails = Field(..., description="Incident Details")
    claimant_information: ClaimantInformation = Field(..., description="Claimant Information")
    claim_description: ClaimDescription = Field(..., description="Claim Description")
    signature: Signature = Field(..., description="Signature")
