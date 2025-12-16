from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class HeaderNoticeInformation(BaseModel):
    """Basic notice details and producer information"""

    date: str = Field(
        ..., description="Date this notice of occurrence/claim is being completed"
    )  # YYYY-MM-DD format

    producer: str = Field(
        ...,
        description=(
            "Name of the insurance producer/agency submitting the notice .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    phone_ac_no_ext: str = Field(
        ...,
        description=(
            "Producer’s telephone number including area code and extension .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    notice_of_occurrence: BooleanLike = Field(
        ..., description="Check if this notice relates to an occurrence"
    )

    notice_of_claim: BooleanLike = Field(..., description="Check if this notice relates to a claim")

    date_of_occurrence_and_time_am: BooleanLike = Field(
        ..., description="Indicate if the time of occurrence is in the AM"
    )

    date_of_occurrence_and_time_pm: BooleanLike = Field(
        ..., description="Indicate if the time of occurrence is in the PM"
    )

    date_of_occurrence_and_time: str = Field(
        ...,
        description=(
            "Date and clock time when the occurrence happened .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_claim: str = Field(..., description="Date the claim was made")  # YYYY-MM-DD format

    previously_reported_yes: BooleanLike = Field(
        ..., description="Indicate YES if this occurrence/claim was previously reported"
    )

    previously_reported_no: BooleanLike = Field(
        ..., description="Indicate NO if this occurrence/claim was not previously reported"
    )


class PolicyInformation(BaseModel):
    """Policy dates, company, and identifying information"""

    effective_date: str = Field(..., description="Policy effective date")  # YYYY-MM-DD format

    expiration_date: str = Field(..., description="Policy expiration date")  # YYYY-MM-DD format

    policy_type: str = Field(
        ...,
        description=(
            "Type of policy (e.g., General Liability, Umbrella) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    retroactive_date: str = Field(
        default="", description="Retroactive date for claims-made coverage, if applicable"
    )  # YYYY-MM-DD format

    company: str = Field(
        ...,
        description=(
            "Name of the insurance company providing coverage .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    naic_code: str = Field(
        default="",
        description=(
            'NAIC code of the insurance company .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    occurrence: BooleanLike = Field(
        ..., description="Check if the policy is written on an occurrence basis"
    )

    claims_made: BooleanLike = Field(
        ..., description="Check if the policy is written on a claims-made basis"
    )

    miscellaneous_info_site_location_code: str = Field(
        default="",
        description=(
            "Miscellaneous information such as site and location codes .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    code: str = Field(
        default="",
        description=(
            'Agency or company code .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    sub_code: str = Field(
        default="",
        description=(
            "Sub code associated with the agency or company .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    policy_number: str = Field(
        ...,
        description=(
            'Insurance policy number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    reference_number: str = Field(
        default="",
        description=(
            "Internal reference or claim number, if any .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    agency: str = Field(
        ...,
        description=(
            "Name of the agency handling the policy .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    customer_id: str = Field(
        default="",
        description=(
            "Customer identification number used by the agency or company .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class InsuredInformation(BaseModel):
    """Insured party identification and address"""

    insured_name_and_address: str = Field(
        ...,
        description=(
            "Full name and mailing address of the insured .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    soc_sec_or_fein: str = Field(
        default="",
        description=(
            "Social Security Number or Federal Employer Identification Number of the "
            'insured .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class ContactInformationforInsured(BaseModel):
    """Contact person for the insured and how/when to reach them"""

    contact_insured_name_and_address: str = Field(
        default="",
        description=(
            "Name and address of the contact person for the insured .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    where_to_contact: str = Field(
        default="",
        description=(
            "Location or method where the contact person can be reached .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    residence_phone_ac_no: str = Field(
        default="",
        description=(
            "Residence phone number for the contact, including area code .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    business_phone_ac_no_ext: str = Field(
        default="",
        description=(
            "Business phone number for the contact, including area code and extension .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    when_to_contact: str = Field(
        default="",
        description=(
            "Preferred times to contact this person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    residence_phone_ac_no_when_to_contact: str = Field(
        default="",
        description=(
            "Residence phone number for the contact during preferred contact times .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    business_phone_ac_no_ext_when_to_contact: str = Field(
        default="",
        description=(
            "Business phone number for the contact during preferred contact times .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class OccurrenceDetails(BaseModel):
    """Location, authorities, and description of the occurrence"""

    location_of_occurrence_include_city_state: str = Field(
        ...,
        description=(
            "Location where the occurrence took place, including city and state .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    authority_contacted: str = Field(
        default="",
        description=(
            "Name of any authority contacted (e.g., police, fire department) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    description_of_occurrence_use_separate_sheet_if_necessary: str = Field(
        ...,
        description=(
            "Detailed description of how the occurrence happened .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CoverageLimits(BaseModel):
    """Policy coverage parts, limits, and umbrella/excess details"""

    coverage_part_or_forms_insert_form_s_and_edition_dates: str = Field(
        default="",
        description=(
            "List applicable coverage parts or forms, including form numbers and edition "
            'dates .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    general_aggregate: Union[float, Literal["N/A", ""]] = Field(
        default="", description="General aggregate limit of liability"
    )

    prod_comp_op_agg: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Products/completed operations aggregate limit"
    )

    pers_adv_inj: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Personal and advertising injury limit"
    )

    each_occurrence: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Each occurrence limit of liability"
    )

    fire_damage: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Fire damage limit (any one fire)"
    )

    medical_expense: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Medical expense limit (any one person)"
    )

    deductible: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Deductible amount applicable to the coverage"
    )

    umbrella: BooleanLike = Field(
        default="", description="Check if the excess coverage is an umbrella policy"
    )

    excess: BooleanLike = Field(
        default="", description="Check if the excess coverage is a straight excess policy"
    )

    carrier: str = Field(
        default="",
        description=(
            'Name of the umbrella/excess carrier .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    limits: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Limit of liability for the umbrella/excess policy"
    )

    aggr: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Aggregate limit for the umbrella/excess policy"
    )

    per_claim_occ: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Per claim or per occurrence limit for the umbrella/excess policy"
    )

    sir_ded: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Self-insured retention or deductible amount for the umbrella/excess policy",
    )

    bi: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Bodily injury limit under the umbrella/excess policy"
    )

    pd: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Property damage limit under the umbrella/excess policy"
    )


class TypeofLiabilityPremises(BaseModel):
    """Premises liability details and ownership"""

    premises_insured_is_owner: BooleanLike = Field(
        default="", description="Check if the insured is the owner of the premises"
    )

    premises_insured_is_tenant: BooleanLike = Field(
        default="", description="Check if the insured is a tenant of the premises"
    )

    premises_insured_is_other: BooleanLike = Field(
        default="", description="Check if the insured has another relationship to the premises"
    )

    other_premises_insured_is: str = Field(
        default="",
        description=(
            "Describe the insured’s relationship to the premises if 'Other' is selected .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    type_of_premises: str = Field(
        default="",
        description=(
            "Description of the type of premises involved .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    owners_name_address_if_not_insured: str = Field(
        default="",
        description=(
            "Name and address of the premises owner if different from the insured .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    owners_phone_ac_no_ext: str = Field(
        default="",
        description=(
            "Phone number of the premises owner, including area code and extension .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class TypeofLiabilityProducts(BaseModel):
    """Products liability details and manufacturer/vendor information"""

    products_insured_is_manufacturer: BooleanLike = Field(
        default="", description="Check if the insured is the manufacturer of the product"
    )

    products_insured_is_vendor: BooleanLike = Field(
        default="", description="Check if the insured is a vendor of the product"
    )

    products_insured_is_other: BooleanLike = Field(
        default="", description="Check if the insured has another relationship to the product"
    )

    other_products_insured_is: str = Field(
        default="",
        description=(
            "Describe the insured’s relationship to the product if 'Other' is selected .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    type_of_product: str = Field(
        default="",
        description=(
            'Description of the product involved .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    manufacturers_name_address_if_not_insured: str = Field(
        default="",
        description=(
            "Name and address of the manufacturer if different from the insured .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    manufact_phone_ac_no_ext: str = Field(
        default="",
        description=(
            "Phone number of the manufacturer, including area code and extension .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    where_can_product_be_seen: str = Field(
        default="",
        description=(
            "Location where the product involved can be inspected .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class OtherLiability(BaseModel):
    """Other liability including completed operations"""

    other_liability_including_completed_operations_explain: str = Field(
        default="",
        description=(
            "Explain any other liability exposures, including completed operations .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class InjuredPersonPropertyDamaged(BaseModel):
    """Details of injured party and/or damaged property"""

    name_address_injured_owner: str = Field(
        ...,
        description=(
            "Name and address of the injured person or property owner .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_ac_no_ext_injured_owner: str = Field(
        default="",
        description=(
            "Phone number of the injured person or property owner .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    age: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age of the injured person"
    )

    sex: str = Field(
        default="",
        description=(
            'Sex of the injured person .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    occupation: str = Field(
        default="",
        description=(
            'Occupation of the injured person .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    employers_name_address: str = Field(
        default="",
        description=(
            "Name and address of the injured person’s employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_ac_no_ext_employer: str = Field(
        default="",
        description=(
            "Employer’s phone number, including area code and extension .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    describe_injury: str = Field(
        default="",
        description=(
            'Description of the injury sustained .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    where_taken: str = Field(
        default="",
        description=(
            "Location where the injured person was taken (e.g., hospital name) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    what_was_injured_doing: str = Field(
        default="",
        description=(
            "Activity the injured person was engaged in at the time of injury .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    fatality: BooleanLike = Field(
        default="", description="Indicate if the injury resulted in a fatality"
    )

    describe_property_type_model_etc: str = Field(
        default="",
        description=(
            "Description of damaged property, including type and model .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    estimate_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated amount of property damage"
    )

    where_can_property_be_seen: str = Field(
        default="",
        description=(
            "Location where the damaged property can be inspected .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    when_can_property_be_seen: str = Field(
        default="",
        description=(
            "Times when the damaged property can be inspected .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Witnesses(BaseModel):
    """Witness contact information"""

    witnesses_name_address: str = Field(
        default="",
        description=(
            'Name and address of any witnesses .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    business_phone_ac_no_ext_witness: str = Field(
        default="",
        description=(
            "Business phone number of the witness, including area code and extension .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    residence_phone_ac_no_witness: str = Field(
        default="",
        description=(
            "Residence phone number of the witness, including area code .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class RemarksandSignatures(BaseModel):
    """Additional remarks and reporting/signature information"""

    remarks: str = Field(
        default="",
        description=(
            "Additional remarks or information relevant to the occurrence/claim .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reported_by: str = Field(
        ...,
        description=(
            "Name of the person reporting the occurrence/claim .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reported_to: str = Field(
        ...,
        description=(
            "Name of the person or organization to whom the occurrence/claim was reported "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    signature_of_insured: str = Field(
        ...,
        description=(
            "Signature of the insured attesting to the accuracy of the information .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    signature_of_producer: str = Field(
        default="",
        description=(
            "Signature of the producer/agent submitting the notice .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AcordGeneralLiabilityNoticeOfOccurrenceclaim(BaseModel):
    """
    ACORD™ GENERAL LIABILITY NOTICE OF OCCURRENCE/CLAIM

    ''
    """

    header__notice_information: HeaderNoticeInformation = Field(
        ..., description="Header / Notice Information"
    )
    policy_information: PolicyInformation = Field(..., description="Policy Information")
    insured_information: InsuredInformation = Field(..., description="Insured Information")
    contact_information_for_insured: ContactInformationforInsured = Field(
        ..., description="Contact Information for Insured"
    )
    occurrence_details: OccurrenceDetails = Field(..., description="Occurrence Details")
    coverage__limits: CoverageLimits = Field(..., description="Coverage / Limits")
    type_of_liability___premises: TypeofLiabilityPremises = Field(
        ..., description="Type of Liability - Premises"
    )
    type_of_liability___products: TypeofLiabilityProducts = Field(
        ..., description="Type of Liability - Products"
    )
    other_liability: OtherLiability = Field(..., description="Other Liability")
    injured_person__property_damaged: InjuredPersonPropertyDamaged = Field(
        ..., description="Injured Person / Property Damaged"
    )
    witnesses: Witnesses = Field(..., description="Witnesses")
    remarks_and_signatures: RemarksandSignatures = Field(..., description="Remarks and Signatures")
