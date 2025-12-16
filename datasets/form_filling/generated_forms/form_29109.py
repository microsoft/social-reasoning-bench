from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class SchoolLevelRow(BaseModel):
    """Single row in School Level"""

    school_level: str = Field(default="", description="School_Level")
    names_and_location_of_school_attended: str = Field(
        default="", description="Names_And_Location_Of_School_Attended"
    )
    graduated: str = Field(default="", description="Graduated")
    major_subject_degree_received: str = Field(
        default="", description="Major_Subject_Degree_Received"
    )


class PositionAppliedFor(BaseModel):
    """Job or position the applicant is applying for"""

    employment_application_for: str = Field(
        ...,
        description=(
            "Title of the position for which you are applying .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PersonalInformation(BaseModel):
    """Basic personal and contact details"""

    name_last_first_middle: str = Field(
        ...,
        description=(
            'Full legal name (last, first, middle) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    drivers_license_state_number: str = Field(
        ...,
        description=(
            'Driver’s license state and number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address_street_address: str = Field(
        ...,
        description=(
            "Street address of your current residence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_state_zip: str = Field(
        ...,
        description=(
            "City, state, and ZIP code for your address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    home_telephone_number: str = Field(
        ...,
        description=(
            'Primary home telephone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    alternate_phone_number: str = Field(
        default="",
        description=(
            'Alternate or mobile phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
        ...,
        description=(
            "Email address where you can be contacted .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class EligibilityandEmploymentHistoryQuestions(BaseModel):
    """Job-related eligibility, prior employment with HWMA, and work history questions"""

    capable_of_performing_essential_job_duties: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you can satisfactorily perform the essential duties of the "
            "job, with or without reasonable accommodation"
        ),
    )

    capable_of_performing_essential_job_duties_no: BooleanLike = Field(
        default="",
        description="Represents a 'No' response to being able to perform essential job duties",
    )

    over_18_proof_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you can provide proof that you are over 18 years of age if hired"
        ),
    )

    over_18_proof_no: BooleanLike = Field(
        default="",
        description="Represents a 'No' response to being able to furnish proof of being over 18",
    )

    previously_worked_for_hwma_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you have previously been employed by Humboldt Waste "
            "Management Authority"
        ),
    )

    previously_worked_for_hwma_no: BooleanLike = Field(
        default="",
        description=(
            "Represents a 'No' response to prior employment with Humboldt Waste Management "
            "Authority"
        ),
    )

    employment_gaps_yes: BooleanLike = Field(
        ..., description="Indicate whether there are gaps in your employment history"
    )

    employment_gaps_no: BooleanLike = Field(
        default="", description="Represents a 'No' response to having gaps in employment history"
    )

    ever_discharged_or_forced_to_resign_yes: BooleanLike = Field(
        ...,
        description="Indicate whether you have ever been discharged or forced to resign from a job",
    )

    ever_discharged_or_forced_to_resign_no: BooleanLike = Field(
        default="",
        description="Represents a 'No' response to having been discharged or forced to resign",
    )

    days_missed_2018: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Number of work days missed in 2018 for reasons other than paid holidays and vacation"
        ),
    )

    days_missed_2019: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Number of work days missed in 2019 for reasons other than paid holidays and vacation"
        ),
    )

    days_missed_2020: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Number of work days missed in 2020 for reasons other than paid holidays and vacation"
        ),
    )

    adequate_transportation_yes: BooleanLike = Field(
        ..., description="Indicate whether you have adequate transportation to and from work"
    )

    adequate_transportation_no: BooleanLike = Field(
        default="", description="Represents a 'No' response to having adequate transportation"
    )

    valid_drivers_license_yes: BooleanLike = Field(
        ..., description="Indicate whether you currently have a valid driver’s license"
    )

    valid_drivers_license_no: BooleanLike = Field(
        default="", description="Represents a 'No' response to having a valid driver’s license"
    )

    prevented_from_lawful_employment_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether visa or immigration status prevents you from lawful "
            "employment in this country"
        ),
    )

    prevented_from_lawful_employment_no: BooleanLike = Field(
        default="",
        description=(
            "Represents a 'No' response to being prevented from lawful employment due to "
            "visa or immigration status"
        ),
    )

    explanation_of_above_questions: str = Field(
        default="",
        description=(
            "Space to provide explanations or additional details for any of the above "
            'questions .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class Education(BaseModel):
    """Educational background including high school, college, and other schooling"""

    school_level: List[SchoolLevelRow] = Field(
        default="",
        description=(
            "Education history including school level, school name and location, graduation "
            "status, and major/degree"
        ),
    )  # List of table rows

    names_and_location_of_school_attended: str = Field(
        default="",
        description=(
            "Name and location of the educational institution attended .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    graduated: BooleanLike = Field(
        default="", description="Indicate whether you graduated from the listed school"
    )

    major_subject_degree_received: str = Field(
        default="",
        description=(
            "Major field of study and/or degree received .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    high_school_names_and_location: str = Field(
        ...,
        description=(
            "Name and location of the high school attended .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    high_school_graduated_yes: BooleanLike = Field(
        default="", description="Indicates a 'Yes' response for graduating from high school"
    )

    high_school_graduated_no: BooleanLike = Field(
        default="", description="Indicates a 'No' response for graduating from high school"
    )

    high_school_major_subject_degree: str = Field(
        default="",
        description=(
            "Major subject or diploma information for high school .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_names_and_location: str = Field(
        default="",
        description=(
            "Name and location of the college attended .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    college_graduated_yes: BooleanLike = Field(
        default="", description="Indicates a 'Yes' response for graduating from college"
    )

    college_graduated_no: BooleanLike = Field(
        default="", description="Indicates a 'No' response for graduating from college"
    )

    college_major_subject_degree: str = Field(
        default="",
        description=(
            "Major subject and/or degree received from college .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_school_names_and_location: str = Field(
        default="",
        description=(
            "Name and location of any other school attended (e.g., trade, vocational, "
            'graduate) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    other_school_graduated_yes: BooleanLike = Field(
        default="",
        description="Indicates a 'Yes' response for graduating from the other listed school",
    )

    other_school_graduated_no: BooleanLike = Field(
        default="",
        description="Indicates a 'No' response for graduating from the other listed school",
    )

    other_school_major_subject_degree: str = Field(
        default="",
        description=(
            "Major subject and/or degree received from the other listed school .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class HumboldtWasteManagementAuthorityEmploymentApplication(BaseModel):
    """
        HUMBOLDT WASTE MANAGEMENT AUTHORITY
    EMPLOYMENT APPLICATION

        THIS APPLICATION IS NOT AN EMPLOYMENT CONTRACT but is merely intended to evaluate suitability for employment. It is our policy to provide equal opportunity for employment to all qualified persons without discrimination on the basis of sex, race, color, religion, age, marital status, national origin, citizenship, disability, veteran status, or any other status protected under State or Federal law. For certain jobs with special needs, the Authority has a policy of requiring a physician’s physical fitness exam, together with urine drug testing of persons who have been offered employment. Individuals who are determined by the physician not to be physically fit for duty, or who test positive for controlled substances, will not be employed. If you have reason to believe that you will not pass a physician’s physical examination, or will test positive for the presence of controlled substances, or if you are unwilling to consent to such an examination or test if offered employment for a job requiring the examination and testing, it is recommended that you not submit an application.
    """

    position_applied_for: PositionAppliedFor = Field(..., description="Position Applied For")
    personal_information: PersonalInformation = Field(..., description="Personal Information")
    eligibility_and_employment_history_questions: EligibilityandEmploymentHistoryQuestions = Field(
        ..., description="Eligibility and Employment History Questions"
    )
    education: Education = Field(..., description="Education")
