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
    """Basic details about the incident and report"""

    facility_location: str = Field(
        ...,
        description=(
            "Name or description of the facility or location where the incident occurred "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    date_of_incident: str = Field(
        ..., description="Calendar date when the incident occurred"
    )  # YYYY-MM-DD format

    time_of_incident: str = Field(
        ...,
        description=(
            "Time of day when the incident occurred, including am or pm .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    report_prepared_by: str = Field(
        ...,
        description=(
            "Full name of the person completing this incident report .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    title: str = Field(
        ...,
        description=(
            "Job title or role of the person preparing the report .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature: str = Field(
        ...,
        description=(
            "Signature of the person preparing the report .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_report_prepared: str = Field(
        ..., description="Date on which this report was completed"
    )  # YYYY-MM-DD format

    program_name: str = Field(
        default="",
        description=(
            "Name of the program or activity associated with the incident .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class InjuredPartyInformation(BaseModel):
    """Details about the injured person"""

    injured_party_first_name: str = Field(
        ...,
        description=(
            'First name of the injured person .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    injured_party_last_name: str = Field(
        ...,
        description=(
            'Last name of the injured person .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    injured_party_age: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Age of the injured person in years"
    )

    injured_party_sex: Literal["M", "F", "N/A", ""] = Field(
        ..., description="Sex of the injured person"
    )

    injured_party_address: str = Field(
        ...,
        description=(
            'Mailing address of the injured person .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    injured_party_postal_code: str = Field(
        ..., description="Postal or ZIP code for the injured person's address"
    )

    injured_party_home_phone: str = Field(
        default="",
        description=(
            "Home telephone number of the injured person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    injured_party_work_phone: str = Field(
        default="",
        description=(
            "Work telephone number of the injured person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    injured_party_work_phone_ext: str = Field(
        default="",
        description=(
            "Telephone extension for the injured person's work phone, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    injured_party_cell_phone: str = Field(
        default="",
        description=(
            "Cell/mobile phone number of the injured person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    injured_party_email: str = Field(
        default="",
        description=(
            'Email address of the injured person .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class WitnessInformation(BaseModel):
    """Details about the witness"""

    witness_first_name: str = Field(
        default="",
        description=(
            'First name of the witness .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    witness_last_name: str = Field(
        default="",
        description=(
            'Last name of the witness .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    witness_age: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age of the witness in years"
    )

    witness_sex: Literal["M", "F", "N/A", ""] = Field(default="", description="Sex of the witness")

    witness_address: str = Field(
        default="",
        description=(
            'Mailing address of the witness .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    witness_postal_code: str = Field(
        default="", description="Postal or ZIP code for the witness's address"
    )

    witness_home_phone: str = Field(
        default="",
        description=(
            'Home telephone number of the witness .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    witness_work_phone: str = Field(
        default="",
        description=(
            'Work telephone number of the witness .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    witness_work_phone_ext: str = Field(
        default="",
        description=(
            "Telephone extension for the witness's work phone, if applicable .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    witness_cell_phone: str = Field(
        default="",
        description=(
            "Cell/mobile phone number of the witness .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    witness_email: str = Field(
        default="",
        description=(
            'Email address of the witness .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class DescriptionofIncident(BaseModel):
    """Information about how the incident description is provided"""

    more_paper_attached: BooleanLike = Field(
        default="", description="Indicate if additional sheets with incident details are attached"
    )

    complete_report_below_on_this_sheet_only: BooleanLike = Field(
        default="",
        description="Indicate if the full incident description is contained only on this sheet",
    )

    continued_on_back: BooleanLike = Field(
        default="",
        description="Indicate if the incident description continues on the back of this form",
    )


class ChecklistForIncidentReport(BaseModel):
    """
    Checklist for Incident Report

    Provide a detailed and factual description of the incident which resulted in the injury. Do not include assumptions or your opinion on what may have happened. Only state the facts. Use more paper if required. Ensure you note below if additional information sheets have been attached, noting the date and time and injured party’s name at the top of the sheet in case they become separated.
    """

    incident_details: IncidentDetails = Field(..., description="Incident Details")
    injured_party_information: InjuredPartyInformation = Field(
        ..., description="Injured Party Information"
    )
    witness_information: WitnessInformation = Field(..., description="Witness Information")
    description_of_incident: DescriptionofIncident = Field(
        ..., description="Description of Incident"
    )
