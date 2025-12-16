from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CouncilMembershipInformation(BaseModel):
    """Information about the council and membership record for this transaction"""

    new_receiving_council_number: str = Field(
        ...,
        description=(
            "New or receiving council number for this membership transaction .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    council_location_city_st_prov: str = Field(
        ...,
        description=(
            "City and state/province of the new or receiving council .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    membership_number: str = Field(
        default="",
        description=(
            "Existing membership number, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_read: str = Field(
        default="", description="Date the application was read at council"
    )  # YYYY-MM-DD format

    date_elected: str = Field(
        default="", description="Date the applicant was elected to membership"
    )  # YYYY-MM-DD format

    first_degree_date: str = Field(
        default="", description="Date of the First Degree exemplification"
    )  # YYYY-MM-DD format


class TransactionType(BaseModel):
    """Type of membership transaction being processed"""

    transaction_new_member: BooleanLike = Field(
        ..., description="Check if this transaction is for a new member"
    )

    transaction_juvenile_to_adult: BooleanLike = Field(
        default="",
        description="Check if this transaction converts a juvenile member to adult status",
    )

    transaction_reinstatement_up_to_3_months: BooleanLike = Field(
        default="", description="Check if this is a reinstatement within 3 months of suspension"
    )

    transaction_reactivation_inactive_insurance: BooleanLike = Field(
        default="", description="Check if this is a reactivation of an inactive insurance member"
    )

    transaction_readmission_up_to_7_years: BooleanLike = Field(
        default="", description="Check if this is a readmission within 7 years"
    )

    transaction_reapplication_over_7_years: BooleanLike = Field(
        default="", description="Check if this is a reapplication after more than 7 years"
    )

    transaction_transfer_in: BooleanLike = Field(
        default="", description="Check if this transaction is a transfer into this council"
    )

    transaction_data_change: BooleanLike = Field(
        default="", description="Check if this transaction is only to change member data"
    )

    transaction_suspension_reason: str = Field(
        default="",
        description=(
            "Check if this is a suspension and specify the reason .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    transaction_death: BooleanLike = Field(
        default="", description="Check if this transaction records the member's death"
    )

    transaction_next_of_kin: BooleanLike = Field(
        default="", description="Check if next of kin information is being provided"
    )


class ApplicantPersonalInformation(BaseModel):
    """Basic personal and contact information for the applicant"""

    last_name: str = Field(
        ...,
        description=(
            'Applicant\'s last name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Applicant\'s first name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    middle_initial: str = Field(
        default="",
        description=(
            'Applicant\'s middle initial .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    title: str = Field(
        default="",
        description=(
            "Applicant's title (e.g., Jr., Sr., III) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    street: str = Field(
        ...,
        description=(
            'Applicant\'s street address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'Applicant\'s city .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    st_prov: str = Field(..., description="Applicant's state or province abbreviation")

    postal_code: str = Field(..., description="Applicant's postal or ZIP code")

    country_outside_us: str = Field(
        default="",
        description=(
            "Country of residence if outside the United States .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mo: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month of application or event (two digits)"
    )

    day: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day of application or event (two digits)"
    )

    yr: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year of application or event (four digits)"
    )

    date_of_birth: str = Field(..., description="Applicant's date of birth")  # YYYY-MM-DD format

    marital_status: str = Field(
        default="",
        description=(
            'Applicant\'s marital status .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    home_phone: str = Field(
        default="",
        description=(
            'Applicant\'s home telephone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    business_phone: str = Field(
        default="",
        description=(
            "Applicant's business or work telephone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        default="",
        description=(
            'Applicant\'s mobile/cell phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
        default="",
        description=(
            'Applicant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    occupation_employer: str = Field(
        default="",
        description=(
            'Applicant\'s occupation and employer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    last_four_digits_of_tax_id: str = Field(
        default="",
        description="Last four digits of applicant's tax identification number (SSN, SIN, etc.)",
    )


class SurvivorNextofKinInformation(BaseModel):
    """Contact and relationship details for survivor or next of kin"""

    relationship: str = Field(
        default="",
        description=(
            "Relationship of survivor/next of kin to the member .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_survivor: str = Field(
        default="",
        description=(
            "Telephone number of the survivor/next of kin .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    street_survivor: str = Field(
        default="",
        description=(
            "Street address of the survivor/next of kin .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_survivor: str = Field(
        default="",
        description=(
            'City of the survivor/next of kin .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    st_prov_survivor: str = Field(
        default="", description="State or province of the survivor/next of kin"
    )

    postal_code_survivor: str = Field(
        default="", description="Postal or ZIP code of the survivor/next of kin"
    )


class ReligiousParishInformation(BaseModel):
    """Information about Catholic practice and parish affiliation"""

    practical_catholic_yes: BooleanLike = Field(
        ...,
        description=(
            "Select YES if the applicant is a practical or practicing Catholic in union "
            "with the Holy See"
        ),
    )

    practical_catholic_no: BooleanLike = Field(
        ...,
        description=(
            "Select NO if the applicant is not a practical or practicing Catholic in union "
            "with the Holy See"
        ),
    )

    parish_name_location_city_st_prov: str = Field(
        default="",
        description=(
            "Name of parish and its city and state/province .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PriorMembershipHistory(BaseModel):
    """Information about previous council membership and initiation history"""

    former_council_member_yes: BooleanLike = Field(
        default="", description="Select YES if the applicant was previously a council member"
    )

    former_council_member_no: BooleanLike = Field(
        default="", description="Select NO if the applicant was not previously a council member"
    )

    applied_previously_yes: BooleanLike = Field(
        default="", description="Select YES if the applicant has applied for membership before"
    )

    applied_previously_no: BooleanLike = Field(
        default="", description="Select NO if the applicant has not applied for membership before"
    )

    initiation_date_first: str = Field(
        default="", description="Date of First Degree initiation"
    )  # YYYY-MM-DD format

    initiation_date_second: str = Field(
        default="", description="Date of Second Degree initiation"
    )  # YYYY-MM-DD format

    initiation_date_third: str = Field(
        default="", description="Date of Third Degree initiation"
    )  # YYYY-MM-DD format

    initiation_date_fourth: str = Field(
        default="", description="Date of Fourth Degree initiation"
    )  # YYYY-MM-DD format

    date_of_termination: str = Field(
        default="", description="Date the previous membership was terminated"
    )  # YYYY-MM-DD format

    termination_reason: str = Field(
        default="",
        description=(
            "Reason for termination of previous membership .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    number_of_last_council: str = Field(
        default="",
        description=(
            "Council number of the member's last council .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    council_location_last_council: str = Field(
        default="",
        description=(
            "City and state/province of the member's last council .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProposerInformation(BaseModel):
    """Information about the member proposing the applicant"""

    printed_name_of_proposer: str = Field(
        ...,
        description=(
            "Printed name of the member proposing the applicant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    proposers_member_number: str = Field(
        ...,
        description=(
            'Membership number of the proposer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class SignaturesApprovals(BaseModel):
    """Applicant and council officer signatures and approval date"""

    signature_of_applicant: str = Field(
        ...,
        description=(
            "Applicant's signature affirming the declaration .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    officer_signatures_date: str = Field(
        ..., description="Date the financial secretary and grand knight signed"
    )  # YYYY-MM-DD format

    financial_secretary_signature: str = Field(
        ...,
        description=(
            'Signature of the financial secretary .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    grand_knight_signature: str = Field(
        ...,
        description=(
            'Signature of the grand knight .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class KnightsOfColumbusMembershipDocument(BaseModel):
    """
        KNIGHTS OF COLUMBUS
    Membership Document

        The member and officers' signatures are required for this form to be processed. Please complete this form legibly.
    """

    council__membership_information: CouncilMembershipInformation = Field(
        ..., description="Council & Membership Information"
    )
    transaction_type: TransactionType = Field(..., description="Transaction Type")
    applicant_personal_information: ApplicantPersonalInformation = Field(
        ..., description="Applicant Personal Information"
    )
    survivor__next_of_kin_information: SurvivorNextofKinInformation = Field(
        ..., description="Survivor / Next of Kin Information"
    )
    religious__parish_information: ReligiousParishInformation = Field(
        ..., description="Religious & Parish Information"
    )
    prior_membership_history: PriorMembershipHistory = Field(
        ..., description="Prior Membership History"
    )
    proposer_information: ProposerInformation = Field(..., description="Proposer Information")
    signatures__approvals: SignaturesApprovals = Field(..., description="Signatures & Approvals")
