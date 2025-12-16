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
    """Details about the applicant and business"""

    name_of_applicant_as_it_is_to_appear_on_the_bond: str = Field(
        ...,
        description=(
            "Legal name of the applicant exactly as it should appear on the bond .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    entity_individual: BooleanLike = Field(
        ..., description="Check if the applicant is an individual"
    )

    entity_corporation: BooleanLike = Field(
        ..., description="Check if the applicant is a corporation"
    )

    entity_llc: BooleanLike = Field(
        ..., description="Check if the applicant is a limited liability company (LLC)"
    )

    entity_partnership: BooleanLike = Field(
        ..., description="Check if the applicant is a partnership"
    )

    entity_other: str = Field(
        default="",
        description=(
            "If entity type is not listed, check 'Other' and specify the type .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street address of the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the applicant\'s address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    county: str = Field(
        default="",
        description=(
            'County of the applicant\'s address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of the applicant's address")

    zip_code: str = Field(..., description="ZIP or postal code of the applicant's address")

    owner_name_if_applicant_is_a_business_entity: str = Field(
        ...,
        description=(
            "Full name of the owner if the applicant is a business entity .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    business_fein: str = Field(
        default="",
        description=(
            "Federal Employer Identification Number of the business .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    owner_ssn: str = Field(..., description="Social Security Number of the owner")

    email_address: str = Field(
        ...,
        description=(
            "Primary email address for the applicant or owner .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    primary_website_url: str = Field(
        default="",
        description=(
            'Main website address for the business .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    business_phone_number: str = Field(
        ...,
        description=(
            'Primary business telephone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    years_of_experience_years_licensed: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of years of relevant experience or years licensed"
    )

    license_ubi_lic_or_application_number: str = Field(
        ...,
        description=(
            "License number, UBI, license number, or application number as applicable .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class BusinessandPrincipalHistory(BaseModel):
    """Background questions about the business and principals"""

    have_any_outstanding_collection_items_or_liens_yes: BooleanLike = Field(
        ...,
        description=(
            "Select 'Yes' if the business or any principal has outstanding collection items "
            "or liens"
        ),
    )

    have_any_outstanding_collection_items_or_liens_no: BooleanLike = Field(
        ...,
        description=(
            "Select 'No' if the business or any principal does not have outstanding "
            "collection items or liens"
        ),
    )

    failed_in_business_or_declared_bankruptcy_yes: BooleanLike = Field(
        ...,
        description=(
            "Select 'Yes' if the business or any principal has failed in business or "
            "declared bankruptcy"
        ),
    )

    failed_in_business_or_declared_bankruptcy_no: BooleanLike = Field(
        ...,
        description=(
            "Select 'No' if the business or any principal has not failed in business or "
            "declared bankruptcy"
        ),
    )

    had_any_lawsuits_or_judgments_against_them_yes: BooleanLike = Field(
        ...,
        description=(
            "Select 'Yes' if the business or any principal has had lawsuits or judgments "
            "against them"
        ),
    )

    had_any_lawsuits_or_judgments_against_them_no: BooleanLike = Field(
        ...,
        description=(
            "Select 'No' if the business or any principal has not had lawsuits or judgments "
            "against them"
        ),
    )

    had_a_license_or_bond_cancelled_or_denied_yes: BooleanLike = Field(
        ..., description="Select 'Yes' if any license or bond has been cancelled or denied"
    )

    had_a_license_or_bond_cancelled_or_denied_no: BooleanLike = Field(
        ..., description="Select 'No' if no license or bond has been cancelled or denied"
    )

    been_a_party_to_a_surety_bond_claim_yes: BooleanLike = Field(
        ...,
        description=(
            "Select 'Yes' if the business or any principal has been a party to a surety bond claim"
        ),
    )

    been_a_party_to_a_surety_bond_claim_no: BooleanLike = Field(
        ...,
        description=(
            "Select 'No' if the business or any principal has not been a party to a surety "
            "bond claim"
        ),
    )

    been_convicted_of_a_crime_yes: BooleanLike = Field(
        ...,
        description="Select 'Yes' if the business or any principal has been convicted of a crime",
    )

    been_convicted_of_a_crime_no: BooleanLike = Field(
        ...,
        description="Select 'No' if the business or any principal has not been convicted of a crime",
    )

    explanations_for_fields_marked_yes: str = Field(
        default="",
        description=(
            "Provide details for any questions above that were answered 'Yes' .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class BondandObligee(BaseModel):
    """Information about the bond and the obligee"""

    bond_amount: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Dollar amount of the bond being requested"
    )

    effective_date: str = Field(
        ..., description="Date on which the bond should become effective"
    )  # YYYY-MM-DD format

    type_of_bond: str = Field(
        ...,
        description=(
            "Description or type of contractor license bond requested .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    full_name_of_obligee_first_last_or_business_name: str = Field(
        ...,
        description=(
            "Full legal name of the obligee (person or entity requiring the bond) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    does_obligee_require_their_own_bond_form_yes: BooleanLike = Field(
        default="", description="Select 'Yes' if the obligee requires use of their own bond form"
    )

    does_obligee_require_their_own_bond_form_no: BooleanLike = Field(
        default="",
        description="Select 'No' if the obligee does not require use of their own bond form",
    )

    obligee_address: str = Field(
        ...,
        description=(
            'Street address of the obligee .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    obligee_city: str = Field(
        ...,
        description=(
            'City of the obligee\'s address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    obligee_state: str = Field(..., description="State of the obligee's address")

    obligee_zip_code: str = Field(..., description="ZIP or postal code of the obligee's address")


class IndemnityAgreementandSignatures(BaseModel):
    """Execution of the indemnity agreement by applicant and indemnitors"""

    day_date_signed: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day of the month on which the agreement is signed"
    )

    month_date_signed: str = Field(
        ...,
        description=(
            "Month in which the agreement is signed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    year_date_signed: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year in which the agreement is signed"
    )

    company_name: str = Field(
        ...,
        description=(
            'Legal name of the applicant company .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    applicant_signature: str = Field(
        ...,
        description=(
            "Signature of the applicant or authorized representative .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    person_authorized_to_sign_for_the_company_print_name: str = Field(
        ...,
        description=(
            "Printed name of the person authorized to sign for the company .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    indemnitor_1_signature: str = Field(
        default="",
        description=(
            'Signature of first indemnitor .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    indemnitor_1_name: str = Field(
        default="",
        description=(
            'Printed name of first indemnitor .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    indemnitor_2_signature: str = Field(
        default="",
        description=(
            'Signature of second indemnitor .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    indemnitor_2_name: str = Field(
        default="",
        description=(
            'Printed name of second indemnitor .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    indemnitor_3_signature: str = Field(
        default="",
        description=(
            'Signature of third indemnitor .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    indemnitor_3_name: str = Field(
        default="",
        description=(
            'Printed name of third indemnitor .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    indemnitor_4_signature: str = Field(
        default="",
        description=(
            'Signature of fourth indemnitor .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    indemnitor_4_name: str = Field(
        default="",
        description=(
            'Printed name of fourth indemnitor .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ContractorsLicenseBondApplication(BaseModel):
    """
    CONTRACTOR'S LICENSE BOND APPLICATION

    Contractor surety bonds, all classes of local and state licenses and permits
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    business_and_principal_history: BusinessandPrincipalHistory = Field(
        ..., description="Business and Principal History"
    )
    bond_and_obligee: BondandObligee = Field(..., description="Bond and Obligee")
    indemnity_agreement_and_signatures: IndemnityAgreementandSignatures = Field(
        ..., description="Indemnity Agreement and Signatures"
    )
