from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AbouttheTraveler(BaseModel):
    """Basic personal and passport information about the traveler"""

    todays_date: str = Field(..., description="Today's date")  # YYYY-MM-DD format

    complete_name_exactly_as_it_appears_in_your_passport: str = Field(
        ...,
        description=(
            "Traveler's full legal name exactly as it appears in the passport .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Traveler's date of birth")  # YYYY-MM-DD format

    name: str = Field(
        default="",
        description=(
            "Preferred name or additional name if different from passport name .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    passport_number: str = Field(
        ...,
        description=(
            'Traveler\'s passport number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    expiration_date: str = Field(..., description="Passport expiration date")  # YYYY-MM-DD format

    country_of_issue: str = Field(
        ...,
        description=(
            'Country that issued the passport .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ContactInformation(BaseModel):
    """Traveler’s address and contact details"""

    address: str = Field(
        ...,
        description=(
            'Street address of the traveler .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city_state: str = Field(
        ...,
        description=(
            "City and state of the traveler's address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    zip: str = Field(..., description="ZIP or postal code")

    home_phone: str = Field(
        default="",
        description=(
            'Home phone number including area code .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        ...,
        description=(
            "Mobile/cell phone number including area code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Traveler\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    what_parish_group_do_you_belong_to: str = Field(
        default="",
        description=(
            "Name of your parish or group affiliation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    how_did_you_hear_about_us: str = Field(
        default="",
        description=(
            "Describe how you learned about this pilgrimage .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class HealthInsurance(BaseModel):
    """Health insurance subscriber information"""

    subscribers_name: str = Field(
        default="",
        description=(
            "Name of the health insurance subscriber .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class TravelPreferences(BaseModel):
    """Preferred travel dates, package type, and companions"""

    interested_travel_jun_24_to_jul_5: BooleanLike = Field(
        default="", description="Check if you wish to travel on the Jun. 24th to Jul. 5th dates"
    )

    interested_travel_sep_16_to_sep_27: BooleanLike = Field(
        default="", description="Check if you wish to travel on the Sep. 16th to Sep. 27th dates"
    )

    full_package: BooleanLike = Field(
        default="", description="Select if you want the full travel package"
    )

    land_package: BooleanLike = Field(
        default="", description="Select if you want the land-only package (no airfare)"
    )

    list_any_travel_companions: str = Field(
        default="",
        description=(
            "Names and relationship of any travel companions .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ApplicationType(BaseModel):
    """Type of pilgrimage or volunteer role being applied for"""

    special_needs_pilgrim: BooleanLike = Field(
        default="", description="Select if you are applying as a special needs pilgrim"
    )

    pilgrim: BooleanLike = Field(
        default="", description="Select if you are applying as a regular pilgrim"
    )

    volunteer: BooleanLike = Field(
        default="", description="Select if you are applying as a volunteer"
    )

    stagiaire_18_to_65_years_old: BooleanLike = Field(
        default="", description="Select if you are applying as a stagiaire (ages 18 to 65)"
    )

    hdm_adult: BooleanLike = Field(
        default="", description="Select if you are applying as an HDM Adult"
    )

    hdm_youth_young_adult: BooleanLike = Field(
        default="", description="Select if you are applying as HDM Youth or Young Adult"
    )

    hdm_medical: BooleanLike = Field(
        default="", description="Select if you are applying as HDM Medical staff"
    )


class Languages(BaseModel):
    """Languages spoken fluently by the traveler"""

    english: BooleanLike = Field(default="", description="Check if you speak English fluently")

    spanish: BooleanLike = Field(default="", description="Check if you speak Spanish fluently")

    french: BooleanLike = Field(default="", description="Check if you speak French fluently")

    other_languages_you_speak_fluently: str = Field(
        default="",
        description=(
            "List any other languages you speak fluently .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class EmergencyContact(BaseModel):
    """Emergency contact information for a person not traveling"""

    emergency_contact_name: str = Field(
        ...,
        description=(
            "Name of emergency contact who is not traveling with you .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_relationship: str = Field(
        ...,
        description=(
            "Relationship of the emergency contact to you .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_phone: str = Field(
        ...,
        description=(
            'Phone number of the emergency contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class SanctuaryServiceInformation(BaseModel):
    """Information for those serving at the Sanctuary, including service preferences"""

    if_serving_the_sanctuary: BooleanLike = Field(
        default="", description="Indicate if you will be serving at the Sanctuary"
    )

    year_of_stagiaire: str = Field(
        default="",
        description=(
            "Specify which year of Stagiaire service you will be doing .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    service_preference: str = Field(
        default="",
        description=(
            "Describe or select the service you would like to sign up for at the Sanctuary "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    service_women_st_john_baptist_baths: BooleanLike = Field(
        default="",
        description="Select if, as a woman, you wish to serve in St. John the Baptist (Baths)",
    )

    service_women_notre_dame_reception_assisting_sick: BooleanLike = Field(
        default="",
        description=(
            "Select if, as a woman, you wish to serve in Notre-Dame (Reception & Assisting "
            "the Sick)"
        ),
    )

    service_men_st_joseph: BooleanLike = Field(
        default="", description="Select if, as a man, you wish to serve in St. Joseph"
    )


class TrainingandBackground(BaseModel):
    """VIRTUS training and background check status"""

    virtus_training_yes: BooleanLike = Field(
        default="", description="Check if you have completed VIRTUS training"
    )

    virtus_training_date: str = Field(
        default="", description="Date you completed VIRTUS training"
    )  # YYYY-MM-DD format

    virtus_training_no: BooleanLike = Field(
        default="", description="Check if you have not completed VIRTUS training"
    )

    background_check_yes: BooleanLike = Field(
        default="", description="Check if you have completed a background check"
    )

    background_check_date: str = Field(
        default="", description="Date your background check was completed"
    )  # YYYY-MM-DD format

    background_check_no: BooleanLike = Field(
        default="", description="Check if you have not completed a background check"
    )


class MedicalInformation(BaseModel):
    """Medical field status and occupation"""

    medical_field_yes: BooleanLike = Field(
        default="", description="Check if you work in the medical field"
    )

    occupation: str = Field(
        default="",
        description=(
            "Your occupation if you are in the medical field .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    medical_field_no: BooleanLike = Field(
        default="", description="Check if you are not in the medical field"
    )


class thAnnualArchdioceseOfMiamiPilgrimageToLourdes5(BaseModel):
    """
    5th Annual Archdiocese of Miami Pilgrimage to Lourdes

    ''
    """

    about_the_traveler: AbouttheTraveler = Field(..., description="About the Traveler")
    contact_information: ContactInformation = Field(..., description="Contact Information")
    health_insurance: HealthInsurance = Field(..., description="Health Insurance")
    travel_preferences: TravelPreferences = Field(..., description="Travel Preferences")
    application_type: ApplicationType = Field(..., description="Application Type")
    languages: Languages = Field(..., description="Languages")
    emergency_contact: EmergencyContact = Field(..., description="Emergency Contact")
    sanctuary_service_information: SanctuaryServiceInformation = Field(
        ..., description="Sanctuary Service Information"
    )
    training_and_background: TrainingandBackground = Field(
        ..., description="Training and Background"
    )
    medical_information: MedicalInformation = Field(..., description="Medical Information")
