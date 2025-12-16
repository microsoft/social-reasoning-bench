from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EmploymentHistory(BaseModel):
    """Employment record for up to three positions (A–C)"""

    a_name_and_address_of_employer_include_zip_code_if_known: str = Field(
        ...,
        description=(
            "Full name and mailing address of employer, including ZIP code if known, for "
            'employment record A. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    a_dates_employed_month_year_from: str = Field(
        ...,
        description=(
            "Start date (month and year) of employment for employer A. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    a_dates_employed_month_year_to: str = Field(
        ...,
        description=(
            "End date (month and year) of employment for employer A. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    a_exact_title_of_your_position: str = Field(
        ...,
        description=(
            "Official job title for the position held with employer A. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    a_name_of_immediate_supervisor: str = Field(
        default="",
        description=(
            "Full name of your direct supervisor at employer A. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    a_telephone_no: str = Field(
        default="",
        description=(
            "Telephone number for employer A or your supervisor there. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    a_number_and_class_or_level_of_employees_you_supervised: str = Field(
        default="",
        description=(
            "Number of employees supervised and their class or level for employer A. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    b_name_and_address_of_employer_include_zip_code_if_known: str = Field(
        default="",
        description=(
            "Full name and mailing address of employer, including ZIP code if known, for "
            'employment record B. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    b_dates_employed_month_year_from: str = Field(
        default="",
        description=(
            "Start date (month and year) of employment for employer B. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    b_dates_employed_month_year_to: str = Field(
        default="",
        description=(
            "End date (month and year) of employment for employer B. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    b_exact_title_of_your_position: str = Field(
        default="",
        description=(
            "Official job title for the position held with employer B. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    b_name_of_immediate_supervisor: str = Field(
        default="",
        description=(
            "Full name of your direct supervisor at employer B. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    b_telephone_no: str = Field(
        default="",
        description=(
            "Telephone number for employer B or your supervisor there. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    b_number_and_class_or_level_of_employees_you_supervised: str = Field(
        default="",
        description=(
            "Number of employees supervised and their class or level for employer B. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    c_name_and_address_of_employer_include_zip_code_if_known: str = Field(
        default="",
        description=(
            "Full name and mailing address of employer, including ZIP code if known, for "
            'employment record C. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    c_dates_employed_month_year_from: str = Field(
        default="",
        description=(
            "Start date (month and year) of employment for employer C. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    c_dates_employed_month_year_to: str = Field(
        default="",
        description=(
            "End date (month and year) of employment for employer C. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    c_exact_title_of_your_position: str = Field(
        default="",
        description=(
            "Official job title for the position held with employer C. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    c_name_of_immediate_supervisor: str = Field(
        default="",
        description=(
            "Full name of your direct supervisor at employer C. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    c_telephone_no: str = Field(
        default="",
        description=(
            "Telephone number for employer C or your supervisor there. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    c_number_and_class_or_level_of_employees_you_supervised: str = Field(
        default="",
        description=(
            "Number of employees supervised and their class or level for employer C. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    authorization_release_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate that you DO authorize the departments to obtain information from "
            "former employers and references and release them from liability."
        ),
    )

    authorization_release_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate that you DO NOT authorize the departments to obtain information from "
            "former employers and references and release them from liability."
        ),
    )


class CriminalHistory(BaseModel):
    """Questions about past convictions and pending charges"""

    convicted_offense_yes: BooleanLike = Field(
        ...,
        description=(
            "Select if you HAVE been convicted of a criminal offense or forfeited "
            "bond/collateral as described."
        ),
    )

    convicted_offense_no: BooleanLike = Field(
        ...,
        description=(
            "Select if you HAVE NOT been convicted of a criminal offense or forfeited "
            "bond/collateral as described."
        ),
    )

    pending_charges_yes: BooleanLike = Field(
        ..., description="Select if there ARE criminal charges currently pending against you."
    )

    pending_charges_no: BooleanLike = Field(
        ..., description="Select if there are NO criminal charges currently pending against you."
    )


class Certification(BaseModel):
    """Applicant certification and signature"""

    signature_of_applicant: str = Field(
        ...,
        description=(
            "Applicant’s handwritten or electronic signature certifying the accuracy of the "
            'application. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    signature_date: str = Field(
        ..., description="Date on which the applicant signs the certification."
    )  # YYYY-MM-DD format


class Employment(BaseModel):
    """
    EMPLOYMENT

    16. List your employment record. Start with present employment, including paid employment, internships, volunteer or unpaid work, and military service. If your title and duties changed in the course of your work with one employer, describe the changed duties in a new block. Attach additional sheets, if needed. Include your name and social security number and the same information as requested in A through C.
    """

    employment_history: EmploymentHistory = Field(..., description="Employment History")
    criminal_history: CriminalHistory = Field(..., description="Criminal History")
    certification: Certification = Field(..., description="Certification")
