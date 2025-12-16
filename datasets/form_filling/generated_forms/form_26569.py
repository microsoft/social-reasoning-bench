from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Section1OrganisationType(BaseModel):
    """Select the type of organisation applying for an account"""

    ltd_company: BooleanLike = Field(
        ..., description="Tick if the organisation type is a limited company"
    )

    partnership: BooleanLike = Field(
        ..., description="Tick if the organisation type is a partnership"
    )

    trust: BooleanLike = Field(..., description="Tick if the organisation type is a trust")

    sole_trader: BooleanLike = Field(
        ..., description="Tick if the organisation type is a sole trader"
    )

    other_please_specify: str = Field(
        default="",
        description=(
            "If organisation type is not listed, specify the type here .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Section2ParticularsofPurchaserLTDCompanyPartnershiporTrust(BaseModel):
    """Organisation and contact details for companies, partnerships or trusts"""

    organisation_name: str = Field(
        ...,
        description=(
            'Legal name of the organisation .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    abn_number: str = Field(
        ...,
        description=(
            "Australian Business Number (ABN) of the organisation .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    trading_name_if_different: str = Field(
        default="",
        description=(
            "Trading name used if different from the organisation name .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    nature_of_business: str = Field(
        ...,
        description=(
            "Brief description of the organisation's main business activities .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    full_name: str = Field(
        ...,
        description=(
            "Full name of the person acting on behalf of the organisation .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    position_in_organisation: str = Field(
        ...,
        description=(
            "Job title or role of the person within the organisation .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
        ...,
        description=(
            "Email address of the person acting on behalf of the organisation .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    mobile: str = Field(
        ...,
        description=(
            "Mobile phone number of the person acting on behalf of the organisation .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    contact_name: str = Field(
        ...,
        description=(
            "Name of the primary contact in the accounts department .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_number: str = Field(
        ...,
        description=(
            "Telephone number for the accounts department contact .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            "Email address for the accounts department .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    special_instructions_ie_working_hours_etc: str = Field(
        default="",
        description=(
            "Any special instructions for deliveries or accounts (e.g. working hours) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    branches_and_related_delivery_address_expected_to_order: str = Field(
        default="",
        description=(
            "List branches and their delivery addresses that are expected to place orders "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class Section3ParticularsofPurchaserSoleTrader(BaseModel):
    """Personal and business details for sole traders"""

    first_name: str = Field(
        ...,
        description=(
            'First name of the sole trader .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    middle_names: str = Field(
        default="",
        description=(
            "Middle name or names of the sole trader .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            "Family name or surname of the sole trader .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(
        ..., description="Date of birth of the sole trader"
    )  # YYYY-MM-DD format

    occupation: str = Field(
        ...,
        description=(
            "Occupation or main work of the sole trader .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address_sole_trader: str = Field(
        ...,
        description=(
            'Email address of the sole trader .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    trading_name_if_applicable: str = Field(
        default="",
        description=(
            "Trading name used by the sole trader, if any .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    abn_number_sole_trader: str = Field(
        ...,
        description=(
            "Australian Business Number (ABN) associated with the sole trader .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    registration_date: str = Field(
        default="", description="Date the ABN or business name was registered"
    )  # YYYY-MM-DD format

    individuals_relationship_to_abn: str = Field(
        ...,
        description=(
            "Describe the individual's relationship to the ABN (e.g. owner, partner) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AccountApplicationForm(BaseModel):
    """
    Account Application Form

    ''
    """

    section_1_organisation_type: Section1OrganisationType = Field(
        ..., description="Section 1: Organisation Type"
    )
    section_2_particulars_of_purchaser_ltd_company_partnership_or_trust: Section2ParticularsofPurchaserLTDCompanyPartnershiporTrust = Field(
        ..., description="Section 2: Particulars of Purchaser (LTD Company, Partnership or Trust)"
    )
    section_3_particulars_of_purchaser_sole_trader: Section3ParticularsofPurchaserSoleTrader = (
        Field(..., description="Section 3: Particulars of Purchaser (Sole Trader)")
    )
