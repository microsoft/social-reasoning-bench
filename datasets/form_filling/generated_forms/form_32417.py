from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PositionAppliedFor(BaseModel):
    """Job opening details and application date"""

    date_of_application: str = Field(
        ..., description="Date this employment application is completed"
    )  # YYYY-MM-DD format

    position_s_applied_for: str = Field(
        ...,
        description=(
            "Title or description of the position or positions you are applying for .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    location: str = Field(
        ...,
        description=(
            "Location or facility where you are applying to work .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    how_did_you_hear_about_this_job: str = Field(
        default="",
        description=(
            "Indicate how you learned about this job opening and, if applicable, the "
            'referring employee\'s name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class PersonalInformation(BaseModel):
    """Applicant’s personal details and contact information"""

    name_in_full: str = Field(
        ...,
        description=(
            'Full legal name .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            'Last (family) name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'First (given) name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    middle_name: str = Field(
        default="",
        description=(
            'Middle name or initial .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    current_address: str = Field(
        ...,
        description=(
            'Current residential address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    current_address_number: str = Field(
        ...,
        description=(
            'Street number of current address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    current_address_street: str = Field(
        ...,
        description=(
            'Street name of current address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    current_address_city: str = Field(
        ...,
        description=(
            'City of current address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    current_address_state: str = Field(..., description="State of current address")

    current_address_zip: str = Field(..., description="ZIP code of current address")

    current_address_how_long: str = Field(
        ...,
        description=(
            "Length of time you have lived at your current address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    previous_address_1: str = Field(
        default="",
        description=(
            "Most recent previous address if less than 3 years at current address .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    previous_address_1_number: str = Field(
        default="",
        description=(
            'Street number for previous address 1 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    previous_address_1_street: str = Field(
        default="",
        description=(
            'Street name for previous address 1 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    previous_address_1_city: str = Field(
        default="",
        description=(
            'City for previous address 1 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    previous_address_1_state: str = Field(default="", description="State for previous address 1")

    previous_address_1_zip: str = Field(default="", description="ZIP code for previous address 1")

    previous_address_1_how_long: str = Field(
        default="",
        description=(
            "Length of time you lived at previous address 1 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    previous_address_2: str = Field(
        default="",
        description=(
            "Second most recent previous address if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    previous_address_2_number: str = Field(
        default="",
        description=(
            'Street number for previous address 2 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    previous_address_2_street: str = Field(
        default="",
        description=(
            'Street name for previous address 2 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    previous_address_2_city: str = Field(
        default="",
        description=(
            'City for previous address 2 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    previous_address_2_state: str = Field(default="", description="State for previous address 2")

    previous_address_2_zip: str = Field(default="", description="ZIP code for previous address 2")

    previous_address_2_how_long: str = Field(
        default="",
        description=(
            "Length of time you lived at previous address 2 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    previous_address_3: str = Field(
        default="",
        description=(
            "Third most recent previous address if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    previous_address_3_number: str = Field(
        default="",
        description=(
            'Street number for previous address 3 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    previous_address_3_street: str = Field(
        default="",
        description=(
            'Street name for previous address 3 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    previous_address_3_city: str = Field(
        default="",
        description=(
            'City for previous address 3 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    previous_address_3_state: str = Field(default="", description="State for previous address 3")

    previous_address_3_zip: str = Field(default="", description="ZIP code for previous address 3")

    previous_address_3_how_long: str = Field(
        default="",
        description=(
            "Length of time you lived at previous address 3 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_number: str = Field(
        ...,
        description=(
            'Primary telephone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    other_telephone_number: str = Field(
        default="",
        description=(
            'Alternate telephone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class EmploymentEligibilityandHistorywithCompany(BaseModel):
    """Prior applications/employment with the company and work eligibility"""

    previously_employed_or_applied_with_pacific_coast_or_family_of_companies_yes: BooleanLike = (
        Field(
            ...,
            description=(
                "Indicate Yes if you have ever been employed by or applied for employment with "
                "Pacific Coast Transportation Services, Inc. or any Pacific Coast Building "
                "Products company"
            ),
        )
    )

    previously_employed_or_applied_with_pacific_coast_or_family_of_companies_no: BooleanLike = (
        Field(
            ...,
            description=(
                "Indicate No if you have never been employed by or applied for employment with "
                "Pacific Coast Transportation Services, Inc. or any Pacific Coast Building "
                "Products company"
            ),
        )
    )

    if_yes_please_specify_dates_locations_and_whether_or_not_you_were_hired: str = Field(
        default="",
        description=(
            "If you answered Yes, provide dates, locations, and whether you were hired .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    legal_right_to_work_verification_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate Yes if you can provide documentation of your legal right to work in the U.S."
        ),
    )

    legal_right_to_work_verification_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate No if you cannot provide documentation of your legal right to work in "
            "the U.S."
        ),
    )

    able_to_perform_essential_functions_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate Yes if you can perform the essential functions of the job with or "
            "without reasonable accommodation"
        ),
    )

    able_to_perform_essential_functions_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate No if you cannot perform the essential functions of the job with or "
            "without reasonable accommodation"
        ),
    )


class DotDriverEmploymentApplication(BaseModel):
    """
    DOT Driver Employment Application

    The information provided in this application may be used, and the applicant’s previous employers will be contacted, for the purpose of investigating the applicant’s safety performance history information as required by 49 CFR 391.23 (d) & (e)
    PACIFIC COAST Transportation Services, Inc., (“the company”) is an equal opportunity employer. All qualified applicants will receive consideration for employment without regard to legally protected status, which may include race, color, religion, sex, sexual orientation, national origin, citizenship status, marital or veteran status, disability, medical condition, age, or other protected status.
    """

    position_applied_for: PositionAppliedFor = Field(..., description="Position Applied For")
    personal_information: PersonalInformation = Field(..., description="Personal Information")
    employment_eligibility_and_history_with_company: EmploymentEligibilityandHistorywithCompany = (
        Field(..., description="Employment Eligibility and History with Company")
    )
