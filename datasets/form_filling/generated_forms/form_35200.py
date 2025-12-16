from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ClassificationofCertificateRequested(BaseModel):
    """Type and level of emergency medical transportation service requested"""

    basic_life_support_ground: BooleanLike = Field(
        ...,
        description="Check if the certificate requested is for Basic Life Support – Ground service",
    )

    advanced_life_support_ground: BooleanLike = Field(
        ...,
        description=(
            "Check if the certificate requested is for Advanced Life Support – Ground service"
        ),
    )

    basic_life_support_air: BooleanLike = Field(
        ...,
        description="Check if the certificate requested is for Basic Life Support – Air service",
    )

    advanced_life_support_air: BooleanLike = Field(
        ...,
        description="Check if the certificate requested is for Advanced Life Support – Air service",
    )


class TypeofApplication(BaseModel):
    """Whether this is a new application or a renewal"""

    new: BooleanLike = Field(..., description="Check if this is a new application")

    renewal: BooleanLike = Field(..., description="Check if this is a renewal application")

    date_of_application: str = Field(
        ..., description="Date this application is completed"
    )  # YYYY-MM-DD format


class TypeofOwnership(BaseModel):
    """Ownership structure of the applying entity"""

    private: BooleanLike = Field(..., description="Check if the ownership type is private")

    governmental: BooleanLike = Field(
        ..., description="Check if the ownership type is governmental"
    )

    volunteer: BooleanLike = Field(..., description="Check if the ownership type is volunteer")

    not_for_profit: BooleanLike = Field(
        ..., description="Check if the ownership type is not-for-profit"
    )


class BusinessInformation(BaseModel):
    """Business identity and primary contact"""

    business_name_address_phone_number: str = Field(
        ...,
        description=(
            "Full legal business name, mailing address, and primary phone number .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    president_ceo: str = Field(
        ...,
        description=(
            "Name of the President or Chief Executive Officer of the business .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class OwnershipandManagementDetails(BaseModel):
    """Operator/owner information and corporate control details"""

    names_business_addresses_experience_operator_owner: str = Field(
        ...,
        description=(
            "Provide names, business addresses, and relevant experience for both the "
            "operator and the owner of the proposed service .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    names_addresses_directors_officers_shareholders_corporate: str = Field(
        ...,
        description=(
            "If the owner or operator is a corporate entity, list the names and addresses "
            "of all directors, officers, and controlling shareholders .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CitrusCountyFireRescueEMTApplicationForCertificate(BaseModel):
    """
        CITRUS COUNTY
    DEPARTMENT OF FIRE RESCUE
    APPLICATION FOR CERTIFICATE OF PUBLIC CONVENIENCE AND
    NECESSITY FOR EMERGENCY MEDICAL TRANSPORTATION

        STATEMENTS AND MATERIALS SUBMITTED WILL BE SUBJECT TO VERIFICATION
    """

    classification_of_certificate_requested: ClassificationofCertificateRequested = Field(
        ..., description="Classification of Certificate Requested"
    )
    type_of_application: TypeofApplication = Field(..., description="Type of Application")
    type_of_ownership: TypeofOwnership = Field(..., description="Type of Ownership")
    business_information: BusinessInformation = Field(..., description="Business Information")
    ownership_and_management_details: OwnershipandManagementDetails = Field(
        ..., description="Ownership and Management Details"
    )
