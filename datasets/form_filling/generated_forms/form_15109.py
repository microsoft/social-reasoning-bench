from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ChildInformation(BaseModel):
    """Basic information about the child enrolled in the program"""

    my_child: str = Field(
        ...,
        description=(
            "Full name of the child enrolled in the program .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Child's date of birth")  # YYYY-MM-DD format


class MedicalSpecialNeedsInformation(BaseModel):
    """Health conditions, special needs, and dietary restrictions"""

    physical_conditions: str = Field(
        default="",
        description=(
            "Describe any physical conditions or limitations the staff should know about "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    special_attention_medications_routines: str = Field(
        default="",
        description=(
            "List any special attention needs, medications, or routines required during "
            'program hours .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    able_to_participate_extended_care: str = Field(
        default="",
        description=(
            "Indicate whether your child is able to participate and explain any limitations "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    restricted_foods: str = Field(
        default="",
        description=(
            "List foods your child should avoid (allergies, dietary restrictions, etc.) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    special_concerns_information: str = Field(
        default="",
        description=(
            "Provide any additional concerns or information to help staff support your "
            'child .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    physicians_name: str = Field(
        default="",
        description=(
            'Name of the child\'s primary physician .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    physicians_phone: str = Field(
        default="",
        description=(
            "Phone number for the child's physician .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    immunizations_up_to_date: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether the child's immunizations are current per school system requirements"
        ),
    )


class EmergencyAuthorizationSignature(BaseModel):
    """Parent/guardian authorization for emergency treatment and signature"""

    parent_guardian_name: str = Field(
        ...,
        description=(
            "Printed name of the parent or guardian authorizing medical treatment .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    childs_name_emergency_authorization: str = Field(
        ...,
        description=(
            "Child's name as it appears in the emergency medical treatment authorization "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    parents_signature: str = Field(
        ...,
        description=(
            "Signature of the parent or guardian authorizing medical treatment .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date: str = Field(..., description="Date the form is signed")  # YYYY-MM-DD format


class MontclairYmcaSchoolAgeChildCareMedicalInformationForm(BaseModel):
    """
    MONTCLAIR YMCA SCHOOL AGE CHILD CARE MEDICAL INFORMATION FORM

    My child, ________________________________, whose date of birth is _______________ has been enrolled in the school age child care program. The daily program involves both vigorous and quiet indoor and outdoor play, including the use of climbing equipment. A snack is served each day to those children enrolled in the After School Program.
    """

    child_information: ChildInformation = Field(..., description="Child Information")
    medical__special_needs_information: MedicalSpecialNeedsInformation = Field(
        ..., description="Medical & Special Needs Information"
    )
    emergency_authorization__signature: EmergencyAuthorizationSignature = Field(
        ..., description="Emergency Authorization & Signature"
    )
