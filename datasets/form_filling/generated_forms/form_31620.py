from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AppraisalDistrictInformation(BaseModel):
    """Information about the appraisal district and tax year"""

    appraisal_districts_name: str = Field(
        ...,
        description=(
            "Name of the appraisal district handling this property .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tax_year: str = Field(
        ...,
        description=(
            "Tax year for which this protest and affidavit apply .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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
    """Contact information for the property owner or lessee"""

    name_of_property_owner_or_lessee: str = Field(
        ...,
        description=(
            "Full legal name of the property owner or lessee .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_city_state_zip_code: str = Field(
        ...,
        description=(
            "Complete mailing address including city, state, and ZIP code .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    phone_number_area_code_and_number: str = Field(
        ...,
        description=(
            "Primary contact phone number including area code .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        default="",
        description=(
            "Email address for contact regarding this protest (will be subject to public "
            'release by consent) .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class Section2PropertyDescription(BaseModel):
    """Location and identifying details of the property"""

    physical_address_city_state_zip_code_if_different_than_above: str = Field(
        default="",
        description=(
            "Physical location of the property, if different from the mailing address .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    if_no_street_address_provide_legal_description: str = Field(
        default="",
        description=(
            "Full legal description of the property if there is no street address .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    mobile_home_make_model_and_identification_number_if_applicable: str = Field(
        default="",
        description=(
            "Make, model, and identification number of the mobile home, if applicable .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Section3ReasonsforProtest(BaseModel):
    """Checkbox reasons and related details for the protest"""

    incorrect_appraised_market_value: BooleanLike = Field(
        default="",
        description="Check if you are protesting that the appraised (market) value is incorrect",
    )

    ag_use_open_space_or_other_special_appraisal_denied_modified_or_cancelled: BooleanLike = Field(
        default="",
        description=(
            "Check if you are protesting denial, modification, or cancellation of an "
            "ag-use, open-space, or other special appraisal"
        ),
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
            "Check if you are protesting a change in use of land that has ag-use, "
            "open-space, or timberland appraisal"
        ),
    )

    property_should_not_be_taxed_in: BooleanLike = Field(
        default="",
        description=(
            "Check if you are protesting that the property should not be taxed in a "
            "particular taxing unit"
        ),
    )

    name_of_taxing_unit: str = Field(
        default="",
        description=(
            "Name of the taxing unit where you believe the property should not be taxed .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    incorrect_appraised_or_market_value_of_land_under_special_appraisal: BooleanLike = Field(
        default="",
        description=(
            "Check if you are protesting the appraised or market value of land under "
            "ag-use, open-space, or other special appraisal"
        ),
    )

    property_not_located_in_this_appraisal_district_or_should_not_be_included_on_record: BooleanLike = Field(
        default="",
        description=(
            "Check if you are protesting that the property is outside this appraisal "
            "district or should not be on its records"
        ),
    )

    owners_name_is_incorrect: BooleanLike = Field(
        default="",
        description="Check if you are protesting that the owner’s name on the record is incorrect",
    )

    failure_to_send_required_notice: BooleanLike = Field(
        default="", description="Check if you are protesting that a required notice was not sent"
    )

    type: str = Field(
        default="",
        description=(
            "Type of required notice that was not sent .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    property_description_is_incorrect: BooleanLike = Field(
        default="",
        description=(
            "Check if you are protesting that the property description on record is incorrect"
        ),
    )

    exemption_was_denied_modified_or_cancelled: BooleanLike = Field(
        default="",
        description=(
            "Check if you are protesting denial, modification, or cancellation of a "
            "property tax exemption"
        ),
    )

    incorrect_damage_assessment_rating_for_temporary_disaster_exemption: BooleanLike = Field(
        default="",
        description=(
            "Check if you are protesting the damage assessment rating for a temporary "
            "disaster exemption"
        ),
    )

    temporary_disaster_damage_exemption_denied_or_modified: BooleanLike = Field(
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


class Section4Evidence(BaseModel):
    """Information about evidence submitted with the affidavit"""

    total_number_of_pages_or_images_submitted_as_evidence: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total count of pages or images attached as evidentiary materials"
    )


class Section5StatementofFactsorArguments(BaseModel):
    """Narrative explanation supporting the protest"""

    statement_of_facts_or_arguments_line_1: str = Field(
        default="",
        description=(
            "First line of your statement of facts or arguments supporting your protest .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    statement_of_facts_or_arguments_line_2: str = Field(
        default="",
        description=(
            "Second line of your statement of facts or arguments supporting your protest "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    statement_of_facts_or_arguments_line_3: str = Field(
        default="",
        description=(
            "Third line of your statement of facts or arguments supporting your protest .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PropertyOwnersAffidavitOfEvidence(BaseModel):
    """
    Property Owner’s Affidavit of Evidence

    GENERAL INSTRUCTIONS: This form is for use by a property owner to offer and submit evidence and/or argument for an appraisal review board (ARB) protest hearing by telephone conference call or written affidavit pursuant to Tax Code Section 41.45.
    FILING INSTRUCTIONS: This affidavit and evidence for the hearing may be submitted to the ARB either in paper or on a small portable electronic device (such as a CD, USB flash drive or thumb drive) which will be kept by the ARB.
    """

    appraisal_district_information: AppraisalDistrictInformation = Field(
        ..., description="Appraisal District Information"
    )
    section_1_property_owner_or_lessee: Section1PropertyOwnerorLessee = Field(
        ..., description="Section 1: Property Owner or Lessee"
    )
    section_2_property_description: Section2PropertyDescription = Field(
        ..., description="Section 2: Property Description"
    )
    section_3_reasons_for_protest: Section3ReasonsforProtest = Field(
        ..., description="Section 3: Reasons for Protest"
    )
    section_4_evidence: Section4Evidence = Field(..., description="Section 4: Evidence")
    section_5_statement_of_facts_or_arguments: Section5StatementofFactsorArguments = Field(
        ..., description="Section 5: Statement of Facts or Arguments"
    )
