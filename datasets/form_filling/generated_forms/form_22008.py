from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class HeaderInformation(BaseModel):
    """Appraisal district identification and tax year"""

    appraisal_districts_name: str = Field(
        ...,
        description=(
            "Name of the appraisal district where the property is taxed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tax_year: str = Field(
        ...,
        description=(
            "Tax year for which this protest is being filed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    appraisal_district_account_number_if_known: str = Field(
        default="",
        description=(
            "Appraisal district account number for the property, if available .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Section1PropertyOwnerorLessee(BaseModel):
    """Information about the property owner or lessee and special status"""

    person_age_65_or_older: BooleanLike = Field(
        default="", description="Check if the property owner or lessee is age 65 or older"
    )

    disabled_person: BooleanLike = Field(
        default="", description="Check if the property owner or lessee is a disabled person"
    )

    military_service_member: BooleanLike = Field(
        default="",
        description="Check if the property owner or lessee is an active military service member",
    )

    military_veteran: BooleanLike = Field(
        default="", description="Check if the property owner or lessee is a military veteran"
    )

    spouse_of_a_military_service_member_or_veteran: BooleanLike = Field(
        default="",
        description="Check if the filer is the spouse of a military service member or veteran",
    )

    name_of_property_owner_or_lessee: str = Field(
        ...,
        description=(
            "Full legal name of the property owner or lessee filing the protest .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    mailing_address_city_state_zip_code: str = Field(
        ...,
        description=(
            "Mailing address including city, state, and ZIP code for correspondence .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    phone_number_area_code_and_number: str = Field(
        default="",
        description=(
            "Primary contact phone number including area code .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        default="",
        description=(
            "Email address for electronic communication (will be subject to public "
            'information laws) .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class Section2PropertyDescription(BaseModel):
    """Location and description of the property being protested"""

    physical_address_city_state_zip_code_if_different_than_above: str = Field(
        default="",
        description=(
            "Physical location of the property, if different from the mailing address .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    legal_description_if_no_street_address: str = Field(
        default="",
        description=(
            "Full legal description of the property if there is no street address .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    mobile_home_make_model_and_identification_if_applicable: str = Field(
        default="",
        description=(
            "Make, model, and identification number of the mobile home, if applicable .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Section3ReasonsforProtest(BaseModel):
    """Specific reasons and issues being protested"""

    incorrect_appraised_market_value: BooleanLike = Field(
        default="",
        description="Check if you are protesting that the appraised (market) value is incorrect",
    )

    ag_use_open_space_or_other_special_appraisal_was_denied_modified_or_cancelled: BooleanLike = (
        Field(
            default="",
            description=(
                "Check if you are protesting denial, modification, or cancellation of an "
                "ag-use, open-space, or other special appraisal"
            ),
        )
    )

    value_is_unequal_compared_with_other_properties: BooleanLike = Field(
        default="",
        description=(
            "Check if you are protesting that the property value is unequal compared with "
            "similar properties"
        ),
    )

    change_in_use_of_land_appraised_as_ag_use_open_space_or_timberland: BooleanLike = Field(
        default="",
        description=(
            "Check if you are protesting a change in use of land that was appraised as "
            "ag-use, open-space, or timberland"
        ),
    )

    property_should_not_be_taxed_in_taxing_unit: str = Field(
        default="",
        description=(
            "Name of the taxing unit where you believe the property should not be taxed .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    incorrect_appraised_or_market_value_of_land_under_special_appraisal_for_ag_use_open_space_or_other_special_appraisal: BooleanLike = Field(
        default="",
        description=(
            "Check if you are protesting the appraised or market value of land under a "
            "special appraisal (ag-use, open-space, etc.)"
        ),
    )

    property_is_not_located_in_this_appraisal_district_or_otherwise_should_not_be_included_on_the_appraisal_districts_record: BooleanLike = Field(
        default="",
        description=(
            "Check if the property is not in this appraisal district or should not appear "
            "on its records"
        ),
    )

    owners_name_is_incorrect: BooleanLike = Field(
        default="", description="Check if the owner’s name on the appraisal records is incorrect"
    )

    failure_to_send_required_notice_type: str = Field(
        default="",
        description=(
            "Describe the type of required notice that was not sent .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    property_description_is_incorrect: BooleanLike = Field(
        default="", description="Check if the property description on record is incorrect"
    )

    exemption_was_denied_modified_or_cancelled: BooleanLike = Field(
        default="",
        description=(
            "Check if you are protesting denial, modification, or cancellation of an exemption"
        ),
    )

    incorrect_damage_assessment_rating_for_a_property_qualified_for_a_temporary_disaster_exemption: BooleanLike = Field(
        default="",
        description=(
            "Check if you are protesting the damage assessment rating for a temporary "
            "disaster exemption"
        ),
    )

    temporary_disaster_damage_exemption_was_denied_or_modified: BooleanLike = Field(
        default="",
        description=(
            "Check if you are protesting denial or modification of a temporary disaster "
            "damage exemption"
        ),
    )

    other_reason_for_protest: str = Field(
        default="",
        description=(
            "Describe any other reason for your protest not listed above .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class Section4AdditionalFacts(BaseModel):
    """Opinion of value and supporting facts for the protest"""

    opinion_of_propertys_value: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Your opinion of the property’s value in dollars"
    )

    additional_facts_line_1: str = Field(
        default="",
        description=(
            "First line of additional facts supporting your protest .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_facts_line_2: str = Field(
        default="",
        description=(
            "Second line of additional facts supporting your protest .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_facts_line_3: str = Field(
        default="",
        description=(
            "Third line of additional facts supporting your protest .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PropertyOwnersNoticeOfProtest(BaseModel):
    """
    Property Owner’s Notice of Protest

    GENERAL INFORMATION: This form is used for a property owner or an owner’s designated agent to file a protest with the appraisal review board (ARB) pursuant to Tax Code Section 41.41. Lessees contractually obligated to reimburse a property owner for property taxes may be entitled to protest as a lessee if all Tax Code requirements are met, including those in Tax Code Section 41.413.
    FILING INSTRUCTIONS: This document and all supporting documentation must be filed with the appraisal district office in the county in which the property is taxable. Do not file this document with the Texas Comptroller of Public Accounts.
    """

    header_information: HeaderInformation = Field(..., description="Header Information")
    section_1_property_owner_or_lessee: Section1PropertyOwnerorLessee = Field(
        ..., description="Section 1: Property Owner or Lessee"
    )
    section_2_property_description: Section2PropertyDescription = Field(
        ..., description="Section 2: Property Description"
    )
    section_3_reasons_for_protest: Section3ReasonsforProtest = Field(
        ..., description="Section 3: Reasons for Protest"
    )
    section_4_additional_facts: Section4AdditionalFacts = Field(
        ..., description="Section 4: Additional Facts"
    )
