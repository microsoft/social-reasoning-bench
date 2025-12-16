from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class BabysitterInformation(BaseModel):
    """Information about the babysitter and their residence"""

    babysitters_name: str = Field(
        ...,
        description=(
            'Full legal name of the babysitter .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    babysitter_address_street_city_state_zip_and_phone_number_line_1: str = Field(
        ...,
        description=(
            "First line of the babysitter's home address including street, city, state, "
            'zip, and phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    babysitter_address_street_city_state_zip_and_phone_number_line_2: str = Field(
        default="",
        description=(
            "Second line for additional babysitter address details and phone number, if "
            'needed .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    are_you_a_licensed_day_care_provider_yes: BooleanLike = Field(
        default="",
        description="Check if the babysitter is a licensed day care provider (Yes option)",
    )

    are_you_a_licensed_day_care_provider_no: BooleanLike = Field(
        default="",
        description="Check if the babysitter is not a licensed day care provider (No option)",
    )


class StudentInformation(BaseModel):
    """Children being babysat and their home address"""

    childs_name_row_1: str = Field(
        ...,
        description=(
            'First child\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    childs_date_of_birth_row_1: str = Field(
        ..., description="Date of birth for the first child"
    )  # YYYY-MM-DD format

    grade_entering_fall_21_row_1: str = Field(
        ...,
        description=(
            "Grade the first child will be entering in Fall 2021 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    childs_name_row_2: str = Field(
        default="",
        description=(
            "Second child's full name, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    childs_date_of_birth_row_2: str = Field(
        default="", description="Date of birth for the second child, if applicable"
    )  # YYYY-MM-DD format

    grade_entering_fall_21_row_2: str = Field(
        default="",
        description=(
            "Grade the second child will be entering in Fall 2021, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    childs_name_row_3: str = Field(
        default="",
        description=(
            "Third child's full name, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    childs_date_of_birth_row_3: str = Field(
        default="", description="Date of birth for the third child, if applicable"
    )  # YYYY-MM-DD format

    grade_entering_fall_21_row_3: str = Field(
        default="",
        description=(
            "Grade the third child will be entering in Fall 2021, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    student_address: str = Field(
        ...,
        description=(
            "Home address where the student(s) reside .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class SchoolRequestSpecialCircumstances(BaseModel):
    """Requested school assignment and any special circumstances"""

    schools_name: str = Field(
        ...,
        description=(
            "Name of the home school for the babysitter's residence .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    special_circumstances: str = Field(
        default="",
        description=(
            "Description of any special circumstances related to this babysitter "
            'arrangement .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class SignaturesandNotary(BaseModel):
    """Babysitter signature and notary verification"""

    babysitter_signature: str = Field(
        ...,
        description=(
            "Signature of the babysitter attesting to the information provided .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_babysitter_signature: str = Field(
        ..., description="Date the babysitter signed the affidavit"
    )  # YYYY-MM-DD format

    sworn_to_before_me_on_this_day_number: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Calendar day of the month when the affidavit was notarized"
    )

    day_of_month: str = Field(
        ...,
        description=(
            "Month name when the affidavit was notarized .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    year_20: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year when the affidavit was notarized (e.g., 2021)"
    )

    notary_public: str = Field(
        ...,
        description=(
            "Signature and identification of the Notary Public .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class LiverpoolCSDOfficeElementaryEdBabysitterApproval2122(BaseModel):
    """
        LIVERPOOL CENTRAL SCHOOL DISTRICT
    Office of Elementary Education
    APPLICATION FOR BABYSITTER APPROVAL 2021-2022

        (To be completed by the BABYSITTER when they DO NOT live in the parent's home school zone).
    """

    babysitter_information: BabysitterInformation = Field(..., description="Babysitter Information")
    student_information: StudentInformation = Field(..., description="Student Information")
    school_request__special_circumstances: SchoolRequestSpecialCircumstances = Field(
        ..., description="School Request & Special Circumstances"
    )
    signatures_and_notary: SignaturesandNotary = Field(..., description="Signatures and Notary")
