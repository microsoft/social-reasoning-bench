from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MedicalInformation(BaseModel):
    """Current medical details, medications, allergies, and related notes"""

    primary_care_physicians_name_address_and_phone_number_approximate_date_of_last_visit: str = (
        Field(
            default="",
            description=(
                "Enter your primary care physician's full name, office address, phone number, "
                "and approximate date of your last visit. .If you cannot fill this, write "
                '"N/A". If this field should not be filled by you (for example, it belongs to '
                'another person or office), leave it blank (empty string "").'
            ),
        )
    )

    what_medications_are_you_currently_taking: str = Field(
        default="",
        description=(
            "List all medications you are currently taking, including prescriptions, "
            "over-the-counter drugs, and supplements. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    please_explain_any_reactions_here: str = Field(
        default="",
        description=(
            "Describe any allergic or adverse reactions you have had to medications or "
            'materials. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    women_only_are_you_pregnant_yes: BooleanLike = Field(
        default="", description="Check if the patient is pregnant (Yes option for women only)."
    )

    women_only_are_you_pregnant_no: BooleanLike = Field(
        default="", description="Check if the patient is not pregnant (No option for women only)."
    )

    do_you_have_any_other_health_issues_or_allergies: str = Field(
        default="",
        description=(
            "Provide details about any additional health issues or allergies not already "
            'listed. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class FormAdministration(BaseModel):
    """Administrative information related to this response"""

    response_date: str = Field(
        default="", description="Date this form was completed."
    )  # YYYY-MM-DD format


class TedAJowettFamilyDentistry(BaseModel):
    """
        TED A. JOWETT
    FAMILY DENTISTRY

        ''
    """

    medical_information: MedicalInformation = Field(..., description="Medical Information")
    form_administration: FormAdministration = Field(..., description="Form Administration")
