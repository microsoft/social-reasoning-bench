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
    """Basic personal and contact details for the applicant"""

    full_name: str = Field(
        ...,
        description=(
            'Applicant\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date this application is completed")  # YYYY-MM-DD format

    address: str = Field(
        ...,
        description=(
            "Street address, including apartment or unit number if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of current residence .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of current residence")

    zip: str = Field(..., description="Zip or postal code")

    home_phone: str = Field(
        default="",
        description=(
            'Home telephone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        ...,
        description=(
            'Primary cell/mobile phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Applicant's date of birth")  # YYYY-MM-DD format

    social_security_number: str = Field(..., description="Applicant's Social Security Number")


class EducationCertifications(BaseModel):
    """Education history and relevant certifications"""

    high_school: str = Field(
        ...,
        description=(
            'Name of high school attended .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    did_you_receive_your_high_school_diploma_yes_no: BooleanLike = Field(
        ..., description="Indicate if you received a high school diploma"
    )

    college: str = Field(
        default="",
        description=(
            "Name of college or university attended .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    did_you_receive_your_college_diploma_yes_no: BooleanLike = Field(
        default="", description="Indicate if you received a college degree or diploma"
    )

    major: str = Field(
        default="",
        description=(
            'Field of study or major in college .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    number_of_years_attended: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years you attended college"
    )

    first_aid_certified_yes_no: BooleanLike = Field(
        default="", description="Indicate if you are currently certified in First Aid"
    )

    first_aid_certified_date_received: str = Field(
        default="", description="Date First Aid certification was received"
    )  # YYYY-MM-DD format


class BackgroundChecksLegalHistory(BaseModel):
    """Background clearances and any criminal history"""

    fbi_fingerprinting_yes_no: BooleanLike = Field(
        ..., description="Indicate if FBI fingerprinting background check has been completed"
    )

    fbi_fingerprinting_date: str = Field(
        ..., description="Date FBI fingerprinting background check was completed"
    )  # YYYY-MM-DD format

    child_abuse_yes_no: BooleanLike = Field(
        ..., description="Indicate if a Child Abuse background check has been completed"
    )

    child_abuse_date: str = Field(
        ..., description="Date Child Abuse background check was completed"
    )  # YYYY-MM-DD format

    pa_criminal_background_yes_no: BooleanLike = Field(
        ..., description="Indicate if a PA Criminal Background check has been completed"
    )

    pa_criminal_background_date: str = Field(
        ..., description="Date PA Criminal Background check was completed"
    )  # YYYY-MM-DD format

    have_you_ever_been_arrested_or_charged_for_a_felony_and_or_misdemeanor_yes_no: BooleanLike = (
        Field(
            ...,
            description=(
                "Indicate if you have ever been arrested or charged for a felony and/or misdemeanor"
            ),
        )
    )

    explain_felony_and_or_misdemeanor: str = Field(
        default="",
        description=(
            "If yes, provide details about the felony and/or misdemeanor .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class AvailabilityEmploymentDetails(BaseModel):
    """Desired hours, schedule, and current employment status"""

    hours_desired_part_time_full_time: Literal["Part Time", "Full Time", "N/A", ""] = Field(
        ..., description="Indicate whether you are seeking part-time or full-time hours"
    )

    are_you_over_18_years_of_age_and_can_you_provide_documentation_to_prove_so_yes_no: BooleanLike = Field(
        ..., description="Confirm you are over 18 and can provide documentation"
    )

    full_time_shift_7_4_8_5_9_6: Literal["7-4", "8-5", "9-6", "N/A", ""] = Field(
        default="", description="Preferred full-time shift hours (if applying for full-time)"
    )

    part_time_hours: str = Field(
        default="",
        description=(
            "Specify desired part-time working hours .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    circle_one_seasonal_year_round: Literal["Seasonal", "Year-Round", "N/A", ""] = Field(
        ..., description="Indicate whether you are seeking seasonal or year-round employment"
    )

    if_seasonal_please_explain: str = Field(
        default="",
        description=(
            "If applying for seasonal work, explain your seasonal availability .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    available_start_date: str = Field(
        ..., description="Date you are available to begin employment"
    )  # YYYY-MM-DD format

    currently_employed_yes_no: BooleanLike = Field(
        default="", description="Indicate if you are currently employed"
    )

    current_employment: str = Field(
        default="",
        description=(
            "Name of current employer or place of employment .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    position_desired: str = Field(
        ...,
        description=(
            "Job title or position you are applying for .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProfessionalDevelopmentProgramKnowledge(BaseModel):
    """Interest in further education and familiarity with Keystone Stars"""

    are_you_willing_to_further_your_education_in_early_childhood_yes_no: BooleanLike = Field(
        default="",
        description="Indicate if you are willing to pursue additional education in early childhood",
    )

    explain_willingness_to_further_education: str = Field(
        default="",
        description=(
            "Provide details about how you are willing to further your education in early "
            'childhood .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    are_you_familiar_with_keystone_stars_yes_no: BooleanLike = Field(
        default="",
        description="Indicate if you are familiar with the Keystone STARS quality rating system",
    )


class AardvarkChildCareEmploymentApplication(BaseModel):
    """
    Aardvark Child Care Employment Application

    ''
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    education__certifications: EducationCertifications = Field(
        ..., description="Education & Certifications"
    )
    background_checks__legal_history: BackgroundChecksLegalHistory = Field(
        ..., description="Background Checks & Legal History"
    )
    availability__employment_details: AvailabilityEmploymentDetails = Field(
        ..., description="Availability & Employment Details"
    )
    professional_development__program_knowledge: ProfessionalDevelopmentProgramKnowledge = Field(
        ..., description="Professional Development & Program Knowledge"
    )
