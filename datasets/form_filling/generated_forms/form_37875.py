from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EmergencyServices(BaseModel):
    """Details about emergency services involvement and reports"""

    field_911_called: str = Field(
        default="",
        description=(
            "Time 911 was called, including am or pm .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ems_arrived: str = Field(
        default="",
        description=(
            'Time EMS arrived, including am or pm .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    fire_department: BooleanLike = Field(
        default="", description="Check if the Fire Department was involved"
    )

    police: BooleanLike = Field(default="", description="Check if the Police were involved")

    ambulance: BooleanLike = Field(
        default="", description="Check if an ambulance service was involved"
    )

    fire_department_report: str = Field(
        default="",
        description=(
            "Fire Department report or incident number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    police_occurrence: str = Field(
        default="",
        description=(
            'Police occurrence or case number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    ambulance_report: str = Field(
        default="",
        description=(
            'Ambulance report number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class FirstAidTreatment(BaseModel):
    """First aid provided prior to arrival of emergency services"""

    specific_first_aid_treatment_provided_prior_to_the_arrival_of_the_emergency_services: str = (
        Field(
            default="",
            description=(
                "Detailed description of first aid treatment provided before emergency services "
                'arrived .If you cannot fill this, write "N/A". If this field should not be '
                "filled by you (for example, it belongs to another person or office), leave it "
                'blank (empty string "").'
            ),
        )
    )

    medical_identification_tags: str = Field(
        default="",
        description=(
            "Details of any medical identification tags observed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    names_of_person_who_provided_first_aid: str = Field(
        default="",
        description=(
            "Names of all individuals who provided first aid .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    treatment_provided: str = Field(
        default="",
        description=(
            "Description of treatment provided, including any use of an AED .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    aed_used: BooleanLike = Field(
        default="", description="Indicate whether an AED was used as part of the treatment"
    )

    person_who_used_aed: str = Field(
        default="",
        description=(
            "Name of the person who operated the AED, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class NextOfKin(BaseModel):
    """Notification and contact details for next of kin"""

    were_next_of_kin_notified: BooleanLike = Field(
        default="", description="Indicate whether next of kin were notified"
    )

    yes_next_of_kin_notified: BooleanLike = Field(
        default="", description="Check if next of kin were notified"
    )

    no_next_of_kin_notified: BooleanLike = Field(
        default="", description="Check if next of kin were not notified"
    )

    name_next_of_kin: str = Field(
        default="",
        description=(
            'Name of the next of kin .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    relationship_next_of_kin: str = Field(
        default="",
        description=(
            "Relationship of the next of kin to the injured party .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_next_of_kin: str = Field(
        default="",
        description=(
            'Telephone number of the next of kin .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class InjuredPartyActionTaken(BaseModel):
    """Disposition of the injured party and transport details"""

    injured_party_taken_home: BooleanLike = Field(
        default="", description="Check if the injured party was taken or sent home"
    )

    injured_party_taken_hospital: BooleanLike = Field(
        default="", description="Check if the injured party was taken or sent to a hospital"
    )

    injured_party_taken_clinic: BooleanLike = Field(
        default="", description="Check if the injured party was taken or sent to a clinic"
    )

    injured_party_refused_treatment: BooleanLike = Field(
        default="", description="Check if the injured party refused treatment"
    )

    other_please_specify: str = Field(
        default="",
        description=(
            "If destination is other than listed, specify where the injured party was taken "
            'or sent .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    taken_by_name_of_person: str = Field(
        default="",
        description=(
            "Name of the person who took or accompanied the injured party .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    phone_person_who_took_injured_party: str = Field(
        default="",
        description=(
            "Phone number of the person who took or accompanied the injured party .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    taken_to_identify_location: str = Field(
        default="",
        description=(
            "Location or facility where the injured party was taken .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    transported_how: str = Field(
        default="",
        description=(
            "Mode of transportation used (e.g., ambulance, car) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    report_submitted_to: str = Field(
        default="",
        description=(
            "Name or office to whom the report was submitted .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_submitted_month_day_year: str = Field(
        default="", description="Date the report was submitted"
    )  # YYYY-MM-DD format


class EmergencyServices(BaseModel):
    """
    Emergency Services

    Please note that we are collecting the personal information contained in this incident report for the purpose of documenting the alleged incident or event in the event that any medical or legal issue(s), claim(s), and/or action(s) arise therefrom, and that, by providing your personal information, you are consenting, to the extent that your consent is required by law, to the collection, use, and disclosure of your personal information for such purpose.
    """

    emergency_services: EmergencyServices = Field(..., description="Emergency Services")
    first_aid_treatment: FirstAidTreatment = Field(..., description="First Aid Treatment")
    next_of_kin: NextOfKin = Field(..., description="Next Of Kin")
    injured_party_action_taken: InjuredPartyActionTaken = Field(
        ..., description="Injured Party Action Taken"
    )
