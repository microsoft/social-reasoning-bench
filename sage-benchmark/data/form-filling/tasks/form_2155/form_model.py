from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class VolunteerPlacementAvailability(BaseModel):
    """Activity/location preference and when you are available to volunteer"""

    name_of_activity_or_location_you_wish_to_volunteer: str = Field(
        ...,
        description=(
            "Specific activity or facility where you wish to volunteer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    availability_mornings: BooleanLike = Field(
        default="", description="Check if you are available to volunteer in the mornings"
    )

    availability_afternoons: BooleanLike = Field(
        default="", description="Check if you are available to volunteer in the afternoons"
    )

    availability_evenings: BooleanLike = Field(
        default="", description="Check if you are available to volunteer in the evenings"
    )

    availability_monday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer on Mondays"
    )

    availability_tuesday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer on Tuesdays"
    )

    availability_wednesday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer on Wednesdays"
    )

    availability_thursday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer on Thursdays"
    )

    availability_friday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer on Fridays"
    )

    availability_saturday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer on Saturdays"
    )

    availability_sunday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer on Sundays"
    )


class PersonalContactInformation(BaseModel):
    """Basic personal details and contact information"""

    name_first: str = Field(
        ...,
        description=(
            'First name .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    name_middle: str = Field(
        default="",
        description=(
            'Middle name .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    name_last: str = Field(
        ...,
        description=(
            'Last name .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Primary phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Email address .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    current_address_street_address: str = Field(
        ...,
        description=(
            'Current street address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    current_address_city: str = Field(
        ...,
        description=(
            'Current city .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    current_address_state: str = Field(..., description="Current state")

    current_address_zip: str = Field(..., description="Current ZIP code")

    previous_address_street_address: str = Field(
        default="",
        description=(
            "Previous street address if less than 5 years at current address .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    previous_address_city: str = Field(
        default="",
        description=(
            'Previous city .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    previous_address_state: str = Field(default="", description="Previous state")

    previous_address_zip: str = Field(default="", description="Previous ZIP code")

    emergency_contact: str = Field(
        ...,
        description=(
            'Name of emergency contact person .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_phone: str = Field(
        ...,
        description=(
            'Phone number of emergency contact .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class DriversLicenseInformation(BaseModel):
    """Driver’s license status and details"""

    do_you_have_a_drivers_license_yes: BooleanLike = Field(
        ..., description="Indicate yes if you have a valid driver's license"
    )

    do_you_have_a_drivers_license_no: BooleanLike = Field(
        ..., description="Indicate no if you do not have a valid driver's license"
    )

    license_number: str = Field(
        ...,
        description=(
            'Driver\'s license number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    class_: str = Field(
        ...,
        description=(
            'Class of driver\'s license .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    issuing_state: str = Field(..., description="State that issued the driver's license")

    expiration_date: str = Field(
        ..., description="Driver's license expiration date"
    )  # YYYY-MM-DD format


class CriminalHistory(BaseModel):
    """Disclosure of felony or misdemeanor convictions"""

    have_you_ever_been_convicted_of_a_felony_yes: BooleanLike = Field(
        ..., description="Indicate yes if you have ever been convicted of a felony"
    )

    have_you_ever_been_convicted_of_a_felony_no: BooleanLike = Field(
        ..., description="Indicate no if you have never been convicted of a felony"
    )

    have_you_ever_been_convicted_of_a_misdemeanor_yes: BooleanLike = Field(
        ..., description="Indicate yes if you have ever been convicted of a misdemeanor"
    )

    have_you_ever_been_convicted_of_a_misdemeanor_no: BooleanLike = Field(
        ..., description="Indicate no if you have never been convicted of a misdemeanor"
    )

    if_yes_nature_and_disposition_of_the_case_line_1: str = Field(
        default="",
        description=(
            "Description of the nature and disposition of the case (first line) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    if_yes_nature_and_disposition_of_the_case_line_2: str = Field(
        default="",
        description=(
            "Description of the nature and disposition of the case (second line) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Education(BaseModel):
    """High school, GED, and education beyond high school"""

    high_school: str = Field(
        default="",
        description=(
            'Name of high school attended .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    high_school_location: str = Field(
        default="",
        description=(
            'City and state of high school .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    high_school_years_attended: str = Field(
        default="",
        description=(
            'Years attended high school .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    high_school_did_you_graduate: str = Field(
        default="",
        description=(
            "Indicate if you graduated from high school .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ged_state_and_date_of_issuance: str = Field(
        default="",
        description=(
            "State and date of GED issuance, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    college_or_university_name_location: str = Field(
        default="",
        description=(
            "Name and location of the college or university .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    college_or_university_years_attended_from_to: str = Field(
        default="",
        description=(
            "Years attended at the college or university (from–to) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_or_university_number_of_years_attended: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of years attended at the college or university"
    )

    college_or_university_degree_or_certificate_received_if_any: str = Field(
        default="",
        description=(
            "Degree or certificate received from the college or university, if any .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    college_or_university_major_subject: str = Field(
        default="",
        description=(
            "Major subject studied at the college or university .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    graduate_or_professional_school_name_location: str = Field(
        default="",
        description=(
            "Name and location of the graduate or professional school .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    graduate_or_professional_school_years_attended_from_to: str = Field(
        default="",
        description=(
            "Years attended at the graduate or professional school (from–to) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    graduate_or_professional_school_number_of_years_attended: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Total number of years attended at the graduate or professional school",
        )
    )

    graduate_or_professional_school_degree_or_certificate_received_if_any: str = Field(
        default="",
        description=(
            "Degree or certificate received from the graduate or professional school, if "
            'any .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    graduate_or_professional_school_major_subject: str = Field(
        default="",
        description=(
            "Major subject studied at the graduate or professional school .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    technical_or_business_school_name_location: str = Field(
        default="",
        description=(
            "Name and location of the technical or business school .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    technical_or_business_school_years_attended_from_to: str = Field(
        default="",
        description=(
            "Years attended at the technical or business school (from–to) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    technical_or_business_school_number_of_years_attended: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of years attended at the technical or business school"
    )

    technical_or_business_school_degree_or_certificate_received_if_any: str = Field(
        default="",
        description=(
            "Degree or certificate received from the technical or business school, if any "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    technical_or_business_school_major_subject: str = Field(
        default="",
        description=(
            "Major subject studied at the technical or business school .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    certifications_name_location: str = Field(
        default="",
        description=(
            "Name and location related to certifications .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    certifications_years_attended_from_to: str = Field(
        default="",
        description=(
            "Years attended or active for certifications (from–to) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    certifications_number_of_years_attended: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of years related to certifications"
    )

    certifications_degree_or_certificate_received_if_any: str = Field(
        default="",
        description=(
            "Degree or certificate received related to certifications, if any .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    certifications_major_subject: str = Field(
        default="",
        description=(
            "Major subject or focus area of certifications .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    military_name_location: str = Field(
        default="",
        description=(
            "Name and location of military service or school .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    military_years_attended_from_to: str = Field(
        default="",
        description=(
            "Years of military service or attendance (from–to) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    military_number_of_years_attended: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of years of military service or attendance"
    )

    military_degree_or_certificate_received_if_any: str = Field(
        default="",
        description=(
            "Degree, certificate, or qualification received from military service, if any "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    military_major_subject: str = Field(
        default="",
        description=(
            "Major subject or specialty in the military .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class HighPointParksRecreationVolunteerApplicationForm(BaseModel):
    """
        High Point Parks & Recreation
    Volunteer Application Form

        ''
    """

    volunteer_placement__availability: VolunteerPlacementAvailability = Field(
        ..., description="Volunteer Placement & Availability"
    )
    personal__contact_information: PersonalContactInformation = Field(
        ..., description="Personal & Contact Information"
    )
    drivers_license_information: DriversLicenseInformation = Field(
        ..., description="Driver’s License Information"
    )
    criminal_history: CriminalHistory = Field(..., description="Criminal History")
    education: Education = Field(..., description="Education")
