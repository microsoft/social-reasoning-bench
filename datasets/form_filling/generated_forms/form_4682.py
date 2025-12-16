from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PLBInformation(BaseModel):
    """Beacon identification and manufacturer details"""

    beacon_id_unique_identification_number_digit_1: str = Field(
        ...,
        description=(
            "First character of the 15-digit hexadecimal beacon ID .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    beacon_id_unique_identification_number_digit_2: str = Field(
        ...,
        description=(
            "Second character of the 15-digit hexadecimal beacon ID .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    beacon_id_unique_identification_number_digit_3: str = Field(
        ...,
        description=(
            "Third character of the 15-digit hexadecimal beacon ID .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    beacon_id_unique_identification_number_digit_4: str = Field(
        ...,
        description=(
            "Fourth character of the 15-digit hexadecimal beacon ID .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    beacon_id_unique_identification_number_digit_5: str = Field(
        ...,
        description=(
            "Fifth character of the 15-digit hexadecimal beacon ID .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    beacon_id_unique_identification_number_digit_6: str = Field(
        ...,
        description=(
            "Sixth character of the 15-digit hexadecimal beacon ID .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    beacon_id_unique_identification_number_digit_7: str = Field(
        ...,
        description=(
            "Seventh character of the 15-digit hexadecimal beacon ID .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    beacon_id_unique_identification_number_digit_8: str = Field(
        ...,
        description=(
            "Eighth character of the 15-digit hexadecimal beacon ID .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    beacon_id_unique_identification_number_digit_9: str = Field(
        ...,
        description=(
            "Ninth character of the 15-digit hexadecimal beacon ID .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    beacon_id_unique_identification_number_digit_10: str = Field(
        ...,
        description=(
            "Tenth character of the 15-digit hexadecimal beacon ID .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    beacon_id_unique_identification_number_digit_11: str = Field(
        ...,
        description=(
            "Eleventh character of the 15-digit hexadecimal beacon ID .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    beacon_id_unique_identification_number_digit_12: str = Field(
        ...,
        description=(
            "Twelfth character of the 15-digit hexadecimal beacon ID .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    beacon_id_unique_identification_number_digit_13: str = Field(
        ...,
        description=(
            "Thirteenth character of the 15-digit hexadecimal beacon ID .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    beacon_id_unique_identification_number_digit_14: str = Field(
        ...,
        description=(
            "Fourteenth character of the 15-digit hexadecimal beacon ID .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    beacon_id_unique_identification_number_digit_15: str = Field(
        ...,
        description=(
            "Fifteenth character of the 15-digit hexadecimal beacon ID .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    checksum_digit_1: str = Field(
        default="",
        description=(
            "First checksum character associated with the beacon ID .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    checksum_digit_2: str = Field(
        default="",
        description=(
            "Second checksum character associated with the beacon ID .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    plb_manufacturer: str = Field(
        ...,
        description=(
            'Manufacturer name of the PLB .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    model_no: str = Field(
        ...,
        description=(
            'Model number of the PLB .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class PurposeofPLBRegistration(BaseModel):
    """Reason for submitting this PLB registration"""

    new_registration: BooleanLike = Field(
        default="", description="Check if this is a new PLB registration"
    )

    change_of_registration_information: BooleanLike = Field(
        default="", description="Check if you are updating existing registration information"
    )

    replacement_of_decal_only: BooleanLike = Field(
        default="", description="Check if you only need a replacement decal"
    )

    renewal_of_registration: BooleanLike = Field(
        default="", description="Check if you are renewing an existing registration"
    )

    replacement_for_previously_registered_plb: BooleanLike = Field(
        default="", description="Check if this PLB replaces a previously registered PLB"
    )

    change_of_ownership: BooleanLike = Field(
        default="", description="Check if ownership of the PLB has changed"
    )

    old_unique_id_number_digit_1: str = Field(
        default="",
        description=(
            "First character of the old 15-digit unique ID number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    old_unique_id_number_digit_2: str = Field(
        default="",
        description=(
            "Second character of the old 15-digit unique ID number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    old_unique_id_number_digit_3: str = Field(
        default="",
        description=(
            "Third character of the old 15-digit unique ID number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    old_unique_id_number_digit_4: str = Field(
        default="",
        description=(
            "Fourth character of the old 15-digit unique ID number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    old_unique_id_number_digit_5: str = Field(
        default="",
        description=(
            "Fifth character of the old 15-digit unique ID number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    old_unique_id_number_digit_6: str = Field(
        default="",
        description=(
            "Sixth character of the old 15-digit unique ID number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    old_unique_id_number_digit_7: str = Field(
        default="",
        description=(
            "Seventh character of the old 15-digit unique ID number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    old_unique_id_number_digit_8: str = Field(
        default="",
        description=(
            "Eighth character of the old 15-digit unique ID number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    old_unique_id_number_digit_9: str = Field(
        default="",
        description=(
            "Ninth character of the old 15-digit unique ID number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    old_unique_id_number_digit_10: str = Field(
        default="",
        description=(
            "Tenth character of the old 15-digit unique ID number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    old_unique_id_number_digit_11: str = Field(
        default="",
        description=(
            "Eleventh character of the old 15-digit unique ID number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    old_unique_id_number_digit_12: str = Field(
        default="",
        description=(
            "Twelfth character of the old 15-digit unique ID number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    old_unique_id_number_digit_13: str = Field(
        default="",
        description=(
            "Thirteenth character of the old 15-digit unique ID number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    old_unique_id_number_digit_14: str = Field(
        default="",
        description=(
            "Fourteenth character of the old 15-digit unique ID number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    old_unique_id_number_digit_15: str = Field(
        default="",
        description=(
            "Fifteenth character of the old 15-digit unique ID number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class OwnerOperatorInformation(BaseModel):
    """Contact and address information for the PLB owner/operator"""

    name: str = Field(
        ...,
        description=(
            "Owner or operator full name (Last, First, Middle Initial) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_primary_area_code: str = Field(
        ...,
        description=(
            "Area code for the primary telephone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_primary_number: str = Field(
        ...,
        description=(
            'Primary telephone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            'Street mailing address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state_province: str = Field(
        ...,
        description=(
            "State or province of the mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    zip_postal_code: str = Field(..., description="ZIP or postal code of the mailing address")

    country: str = Field(
        ...,
        description=(
            'Country of the mailing address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            'Email address of the owner/operator .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    telephone_1_area_code: str = Field(
        default="",
        description=(
            "Area code for the first additional telephone number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_1_number: str = Field(
        default="",
        description=(
            'First additional telephone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    telephone_1_home: BooleanLike = Field(
        default="", description="Mark if telephone 1 is a home number"
    )

    telephone_1_work: BooleanLike = Field(
        default="", description="Mark if telephone 1 is a work number"
    )

    telephone_1_cellular: BooleanLike = Field(
        default="", description="Mark if telephone 1 is a cellular/mobile number"
    )

    telephone_1_fax: BooleanLike = Field(
        default="", description="Mark if telephone 1 is a fax number"
    )

    telephone_1_other: BooleanLike = Field(
        default="", description="Mark if telephone 1 is another type of number"
    )

    telephone_2_area_code: str = Field(
        default="",
        description=(
            "Area code for the second additional telephone number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_2_number: str = Field(
        default="",
        description=(
            'Second additional telephone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    telephone_2_home: BooleanLike = Field(
        default="", description="Mark if telephone 2 is a home number"
    )

    telephone_2_work: BooleanLike = Field(
        default="", description="Mark if telephone 2 is a work number"
    )

    telephone_2_cellular: BooleanLike = Field(
        default="", description="Mark if telephone 2 is a cellular/mobile number"
    )

    telephone_2_fax: BooleanLike = Field(
        default="", description="Mark if telephone 2 is a fax number"
    )

    telephone_2_other: BooleanLike = Field(
        default="", description="Mark if telephone 2 is another type of number"
    )

    telephone_3_area_code: str = Field(
        default="",
        description=(
            "Area code for the third additional telephone number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_3_number: str = Field(
        default="",
        description=(
            'Third additional telephone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    telephone_3_home: BooleanLike = Field(
        default="", description="Mark if telephone 3 is a home number"
    )

    telephone_3_work: BooleanLike = Field(
        default="", description="Mark if telephone 3 is a work number"
    )

    telephone_3_cellular: BooleanLike = Field(
        default="", description="Mark if telephone 3 is a cellular/mobile number"
    )

    telephone_3_fax: BooleanLike = Field(
        default="", description="Mark if telephone 3 is a fax number"
    )

    telephone_3_other: BooleanLike = Field(
        default="", description="Mark if telephone 3 is another type of number"
    )


class GeneralUseData(BaseModel):
    """Intended usage, environment, and additional information about PLB use"""

    usage_commercial: BooleanLike = Field(
        default="", description="Check if the PLB is used for commercial purposes"
    )

    usage_non_commercial: BooleanLike = Field(
        default="", description="Check if the PLB is used for non-commercial purposes"
    )

    usage_government_military: BooleanLike = Field(
        default="", description="Check if the PLB is used for government military purposes"
    )

    usage_government_non_military: BooleanLike = Field(
        default="", description="Check if the PLB is used for government non-military purposes"
    )

    specific_usage_hiking: BooleanLike = Field(
        default="", description="Check if the PLB is used for hiking"
    )

    specific_usage_hunting: BooleanLike = Field(
        default="", description="Check if the PLB is used for hunting"
    )

    specific_usage_fishing: BooleanLike = Field(
        default="", description="Check if the PLB is used for fishing"
    )

    specific_usage_other: BooleanLike = Field(
        default="", description="Check if the PLB is used for other recreational activities"
    )

    specific_usage_other_description: str = Field(
        default="",
        description=(
            "Describe other specific recreational usage of the PLB .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    type_land_vehicle: BooleanLike = Field(
        default="", description="Check if the PLB is associated with a land vehicle"
    )

    type_boat: BooleanLike = Field(
        default="", description="Check if the PLB is associated with a boat"
    )

    type_aircraft: BooleanLike = Field(
        default="", description="Check if the PLB is associated with an aircraft"
    )

    type_none: BooleanLike = Field(
        default="", description="Check if the PLB is not associated with any vehicle or craft"
    )

    type_other: BooleanLike = Field(
        default="", description="Check if the PLB is associated with another type not listed"
    )

    type_other_description: str = Field(
        default="",
        description=(
            "Describe the other type associated with the PLB .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_data_line_1: str = Field(
        default="",
        description=(
            "First line of additional information (e.g., areas frequented, home port) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    additional_data_line_2: str = Field(
        default="",
        description=(
            'Second line of additional information .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    additional_data_line_3: str = Field(
        default="",
        description=(
            'Third line of additional information .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class EmergencyContactInformation(BaseModel):
    """Primary and alternate 24-hour emergency contacts"""

    name_of_primary_24_hour_emergency_contact: str = Field(
        ...,
        description=(
            "Full name of the primary 24-hour emergency contact .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    primary_emergency_contact_telephone_1_area_code: str = Field(
        ...,
        description=(
            "Area code for the primary contact's first telephone number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    primary_emergency_contact_telephone_1_number: str = Field(
        ...,
        description=(
            "First telephone number for the primary emergency contact .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    primary_emergency_contact_telephone_1_home: BooleanLike = Field(
        default="", description="Mark if primary contact telephone 1 is a home number"
    )

    primary_emergency_contact_telephone_1_work: BooleanLike = Field(
        default="", description="Mark if primary contact telephone 1 is a work number"
    )

    primary_emergency_contact_telephone_1_cellular: BooleanLike = Field(
        default="", description="Mark if primary contact telephone 1 is a cellular/mobile number"
    )

    primary_emergency_contact_telephone_1_fax: BooleanLike = Field(
        default="", description="Mark if primary contact telephone 1 is a fax number"
    )

    primary_emergency_contact_telephone_1_other: BooleanLike = Field(
        default="", description="Mark if primary contact telephone 1 is another type of number"
    )

    primary_emergency_contact_telephone_2_area_code: str = Field(
        default="",
        description=(
            "Area code for the primary contact's second telephone number .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    primary_emergency_contact_telephone_2_number: str = Field(
        default="",
        description=(
            "Second telephone number for the primary emergency contact .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    primary_emergency_contact_telephone_2_home: BooleanLike = Field(
        default="", description="Mark if primary contact telephone 2 is a home number"
    )

    primary_emergency_contact_telephone_2_work: BooleanLike = Field(
        default="", description="Mark if primary contact telephone 2 is a work number"
    )

    primary_emergency_contact_telephone_2_cellular: BooleanLike = Field(
        default="", description="Mark if primary contact telephone 2 is a cellular/mobile number"
    )

    primary_emergency_contact_telephone_2_fax: BooleanLike = Field(
        default="", description="Mark if primary contact telephone 2 is a fax number"
    )

    primary_emergency_contact_telephone_2_other: BooleanLike = Field(
        default="", description="Mark if primary contact telephone 2 is another type of number"
    )

    primary_emergency_contact_telephone_3_area_code: str = Field(
        default="",
        description=(
            "Area code for the primary contact's third telephone number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    primary_emergency_contact_telephone_3_number: str = Field(
        default="",
        description=(
            "Third telephone number for the primary emergency contact .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    primary_emergency_contact_telephone_3_home: BooleanLike = Field(
        default="", description="Mark if primary contact telephone 3 is a home number"
    )

    primary_emergency_contact_telephone_3_work: BooleanLike = Field(
        default="", description="Mark if primary contact telephone 3 is a work number"
    )

    primary_emergency_contact_telephone_3_cellular: BooleanLike = Field(
        default="", description="Mark if primary contact telephone 3 is a cellular/mobile number"
    )

    primary_emergency_contact_telephone_3_fax: BooleanLike = Field(
        default="", description="Mark if primary contact telephone 3 is a fax number"
    )

    primary_emergency_contact_telephone_3_other: BooleanLike = Field(
        default="", description="Mark if primary contact telephone 3 is another type of number"
    )

    name_of_alternate_24_hour_emergency_contact: str = Field(
        default="",
        description=(
            "Full name of the alternate 24-hour emergency contact .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    alternate_emergency_contact_telephone_1_area_code: str = Field(
        default="",
        description=(
            "Area code for the alternate contact's first telephone number .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    alternate_emergency_contact_telephone_1_number: str = Field(
        default="",
        description=(
            "First telephone number for the alternate emergency contact .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    alternate_emergency_contact_telephone_1_home: BooleanLike = Field(
        default="", description="Mark if alternate contact telephone 1 is a home number"
    )

    alternate_emergency_contact_telephone_1_work: BooleanLike = Field(
        default="", description="Mark if alternate contact telephone 1 is a work number"
    )

    alternate_emergency_contact_telephone_1_cellular: BooleanLike = Field(
        default="", description="Mark if alternate contact telephone 1 is a cellular/mobile number"
    )

    alternate_emergency_contact_telephone_1_fax: BooleanLike = Field(
        default="", description="Mark if alternate contact telephone 1 is a fax number"
    )

    alternate_emergency_contact_telephone_1_other: BooleanLike = Field(
        default="", description="Mark if alternate contact telephone 1 is another type of number"
    )

    alternate_emergency_contact_telephone_2_area_code: str = Field(
        default="",
        description=(
            "Area code for the alternate contact's second telephone number .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    alternate_emergency_contact_telephone_2_number: str = Field(
        default="",
        description=(
            "Second telephone number for the alternate emergency contact .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    alternate_emergency_contact_telephone_2_home: BooleanLike = Field(
        default="", description="Mark if alternate contact telephone 2 is a home number"
    )

    alternate_emergency_contact_telephone_2_work: BooleanLike = Field(
        default="", description="Mark if alternate contact telephone 2 is a work number"
    )

    alternate_emergency_contact_telephone_2_cellular: BooleanLike = Field(
        default="", description="Mark if alternate contact telephone 2 is a cellular/mobile number"
    )

    alternate_emergency_contact_telephone_2_fax: BooleanLike = Field(
        default="", description="Mark if alternate contact telephone 2 is a fax number"
    )

    alternate_emergency_contact_telephone_2_other: BooleanLike = Field(
        default="", description="Mark if alternate contact telephone 2 is another type of number"
    )

    alternate_emergency_contact_telephone_3_area_code: str = Field(
        default="",
        description=(
            "Area code for the alternate contact's third telephone number .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    alternate_emergency_contact_telephone_3_number: str = Field(
        default="",
        description=(
            "Third telephone number for the alternate emergency contact .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    alternate_emergency_contact_telephone_3_home: BooleanLike = Field(
        default="", description="Mark if alternate contact telephone 3 is a home number"
    )

    alternate_emergency_contact_telephone_3_work: BooleanLike = Field(
        default="", description="Mark if alternate contact telephone 3 is a work number"
    )

    alternate_emergency_contact_telephone_3_cellular: BooleanLike = Field(
        default="", description="Mark if alternate contact telephone 3 is a cellular/mobile number"
    )

    alternate_emergency_contact_telephone_3_fax: BooleanLike = Field(
        default="", description="Mark if alternate contact telephone 3 is a fax number"
    )

    alternate_emergency_contact_telephone_3_other: BooleanLike = Field(
        default="", description="Mark if alternate contact telephone 3 is another type of number"
    )


class Certification(BaseModel):
    """Signature and date of certification"""

    signature: str = Field(
        ...,
        description=(
            "Signature of the owner/operator certifying the information .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the form is signed")  # YYYY-MM-DD format


class Official406MhzPlbRegistrationForm(BaseModel):
    """
    Official 406 MHz PLB Registration Form

    ''
    """

    plb_information: PLBInformation = Field(..., description="PLB Information")
    purpose_of_plb_registration: PurposeofPLBRegistration = Field(
        ..., description="Purpose of PLB Registration"
    )
    owneroperator_information: OwnerOperatorInformation = Field(
        ..., description="Owner/Operator Information"
    )
    general_use_data: GeneralUseData = Field(..., description="General Use Data")
    emergency_contact_information: EmergencyContactInformation = Field(
        ..., description="Emergency Contact Information"
    )
    certification: Certification = Field(..., description="Certification")
