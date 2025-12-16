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
    """Health details, allergies, medications, and special needs for the child"""

    health_card_number: str = Field(
        ...,
        description=(
            'Child\'s provincial health card number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    does_your_child_have_any_food_allergies_or_dietary_restrictions: str = Field(
        ...,
        description=(
            "Describe any food allergies or dietary restrictions your child has .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    please_list_any_medical_conditions_or_and_allergies: str = Field(
        ...,
        description=(
            "List all relevant medical conditions and allergies .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    please_list_any_medications_your_child_is_currently_taking_please_include_dosage_and_frequency: str = Field(
        ...,
        description=(
            "List all current medications including dosage and frequency .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    does_your_child_require_an_epipen_for_which_allergy_is_this_required: str = Field(
        ...,
        description=(
            "Indicate if an EpiPen is required and specify the allergy .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    please_identify_and_explain_any_special_needs_or_exceptionalities_as_they_pertain_to_you_child: str = Field(
        default="",
        description=(
            "Describe any special needs, exceptionalities, or accommodations required .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class MedicalRiskRelease(BaseModel):
    """Parental permissions and acknowledgements for medical treatment and outings"""

    name_of_parent_guardian_giving_medical_permission: str = Field(
        ...,
        description=(
            "Printed name of the parent or guardian authorizing medical treatment .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    name_of_child_for_medical_permission: str = Field(
        ...,
        description=(
            "Name of the child for whom medical permission is granted .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_parent_guardian_giving_outing_permission: str = Field(
        ...,
        description=(
            "Printed name of the parent or guardian authorizing community outings .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    name_of_child_for_outing_permission: str = Field(
        ...,
        description=(
            "Name of the child who is permitted to take part in community outings .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    name: str = Field(
        ...,
        description=(
            "Name of parent or guardian completing and signing the form .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature: str = Field(
        ...,
        description=(
            "Signature of parent or guardian confirming consent and accuracy .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date: str = Field(..., description="Date the form is signed")  # YYYY-MM-DD format


class MedicalInformation(BaseModel):
    """
    Medical Information

    Ralph Thornton Community Centre respects your privacy. We adhere to legislative requirements with respect to protecting your privacy. The information on this form will be used to process your application for program participation, to deliver services, and to keep you informed and up to date about Ralph Thornton Community Center activities.
    """

    medical_information: MedicalInformation = Field(..., description="Medical Information")
    medicalrisk_release: MedicalRiskRelease = Field(..., description="Medical/Risk Release")
