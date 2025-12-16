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
    """Basic identifying and contact information for the applicant"""

    name_last: str = Field(
        ...,
        description=(
            'Applicant\'s legal last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    name_first: str = Field(
        ...,
        description=(
            'Applicant\'s legal first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    name_middle: str = Field(
        default="",
        description=(
            'Applicant\'s middle name or initial .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_npc_student_id: str = Field(
        default="",
        description=(
            'NPC Student ID number, if assigned .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    other_names_used_now_or_in_the_past: str = Field(
        default="",
        description=(
            "Any other names you have used (maiden name, previous legal names, etc.) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    e_mail_address: str = Field(
        ...,
        description=(
            'Primary email address for contact .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_number: str = Field(
        ...,
        description=(
            'Street number of your mailing address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_street: str = Field(
        ...,
        description=(
            "Street name and apartment or unit, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_city: str = Field(
        ...,
        description=(
            'City of your mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_state: str = Field(..., description="State of your mailing address")

    mailing_address_zip: str = Field(..., description="ZIP code of your mailing address")

    phone_home: str = Field(
        default="",
        description=(
            'Home phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    phone_work: str = Field(
        default="",
        description=(
            'Work phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    phone_cell: str = Field(
        ...,
        description=(
            'Cell phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    when_do_you_anticipate_starting_the_rn_refresher_program: str = Field(
        ...,
        description=(
            "Planned start term or date for the RN Refresher Program .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class LicensureandEmploymentHistory(BaseModel):
    """Previous RN license information and employment background"""

    previous_rn_license_number: str = Field(
        ...,
        description=(
            "Your previous Registered Nurse license number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    previous_rn_license_state: str = Field(
        ..., description="State that issued your previous RN license"
    )

    previous_rn_license_date_expired: str = Field(
        ..., description="Expiration date of your previous RN license"
    )  # YYYY-MM-DD format

    current_employment: str = Field(
        default="",
        description=(
            'Your current employer and position .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    last_place_and_dates_of_employment_as_a_registered_nurse: str = Field(
        default="",
        description=(
            "Most recent RN employer and dates of employment .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProfessionalandLegalHistory(BaseModel):
    """Disciplinary, legal, health, and related background information"""

    any_disciplinary_actions_on_your_nursing_license: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether there have been any disciplinary actions on your nursing license"
        ),
    )

    any_disciplinary_actions_on_your_nursing_license_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether there have been any disciplinary actions on your nursing license"
        ),
    )

    if_yes_please_explain_disciplinary_actions_on_your_nursing_license: str = Field(
        default="",
        description=(
            "Explanation of any disciplinary actions on your nursing license .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    previously_enrolled_in_other_refresher_programs: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you have ever been enrolled in any other or different "
            "refresher programs"
        ),
    )

    previously_enrolled_in_other_refresher_programs_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you have ever been enrolled in any other or different "
            "refresher programs"
        ),
    )

    able_to_perform_essential_functions: BooleanLike = Field(
        ...,
        description=(
            "Confirm whether you can perform the essential functions described in the "
            "Nursing Student Handbook, with or without reasonable accommodations"
        ),
    )

    able_to_perform_essential_functions_no: BooleanLike = Field(
        ...,
        description=(
            "Confirm whether you can perform the essential functions described in the "
            "Nursing Student Handbook, with or without reasonable accommodations"
        ),
    )

    ever_convicted_of_a_felony: BooleanLike = Field(
        ..., description="Indicate whether you have ever been convicted of a felony"
    )

    ever_convicted_of_a_felony_no: BooleanLike = Field(
        ..., description="Indicate whether you have ever been convicted of a felony"
    )

    legal_resident_of_united_states: BooleanLike = Field(
        ..., description="Indicate whether you are a legal resident of the United States of America"
    )

    legal_resident_of_united_states_no: BooleanLike = Field(
        ..., description="Indicate whether you are a legal resident of the United States of America"
    )

    currently_using_illegal_or_misusing_prescription_drugs: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you are currently using illegal drugs or misusing prescription drugs"
        ),
    )

    currently_using_illegal_or_misusing_prescription_drugs_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you are currently using illegal drugs or misusing prescription drugs"
        ),
    )

    subject_of_any_complaint_investigation_or_disciplinary_action: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you have ever been or are currently the subject of any "
            "complaint, investigation, or disciplinary action related to your professional "
            "credentials"
        ),
    )

    subject_of_any_complaint_investigation_or_disciplinary_action_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you have ever been or are currently the subject of any "
            "complaint, investigation, or disciplinary action related to your professional "
            "credentials"
        ),
    )

    if_yes_please_explain_complaint_investigation_or_disciplinary_action: str = Field(
        default="",
        description=(
            "Explanation of any complaint, investigation, or disciplinary action related to "
            'your professional credentials .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class RnRefresherProgramApplicationForAdmission(BaseModel):
    """
        RN REFRESHER PROGRAM
    APPLICATION FOR ADMISSION

        ''
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    licensure_and_employment_history: LicensureandEmploymentHistory = Field(
        ..., description="Licensure and Employment History"
    )
    professional_and_legal_history: ProfessionalandLegalHistory = Field(
        ..., description="Professional and Legal History"
    )
