from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class GeneralInformation(BaseModel):
    """Basic claim and agency details at the top of the form"""

    date_mm_dd_yyyy: str = Field(
        ..., description="Date the property loss notice is completed"
    )  # YYYY-MM-DD format

    agency: str = Field(
        ...,
        description=(
            "Name of the agency submitting the loss notice .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    insured_location_code: str = Field(
        default="",
        description=(
            "Internal code identifying the insured location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_loss_and_time: str = Field(
        ...,
        description=(
            'Date and time when the loss occurred .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_of_loss_and_time_am: BooleanLike = Field(
        ..., description="Check if the time of loss is in the AM"
    )

    date_of_loss_and_time_pm: BooleanLike = Field(
        ..., description="Check if the time of loss is in the PM"
    )

    property_home_policy_carrier: str = Field(
        ...,
        description=(
            "Name of the carrier for the property/home policy .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    property_home_policy_naic_code: str = Field(
        default="",
        description=(
            "NAIC code for the property/home policy carrier .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    property_home_policy_policy_number: str = Field(
        ...,
        description=(
            "Policy number for the property/home policy .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    flood_policy_carrier: str = Field(
        default="",
        description=(
            "Name of the carrier for the flood policy .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    flood_policy_naic_code: str = Field(
        default="",
        description=(
            "NAIC code for the flood policy carrier .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    flood_policy_policy_number: str = Field(
        default="",
        description=(
            'Policy number for the flood policy .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    wind_policy_carrier: str = Field(
        default="",
        description=(
            "Name of the carrier for the wind policy .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    wind_policy_naic_code: str = Field(
        default="",
        description=(
            'NAIC code for the wind policy carrier .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    wind_policy_policy_number: str = Field(
        default="",
        description=(
            'Policy number for the wind policy .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_name: str = Field(
        ...,
        description=(
            "Name of the primary contact at the agency .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_phone_a_c_no_ext: str = Field(
        ...,
        description=(
            "Agency contact phone number including area code and extension .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    contact_fax_a_c_no: str = Field(
        default="",
        description=(
            "Agency contact fax number including area code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_e_mail: str = Field(
        default="",
        description=(
            'Email address for the agency contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_address_line_1: str = Field(
        default="",
        description=(
            "First line of the agency contact address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_address_line_2: str = Field(
        default="",
        description=(
            "Second line of the agency contact address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_code: str = Field(
        default="",
        description=(
            'Agency contact code .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    contact_subcode: str = Field(
        default="",
        description=(
            'Agency contact subcode .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    agency_customer_id: str = Field(
        default="",
        description=(
            "Agency's internal customer identification number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class InsuredInformation(BaseModel):
    """Details about the insured and spouse"""

    name_of_insured_first_middle_last: str = Field(
        ...,
        description=(
            'Full legal name of the insured .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    insured_s_mailing_address: str = Field(
        ...,
        description=(
            'Mailing address of the insured .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    insured_date_of_birth: str = Field(
        default="", description="Date of birth of the insured"
    )  # YYYY-MM-DD format

    insured_fein_if_applicable: str = Field(
        default="",
        description=(
            "Federal Employer Identification Number of the insured, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    insured_marital_status: str = Field(
        default="",
        description=(
            'Marital status of the insured .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    insured_primary_phone: str = Field(
        default="",
        description=(
            'Primary phone number for the insured .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    insured_primary_phone_home: BooleanLike = Field(
        default="", description="Check if the insured's primary phone is a home number"
    )

    insured_primary_phone_bus: BooleanLike = Field(
        default="", description="Check if the insured's primary phone is a business number"
    )

    insured_primary_phone_cell: BooleanLike = Field(
        default="", description="Check if the insured's primary phone is a cell number"
    )

    insured_secondary_phone: str = Field(
        default="",
        description=(
            "Secondary phone number for the insured .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    insured_secondary_phone_home: BooleanLike = Field(
        default="", description="Check if the insured's secondary phone is a home number"
    )

    insured_secondary_phone_bus: BooleanLike = Field(
        default="", description="Check if the insured's secondary phone is a business number"
    )

    insured_secondary_phone_cell: BooleanLike = Field(
        default="", description="Check if the insured's secondary phone is a cell number"
    )

    insured_primary_e_mail_address: str = Field(
        default="",
        description=(
            'Primary email address of the insured .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    insured_secondary_e_mail_address: str = Field(
        default="",
        description=(
            "Secondary email address of the insured .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_spouse_first_middle_last_if_applicable: str = Field(
        default="",
        description=(
            "Full legal name of the insured's spouse, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    spouse_date_of_birth: str = Field(
        default="", description="Date of birth of the spouse"
    )  # YYYY-MM-DD format

    spouse_fein_if_applicable: str = Field(
        default="",
        description=(
            "Federal Employer Identification Number of the spouse, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    spouse_marital_status: str = Field(
        default="",
        description=(
            'Marital status of the spouse .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    spouse_primary_phone: str = Field(
        default="",
        description=(
            'Primary phone number for the spouse .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    spouse_primary_phone_home: BooleanLike = Field(
        default="", description="Check if the spouse's primary phone is a home number"
    )

    spouse_primary_phone_bus: BooleanLike = Field(
        default="", description="Check if the spouse's primary phone is a business number"
    )

    spouse_primary_phone_cell: BooleanLike = Field(
        default="", description="Check if the spouse's primary phone is a cell number"
    )

    spouse_secondary_phone: str = Field(
        default="",
        description=(
            'Secondary phone number for the spouse .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    spouse_secondary_phone_home: BooleanLike = Field(
        default="", description="Check if the spouse's secondary phone is a home number"
    )

    spouse_secondary_phone_bus: BooleanLike = Field(
        default="", description="Check if the spouse's secondary phone is a business number"
    )

    spouse_secondary_phone_cell: BooleanLike = Field(
        default="", description="Check if the spouse's secondary phone is a cell number"
    )

    spouse_primary_e_mail_address: str = Field(
        default="",
        description=(
            'Primary email address of the spouse .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    spouse_secondary_e_mail_address: str = Field(
        default="",
        description=(
            'Secondary email address of the spouse .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    spouse_s_mailing_address_if_applicable: str = Field(
        default="",
        description=(
            "Mailing address of the spouse, if different and applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Contact(BaseModel):
    """Designated contact person for the claim"""

    contact_insured: BooleanLike = Field(
        default="", description="Check if the insured is the primary contact"
    )

    name_of_contact_first_middle_last: str = Field(
        default="",
        description=(
            "Full name of the designated contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_primary_phone: str = Field(
        default="",
        description=(
            "Primary phone number for the contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_primary_phone_home: BooleanLike = Field(
        default="", description="Check if the contact's primary phone is a home number"
    )

    contact_primary_phone_bus: BooleanLike = Field(
        default="", description="Check if the contact's primary phone is a business number"
    )

    contact_primary_phone_cell: BooleanLike = Field(
        default="", description="Check if the contact's primary phone is a cell number"
    )

    contact_secondary_phone: str = Field(
        default="",
        description=(
            "Secondary phone number for the contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_secondary_phone_home: BooleanLike = Field(
        default="", description="Check if the contact's secondary phone is a home number"
    )

    contact_secondary_phone_bus: BooleanLike = Field(
        default="", description="Check if the contact's secondary phone is a business number"
    )

    contact_secondary_phone_cell: BooleanLike = Field(
        default="", description="Check if the contact's secondary phone is a cell number"
    )

    when_to_contact: str = Field(
        default="",
        description=(
            "Preferred times or conditions for contacting this person .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contacts_mailing_address: str = Field(
        default="",
        description=(
            'Mailing address of the contact person .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_primary_e_mail_address: str = Field(
        default="",
        description=(
            "Primary email address of the contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_secondary_e_mail_address: str = Field(
        default="",
        description=(
            "Secondary email address of the contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class LossInformation(BaseModel):
    """Details about the loss event and damage"""

    location_of_loss: str = Field(
        ...,
        description=(
            "General location name or identifier where the loss occurred .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    street: str = Field(
        default="",
        description=(
            'Street address of the loss location .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city_state_zip: str = Field(
        default="",
        description=(
            "City, state, and ZIP code of the loss location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    country: str = Field(
        default="",
        description=(
            'Country where the loss occurred .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    describe_location_of_loss_if_not_at_specific_street_address: str = Field(
        default="",
        description=(
            "Description of the loss location if no specific street address applies .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    police_or_fire_department_contacted: str = Field(
        default="",
        description=(
            "Name of the police or fire department that was contacted .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    report_number: str = Field(
        default="",
        description=(
            "Official report number assigned by authorities, if any .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    kind_of_loss_fire: BooleanLike = Field(
        default="", description="Check if the loss involved fire"
    )

    kind_of_loss_lightning: BooleanLike = Field(
        default="", description="Check if the loss involved lightning"
    )

    kind_of_loss_flood: BooleanLike = Field(
        default="", description="Check if the loss involved flood"
    )

    kind_of_loss_theft: BooleanLike = Field(
        default="", description="Check if the loss involved theft"
    )

    kind_of_loss_hail: BooleanLike = Field(
        default="", description="Check if the loss involved hail"
    )

    kind_of_loss_wind: BooleanLike = Field(
        default="", description="Check if the loss involved wind"
    )

    probable_amount_entire_loss: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated total amount of the entire loss"
    )

    description_of_loss_damage: str = Field(
        ...,
        description=(
            "Detailed description of how the loss occurred and the resulting damage .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reported_by: str = Field(
        ...,
        description=(
            'Name of the person reporting the loss .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reported_to: str = Field(
        ...,
        description=(
            "Name of the person or organization to whom the loss was reported .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AcordPropertyLossNotice(BaseModel):
    """ACORD

    PROPERTY LOSS NOTICE"""

    general_information: GeneralInformation = Field(..., description="General Information")
    insured_information: InsuredInformation = Field(..., description="Insured Information")
    contact: Contact = Field(..., description="Contact")
    loss_information: LossInformation = Field(..., description="Loss Information")
