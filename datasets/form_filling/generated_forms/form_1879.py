from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicationHeader(BaseModel):
    """Basic application and company information"""

    company_name: str = Field(
        ...,
        description=(
            "Name of the company to which you are applying .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date this application is completed")  # YYYY-MM-DD format


class ApplicantInformation(BaseModel):
    """Personal details and contact information for the applicant"""

    applicant_name: str = Field(
        ...,
        description=(
            'Your full legal name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    position_applied_for: str = Field(
        ...,
        description=(
            "Title of the position you are applying for (only one position) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    telephone_number: str = Field(
        ...,
        description=(
            "Primary telephone number with area code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    alternate_cellular_telephone_number: str = Field(
        default="",
        description=(
            "Alternate or mobile telephone number with area code .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    present_address_street_apartment_or_unit_number: str = Field(
        ...,
        description=(
            "Street address including apartment or unit number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    present_address_city: str = Field(
        ...,
        description=(
            'City of your current residence .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    present_address_state: str = Field(..., description="State of your current residence")

    present_address_zip: str = Field(
        ..., description="ZIP or postal code of your current residence"
    )

    how_long_have_you_lived_there_years_months: str = Field(
        ...,
        description=(
            "Length of time at your current address in years and months .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email_address_optional: str = Field(
        default="",
        description=(
            "Email address where you can be contacted .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    under_18_work_certificate_yes: BooleanLike = Field(
        default="", description="Indicate yes if you can provide a work certificate if under 18"
    )

    under_18_work_certificate_no: BooleanLike = Field(
        default="", description="Indicate no if you cannot provide a work certificate if under 18"
    )

    employment_type_full_time: BooleanLike = Field(
        default="", description="Check if you are seeking full-time employment"
    )

    employment_type_part_time: BooleanLike = Field(
        default="", description="Check if you are seeking part-time employment"
    )

    employment_type_specify_hours: str = Field(
        default="",
        description=(
            "If part-time, specify the hours or schedule you are available .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    willing_to_work_overtime_yes: BooleanLike = Field(
        default="", description="Indicate yes if you are willing to work overtime"
    )

    willing_to_work_overtime_no: BooleanLike = Field(
        default="", description="Indicate no if you are not willing to work overtime"
    )

    start_date_if_hired: str = Field(
        ..., description="Earliest date you are available to begin work if hired"
    )  # YYYY-MM-DD format

    previously_applied_yes: BooleanLike = Field(
        default="", description="Indicate yes if you have applied to this company before"
    )

    previously_applied_no: BooleanLike = Field(
        default="", description="Indicate no if you have not applied to this company before"
    )

    previous_application_when_where: str = Field(
        default="",
        description=(
            "If you previously applied, provide the date(s) and location(s) of your "
            'application .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    previously_employed_yes: BooleanLike = Field(
        default="", description="Indicate yes if you have worked for this company before"
    )

    previously_employed_no: BooleanLike = Field(
        default="", description="Indicate no if you have never worked for this company"
    )

    prior_employment_details: str = Field(
        default="",
        description=(
            "If previously employed here, list dates, location, and reason for leaving .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other_names_known_by: str = Field(
        default="",
        description=(
            "Any other names used (maiden name, prior legal names, nicknames) relevant to "
            'work or education records .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class Education(BaseModel):
    """Educational background of the applicant"""

    education_high_school_school_name_location: str = Field(
        ...,
        description=(
            "Name and full address (city and state at minimum) of the high school attended "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    education_high_school_course_of_study_or_major: str = Field(
        default="",
        description=(
            "Primary course of study or academic focus in high school .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    education_high_school_graduate: BooleanLike = Field(
        ..., description="Indicate whether you graduated from high school"
    )

    education_high_school_years_completed: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of years of high school completed"
    )

    education_high_school_honors_received: str = Field(
        default="",
        description=(
            "Any academic honors, awards, or distinctions received in high school .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    education_college_school_name_location: str = Field(
        default="",
        description=(
            "Name and full address (city and state at minimum) of the college attended .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    education_college_course_of_study_or_major: str = Field(
        default="",
        description=(
            "Major field of study or program pursued in college .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    education_college_graduate: BooleanLike = Field(
        default="", description="Indicate whether you graduated from this college"
    )

    education_college_years_completed: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years of college completed"
    )

    education_college_honors_received: str = Field(
        default="",
        description=(
            "Any academic honors, awards, or distinctions received in college .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    education_graduate_professional_school_name_location: str = Field(
        default="",
        description=(
            "Name and full address of any graduate or professional school attended .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    education_graduate_professional_course_of_study_or_major: str = Field(
        default="",
        description=(
            "Graduate or professional program or major field of study .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    education_graduate_professional_graduate: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether you completed and graduated from this graduate/professional program"
        ),
    )

    education_graduate_professional_years_completed: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years completed in graduate or professional school"
    )

    education_graduate_professional_honors_received: str = Field(
        default="",
        description=(
            "Any academic or professional honors received in graduate or professional "
            'school .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    education_trade_correspondence_school_name_location: str = Field(
        default="",
        description=(
            "Name and full address of any trade or correspondence school attended .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    education_trade_correspondence_course_of_study_or_major: str = Field(
        default="",
        description=(
            "Program, trade, or subject studied at the trade or correspondence school .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    education_trade_correspondence_graduate: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether you completed and graduated from this trade or correspondence program"
        ),
    )

    education_trade_correspondence_years_completed: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years completed in trade or correspondence school"
    )

    education_trade_correspondence_honors_received: str = Field(
        default="",
        description=(
            "Any honors, certifications, or distinctions received in trade or "
            'correspondence school .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class ApplicationForEmployment(BaseModel):
    """
    APPLICATION FOR EMPLOYMENT

    Please Answer All Questions. Rsums Are Not A Substitute For A Completed Application.
    We are an equal opportunity employer. Applicants are considered for positions without regard to veteran status, uniformed servicemember status, race, color, religion, sex, national origin, age, physical or mental disability, genetic information or any other category protected by applicable federal, state, or local laws.
    For Rhode Island Employers Only: This Company is subject to the Workers' Compensation laws of the State of Rhode Island.*
    THIS COMPANY IS AN AT-WILL EMPLOYER AS ALLOWED BY APPLICABLE STATE LAW. THIS MEANS THAT REGARDLESS OF ANY PROVISION IN THIS APPLICATION, IF HIRED, THE COMPANY OR I MAY TERMINATE THE EMPLOYMENT RELATIONSHIP AT ANY TIME, FOR ANY REASON, WITH OR WITHOUT CAUSE OR NOTICE.
    """

    application_header: ApplicationHeader = Field(..., description="Application Header")
    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    education: Education = Field(..., description="Education")
