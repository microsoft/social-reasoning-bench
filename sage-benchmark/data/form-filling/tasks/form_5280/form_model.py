from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProjectInformation(BaseModel):
    """Basic information about the project and its location"""

    project_title: str = Field(
        ...,
        description=(
            'Title or name of the project .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Street address of the project location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City where the project is located .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zip: str = Field(..., description="Zip code for the project location")


class EnvironmentalDetails(BaseModel):
    """Narrative description of the project and environmental context"""

    project_description: str = Field(
        ...,
        description=(
            "Narrative description of the proposed project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    existing_environmental_conditions: str = Field(
        ...,
        description=(
            "Description of current environmental conditions at the project site .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    itemization_of_attached_support_data: str = Field(
        default="",
        description=(
            "List and describe any supporting documents attached to this form .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    previous_county_actions_and_or_environmental_documentation: str = Field(
        default="",
        description=(
            "Describe any prior County actions or environmental documents related to this "
            'project .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    government_approvals_required: str = Field(
        default="",
        description=(
            "List other government approvals, permits, or clearances required for the "
            'project .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class ContactInformation(BaseModel):
    """Primary contact person for this application"""

    contact_persons: str = Field(
        ...,
        description=(
            "Name(s) of the primary contact person(s) for this project .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number: str = Field(
        ...,
        description=(
            "Phone number for the contact person(s) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Declaration(BaseModel):
    """Applicant declaration and authorization"""

    signature: str = Field(
        ...,
        description=(
            "Signature of the person making the declaration .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the declaration is signed")  # YYYY-MM-DD format


class OcPublicWorksEnvironmentalInformation(BaseModel):
    """
        OC Public Works

    Environmental Information

        ''
    """

    project_information: ProjectInformation = Field(..., description="Project Information")
    environmental_details: EnvironmentalDetails = Field(..., description="Environmental Details")
    contact_information: ContactInformation = Field(..., description="Contact Information")
    declaration: Declaration = Field(..., description="Declaration")
