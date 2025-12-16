from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class GeneralInformation11(BaseModel):
    """General details about the trust and settlor"""

    full_name_of_the_trust: str = Field(
        ...,
        description=(
            "Registered full legal name of the trust .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    full_business_name_of_the_trustee_in_respect_of_the_trust_if_any: str = Field(
        default="",
        description=(
            "Full business or trading name of the trustee, if applicable .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    country_where_trust_established_if_not_established_in_australia: str = Field(
        default="",
        description=(
            "Country in which the trust was originally established, if outside Australia "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    full_name_of_settlors: str = Field(
        ...,
        description=(
            "Full name(s) of the person or people who settled the initial sum or assets to "
            'create the trust .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class TypeofUnregulatedTrust12(BaseModel):
    """Selection of the trust type"""

    family_trust: BooleanLike = Field(..., description="Select if the trust is a family trust")

    charitable_trust: BooleanLike = Field(
        ..., description="Select if the trust is a charitable trust"
    )

    testamentary_trust: BooleanLike = Field(
        ..., description="Select if the trust is a testamentary trust"
    )

    other_type_provide_description: str = Field(
        default="",
        description=(
            "Description of the trust type if it is not family, charitable, or testamentary "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class BeneficiariesDetails13(BaseModel):
    """Named beneficiaries and classes of beneficiaries"""

    full_given_entity_names_1: str = Field(
        default="",
        description=(
            "First named beneficiary’s full given or entity name .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    surname_1: str = Field(
        default="",
        description=(
            'First named beneficiary’s surname .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    full_given_entity_names_2: str = Field(
        default="",
        description=(
            "Second named beneficiary’s full given or entity name .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    surname_2: str = Field(
        default="",
        description=(
            'Second named beneficiary’s surname .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    full_given_entity_names_3: str = Field(
        default="",
        description=(
            "Third named beneficiary’s full given or entity name .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    surname_3: str = Field(
        default="",
        description=(
            'Third named beneficiary’s surname .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    full_given_entity_names_4: str = Field(
        default="",
        description=(
            "Fourth named beneficiary’s full given or entity name .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    surname_4: str = Field(
        default="",
        description=(
            'Fourth named beneficiary’s surname .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    classes_of_beneficiaries: str = Field(
        default="",
        description=(
            "Description of the class or classes of beneficiaries (e.g. unit holders, "
            "family members, charitable organisations/causes) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    more_beneficiaries_box: BooleanLike = Field(
        default="", description="Tick if additional beneficiaries are listed on a separate sheet"
    )


class pythonFscJfaUnregulatedForeignTrustsIdentificationForm(BaseModel):
    """
        FSC
    FINANCIAL SERVICES COUNCIL

    JFA
    FINANCIAL PLANNING ASSOCIATION OF AUSTRALIA

    IDENTIFICATION FORM
    UNREGULATED AUSTRALIAN TRUSTS & FOREIGN TRUSTS

        This form is for all Trusts that are not subject to the oversight of an Australian statutory regulator. Trusts that are subject to the oversight of an Australian statutory regulator, including Self-Managed Superannuation Funds, should complete the AUSTRALIAN REGULATED TRUSTS AND TRUSTEES IDENTIFICATION FORM. Provide information about the Trust (Section 1) and complete the Trust verification procedure (Section 3). Provide details for ALL Trustees (Section 1.4) and provide a separate Customer ID Form for ONE of the Trustees. Provide details for the Trust's Beneficial Owners (Section 1.5) and provide separate INDIVIDUAL ID Forms for each of these Beneficial Owners. Tax information must be collected from an authorised representative of the Trust.
    """

    general_information: GeneralInformation11 = Field(..., description="1.1 General Information")
    type_of_unregulated_trust: TypeofUnregulatedTrust12 = Field(
        ..., description="1.2 Type of Unregulated Trust"
    )
    beneficiaries_details: BeneficiariesDetails13 = Field(
        ..., description="1.3 Beneficiaries Details"
    )
