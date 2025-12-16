from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RecordingReferenceInformation(BaseModel):
    """Return address and basic permit/tax reference details"""

    after_recording_return_to_line_1: str = Field(
        default="",
        description=(
            "First line of the name or address where the recorded document should be "
            'returned .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    after_recording_return_to_line_2: str = Field(
        default="",
        description=(
            "Second line of the name or address where the recorded document should be "
            'returned .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    after_recording_return_to_line_3: str = Field(
        default="",
        description=(
            "Third line of the name or address where the recorded document should be "
            'returned .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    after_recording_return_to_line_4: str = Field(
        default="",
        description=(
            "Fourth line of the name or address where the recorded document should be "
            'returned .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    permit_no: str = Field(
        default="",
        description=(
            "Permit number associated with this notice of commencement .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tax_folio_or_alternate_key: str = Field(
        default="",
        description=(
            "Tax folio number or alternate key number for the property .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PropertyImprovementInformation(BaseModel):
    """Description of the property and the work to be performed"""

    description_of_property_line_1: str = Field(
        ...,
        description=(
            "First line of the legal description of the property .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    description_of_property_line_2: str = Field(
        default="",
        description=(
            "Second line of the legal description of the property .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    description_of_property_line_3: str = Field(
        default="",
        description=(
            "Third line of the legal description of the property .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    description_of_property_line_4: str = Field(
        default="",
        description=(
            "Fourth line of the legal description of the property .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    street_address: str = Field(
        ...,
        description=(
            "Street address of the property, if available .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    general_description_of_improvement_line_1: str = Field(
        ...,
        description=(
            "First line describing the general nature of the improvement .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    general_description_of_improvement_line_2: str = Field(
        default="",
        description=(
            "Second line describing the general nature of the improvement .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class OwnerTitleInformation(BaseModel):
    """Owner details and interest in the property"""

    owners_name: str = Field(
        ...,
        description=(
            'Full legal name of the property owner .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    owners_address: str = Field(
        ...,
        description=(
            'Mailing address of the property owner .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    interest_in_property: str = Field(
        ...,
        description=(
            "Description of the owner's interest in the property (e.g., fee simple, "
            'leasehold) .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    fee_simple_titleholder_name_and_address_if_other_than_owner: str = Field(
        default="",
        description=(
            "Name and address of the fee simple titleholder if different from the owner .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ContractorSuretyLenderInformation(BaseModel):
    """Parties involved in construction, bonding, and financing"""

    contractor_name: str = Field(
        ...,
        description=(
            "Name of the contractor for the improvement .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contractor_address: str = Field(
        ...,
        description=(
            'Mailing address of the contractor .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contractor_telephone_no: str = Field(
        ...,
        description=(
            "Primary telephone number for the contractor .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contractor_fax_no_opt: str = Field(
        default="",
        description=(
            "Fax number for the contractor (optional) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    surety_name: str = Field(
        default="",
        description=(
            'Name of the surety company, if any .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    surety_address: str = Field(
        default="",
        description=(
            'Mailing address of the surety company .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    surety_telephone_no: str = Field(
        default="",
        description=(
            "Primary telephone number for the surety company .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    surety_fax_no_opt: str = Field(
        default="",
        description=(
            "Fax number for the surety company (optional) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    amount_of_bond: str = Field(
        default="",
        description=(
            "Total amount of the surety bond, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    lender_name: str = Field(
        default="",
        description=(
            "Name of the lender providing financing, if any .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    lender_address: str = Field(
        default="",
        description=(
            'Mailing address of the lender .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    lender_telephone_no: str = Field(
        default="",
        description=(
            "Primary telephone number for the lender .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    lender_fax_no_opt: str = Field(
        default="",
        description=(
            'Fax number for the lender (optional) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class NoticeDesigneesforService(BaseModel):
    """Persons designated to receive notices and lienor communications"""

    designated_person_name_for_service_of_notices: str = Field(
        default="",
        description=(
            "Name of the person in Florida designated by the owner to receive notices or "
            'documents .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    designated_person_address_for_service_of_notices: str = Field(
        default="",
        description=(
            "Mailing address of the designated person for service of notices .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    designated_person_telephone_no_for_service_of_notices: str = Field(
        default="",
        description=(
            "Telephone number of the designated person for service of notices .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    designated_person_fax_no_opt_for_service_of_notices: str = Field(
        default="",
        description=(
            "Fax number of the designated person for service of notices (optional) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    additional_designee_name: str = Field(
        default="",
        description=(
            "Name of the additional person designated by the owner to receive lienor's "
            'notices .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    additional_designee_of: str = Field(
        default="",
        description=(
            'Affiliation or company of the additional designee ("of" field) .If you '
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    additional_designee_full_name: str = Field(
        default="",
        description=(
            "Name of the additional designee as repeated in the contact section .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    additional_designee_address: str = Field(
        default="",
        description=(
            "Mailing address of the additional designee .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    additional_designee_telephone_no: str = Field(
        default="",
        description=(
            "Telephone number of the additional designee .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    additional_designee_fax_no_opt: str = Field(
        default="",
        description=(
            "Fax number of the additional designee (optional) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    expiration_date_of_notice_of_commencement: str = Field(
        ...,
        description=(
            "Expiration date of this notice of commencement (defaults to 1 year from "
            "recording if not specified)"
        ),
    )  # YYYY-MM-DD format


class OwnerExecution(BaseModel):
    """Owner or authorized signatory execution of the notice"""

    owner_or_authorized_signatory_signature: str = Field(
        ...,
        description=(
            "Signature of the owner or authorized representative executing the notice .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    printed_name_and_signatory_title_office: str = Field(
        ...,
        description=(
            "Printed name of the signatory and their title or office .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class NotaryAcknowledgment(BaseModel):
    """Notarial acknowledgment of the owner's signature"""

    day_of_acknowledgment: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day of the month on which the notary acknowledgment is made"
    )

    month_of_acknowledgment: str = Field(
        ...,
        description=(
            "Month in which the notary acknowledgment is made .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    year_of_acknowledgment: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year in which the notary acknowledgment is made"
    )

    name_of_person_acknowledged: str = Field(
        ...,
        description=(
            "Name of the person whose signature is being acknowledged by the notary .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    personally_known_to_me: BooleanLike = Field(
        ..., description="Indicates that the signer is personally known to the notary"
    )

    has_produced_identification: BooleanLike = Field(
        ..., description="Indicates that the signer produced identification to the notary"
    )

    type_of_identification_produced: str = Field(
        default="",
        description=(
            "Type of identification presented to the notary (e.g., driver's license, "
            'passport) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    who_did_take_an_oath: BooleanLike = Field(
        ..., description="Indicates that the signer took an oath before the notary"
    )

    who_did_not_take_an_oath: BooleanLike = Field(
        ..., description="Indicates that the signer did not take an oath before the notary"
    )

    signature_of_notary_public_state_of_florida: str = Field(
        ...,
        description=(
            "Signature of the Florida notary public .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    commissioned_name_of_notary_public: str = Field(
        ...,
        description=(
            "Commissioned name of the notary public, printed, typed, or stamped .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PerjuryVerification(BaseModel):
    """Owner’s verification under penalties of perjury"""

    signature_of_natural_person_owner_signing_above: str = Field(
        ...,
        description=(
            "Signature of the natural person owner verifying the truth of the information "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class NoticeOfCommencement(BaseModel):
    """
    NOTICE OF COMMENCEMENT

    The undersigned hereby gives notice that improvement will be made to certain real property, and in accordance with Chapter 713, Florida Statutes, the following information is provided in this Notice of Commencement.
    """

    recording__reference_information: RecordingReferenceInformation = Field(
        ..., description="Recording & Reference Information"
    )
    property__improvement_information: PropertyImprovementInformation = Field(
        ..., description="Property & Improvement Information"
    )
    owner__title_information: OwnerTitleInformation = Field(
        ..., description="Owner & Title Information"
    )
    contractor_surety__lender_information: ContractorSuretyLenderInformation = Field(
        ..., description="Contractor, Surety & Lender Information"
    )
    notice__designees_for_service: NoticeDesigneesforService = Field(
        ..., description="Notice & Designees for Service"
    )
    owner_execution: OwnerExecution = Field(..., description="Owner Execution")
    notary_acknowledgment: NotaryAcknowledgment = Field(..., description="Notary Acknowledgment")
    perjury_verification: PerjuryVerification = Field(..., description="Perjury Verification")
