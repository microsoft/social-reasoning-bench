from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantandPropertyInformation(BaseModel):
    """Owner, applicant, contact, and site identification details"""

    owner_of_site: str = Field(
        ...,
        description=(
            "Name of the property owner of the site .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_owner_of_site: str = Field(
        ...,
        description=(
            "Mailing address of the property owner of the site .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    applicant_if_other_than_owner: str = Field(
        default="",
        description=(
            "Name of the applicant if different from the property owner .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_applicant: str = Field(
        default="",
        description=(
            "Mailing address of the applicant (if different from owner) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number_owner: str = Field(
        ...,
        description=(
            'Phone number for the property owner .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone_number_applicant: str = Field(
        default="",
        description=(
            "Phone number for the applicant (if different from owner) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tax_key_number_of_site: str = Field(
        ...,
        description=(
            "Tax key or parcel identification number for the site .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    legal_description_of_site: str = Field(
        ...,
        description=(
            "Full legal description of the property .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ZoningandProposedUse(BaseModel):
    """Zoning classification and details of the proposed structure/use"""

    zoning_district: str = Field(
        ...,
        description=(
            "Current zoning district designation for the site .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    type_of_structure: str = Field(
        ...,
        description=(
            "Type of building or structure involved in the conditional use .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    proposed_use_of_structure_or_site_in_detail: str = Field(
        ...,
        description=(
            "Detailed description of the proposed use of the structure or site .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class A1ZoningDistrictAcknowledgment(BaseModel):
    """Signatures acknowledging conditions for A-1 zoning district conditional uses"""

    property_owner_signature_a1_section: str = Field(
        default="",
        description=(
            "Signature of the property owner acknowledging A-1 zoning district conditions "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    applicant_signature_a1_section: str = Field(
        default="",
        description=(
            "Signature of the applicant acknowledging A-1 zoning district conditions .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class OperationalDetailsandFees(BaseModel):
    """Operational information, timing of improvements, and fee payment"""

    number_of_employees_or_users_to_be_accommodated: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Total number of employees or users that the proposed use will accommodate",
    )

    start_date_for_installation_of_all_improvements: str = Field(
        default="", description="Planned start date for installing all improvements"
    )  # YYYY-MM-DD format

    completion_date_for_installation_of_all_improvements: str = Field(
        default="", description="Planned completion date for installing all improvements"
    )  # YYYY-MM-DD format

    amount_enclosed: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Dollar amount of the application fee enclosed"
    )


class FinalAuthorization(BaseModel):
    """Final date and property owner signature for the application"""

    date_final_signature_line: str = Field(
        ..., description="Date the property owner signs the application"
    )  # YYYY-MM-DD format

    property_owner_signature_final: str = Field(
        ...,
        description=(
            "Final signature of the property owner certifying the application .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ConditionalUsePermitApplicationForWalworthCounty(BaseModel):
    """
    CONDITIONAL USE PERMIT APPLICATION FOR WALWORTH COUNTY

    The undersigned hereby applies to the Walworth County Zoning Agency pursuant to Section 4 of the Code of Ordinances (Zoning/Shoreland Zoning), Walworth County, Wisconsin for a conditional use permit and represents as follows:
    """

    applicant_and_property_information: ApplicantandPropertyInformation = Field(
        ..., description="Applicant and Property Information"
    )
    zoning_and_proposed_use: ZoningandProposedUse = Field(
        ..., description="Zoning and Proposed Use"
    )
    a_1_zoning_district_acknowledgment: A1ZoningDistrictAcknowledgment = Field(
        ..., description="A-1 Zoning District Acknowledgment"
    )
    operational_details_and_fees: OperationalDetailsandFees = Field(
        ..., description="Operational Details and Fees"
    )
    final_authorization: FinalAuthorization = Field(..., description="Final Authorization")
