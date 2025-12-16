from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AccountCustomerInformation(BaseModel):
    """Basic account details and customer contact information"""

    account_number: str = Field(
        ...,
        description=(
            "Monitoring account number assigned to this site .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_on_line: str = Field(
        ..., description="Date the account goes online/monitoring starts"
    )  # YYYY-MM-DD format

    new_account: BooleanLike = Field(
        default="", description="Check if this is a new monitoring account"
    )

    replace_account: BooleanLike = Field(
        default="", description="Check if this account replaces an existing one"
    )

    relocate: BooleanLike = Field(
        default="", description="Check if the monitored site is being relocated"
    )

    info_change: BooleanLike = Field(
        default="", description="Check if this form is for updating account information only"
    )

    company_name: str = Field(
        ...,
        description=(
            "Legal or trading name of the company or customer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    res_no: str = Field(
        default="",
        description=(
            "Residential or main contact phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    responsible_person: str = Field(
        ...,
        description=(
            "Primary person responsible for the alarm account .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    bus_no: str = Field(
        default="",
        description=(
            "Business phone number for the responsible person or company .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Street address of the monitored premises .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    cell_no: str = Field(
        default="",
        description=(
            "Mobile phone number for the responsible person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    fax_no: str = Field(
        default="",
        description=(
            'Fax number for the account or company .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the monitored premises .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    province: str = Field(
        ...,
        description=(
            "Province or state of the monitored premises .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    postal_code: str = Field(..., description="Postal or ZIP code of the monitored premises")

    email: str = Field(
        default="",
        description=(
            "Email address for account communication .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class SignalZoneDescription(BaseModel):
    """Zone numbers, signal types, and descriptions for the alarm system"""

    zone_1_signal: str = Field(
        default="",
        description=(
            'Signal code or type for zone 1 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_1_description: str = Field(
        default="",
        description=(
            "Description of what zone 1 monitors (e.g., front door, motion) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    zone_2_signal: str = Field(
        default="",
        description=(
            'Signal code or type for zone 2 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_2_description: str = Field(
        default="",
        description=(
            'Description of what zone 2 monitors .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_3_signal: str = Field(
        default="",
        description=(
            'Signal code or type for zone 3 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_3_description: str = Field(
        default="",
        description=(
            'Description of what zone 3 monitors .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_4_signal: str = Field(
        default="",
        description=(
            'Signal code or type for zone 4 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_4_description: str = Field(
        default="",
        description=(
            'Description of what zone 4 monitors .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_5_signal: str = Field(
        default="",
        description=(
            'Signal code or type for zone 5 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_5_description: str = Field(
        default="",
        description=(
            'Description of what zone 5 monitors .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_6_signal: str = Field(
        default="",
        description=(
            'Signal code or type for zone 6 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_6_description: str = Field(
        default="",
        description=(
            'Description of what zone 6 monitors .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_7_signal: str = Field(
        default="",
        description=(
            'Signal code or type for zone 7 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_7_description: str = Field(
        default="",
        description=(
            'Description of what zone 7 monitors .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_8_signal: str = Field(
        default="",
        description=(
            'Signal code or type for zone 8 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_8_description: str = Field(
        default="",
        description=(
            'Description of what zone 8 monitors .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_9_signal: str = Field(
        default="",
        description=(
            'Signal code or type for zone 9 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_9_description: str = Field(
        default="",
        description=(
            'Description of what zone 9 monitors .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_10_signal: str = Field(
        default="",
        description=(
            'Signal code or type for zone 10 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_10_description: str = Field(
        default="",
        description=(
            'Description of what zone 10 monitors .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_11_signal: str = Field(
        default="",
        description=(
            'Signal code or type for zone 11 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_11_description: str = Field(
        default="",
        description=(
            'Description of what zone 11 monitors .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_12_signal: str = Field(
        default="",
        description=(
            'Signal code or type for zone 12 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_12_description: str = Field(
        default="",
        description=(
            'Description of what zone 12 monitors .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_13_signal: str = Field(
        default="",
        description=(
            'Signal code or type for zone 13 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_13_description: str = Field(
        default="",
        description=(
            'Description of what zone 13 monitors .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_14_signal: str = Field(
        default="",
        description=(
            'Signal code or type for zone 14 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_14_description: str = Field(
        default="",
        description=(
            'Description of what zone 14 monitors .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_15_signal: str = Field(
        default="",
        description=(
            'Signal code or type for zone 15 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_15_description: str = Field(
        default="",
        description=(
            'Description of what zone 15 monitors .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_16_signal: str = Field(
        default="",
        description=(
            'Signal code or type for zone 16 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zone_16_description: str = Field(
        default="",
        description=(
            'Description of what zone 16 monitors .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class KeyholderPasscards(BaseModel):
    """Keyholder names and their associated passcards and telephone numbers"""

    passcard_1_name: str = Field(
        default="",
        description=(
            'Name of keyholder/passcard holder 1 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    passcard_1_telephone: str = Field(
        default="",
        description=(
            "Telephone number for keyholder/passcard holder 1 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    passcard_2_name: str = Field(
        default="",
        description=(
            'Name of keyholder/passcard holder 2 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    passcard_2_telephone: str = Field(
        default="",
        description=(
            "Telephone number for keyholder/passcard holder 2 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    passcard_3_name: str = Field(
        default="",
        description=(
            'Name of keyholder/passcard holder 3 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    passcard_3_telephone: str = Field(
        default="",
        description=(
            "Telephone number for keyholder/passcard holder 3 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    passcard_4_name: str = Field(
        default="",
        description=(
            'Name of keyholder/passcard holder 4 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    passcard_4_telephone: str = Field(
        default="",
        description=(
            "Telephone number for keyholder/passcard holder 4 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    passcard_5_name: str = Field(
        default="",
        description=(
            'Name of keyholder/passcard holder 5 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    passcard_5_telephone: str = Field(
        default="",
        description=(
            "Telephone number for keyholder/passcard holder 5 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    passcard_6_name: str = Field(
        default="",
        description=(
            'Name of keyholder/passcard holder 6 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    passcard_6_telephone: str = Field(
        default="",
        description=(
            "Telephone number for keyholder/passcard holder 6 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    passcard_7_name: str = Field(
        default="",
        description=(
            'Name of keyholder/passcard holder 7 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    passcard_7_telephone: str = Field(
        default="",
        description=(
            "Telephone number for keyholder/passcard holder 7 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    passcard_8_name: str = Field(
        default="",
        description=(
            'Name of keyholder/passcard holder 8 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    passcard_8_telephone: str = Field(
        default="",
        description=(
            "Telephone number for keyholder/passcard holder 8 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SpecialInstructions(BaseModel):
    """Free-form special instructions for handling the account"""

    special_instructions_line_1: str = Field(
        default="",
        description=(
            "First line of any special monitoring or response instructions .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    special_instructions_line_2: str = Field(
        default="",
        description=(
            "Second line of any special monitoring or response instructions .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    special_instructions_line_3: str = Field(
        default="",
        description=(
            "Third line of any special monitoring or response instructions .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ServiceOptionsAlarmHandling(BaseModel):
    """Service options, reporting preferences, and alarm response handling details"""

    gsm_ac_number_checkbox: BooleanLike = Field(
        default="", description="Check if GSM account number/service applies"
    )

    gsm_ac_number: str = Field(
        default="",
        description=(
            "GSM account number if GSM service is used .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    open_closing_report: BooleanLike = Field(
        default="", description="Check to enable open and closing activity reports"
    )

    info_change_date_open_closing: BooleanLike = Field(
        default="",
        description="Checkbox indicating this is an information change for open & closing report",
    )

    send_police_registered: BooleanLike = Field(
        default="",
        description="Check to indicate police dispatch is requested and registration applies",
    )

    send_police_registered_yes: BooleanLike = Field(
        default="", description="Select 'Yes' if the account is registered for police dispatch"
    )

    send_police_registered_no: BooleanLike = Field(
        default="", description="Select 'No' if the account is not registered for police dispatch"
    )

    chinese_operator_service: BooleanLike = Field(
        default="", description="Check if Chinese language operator service is required"
    )

    info_change_date_chinese_service: BooleanLike = Field(
        default="",
        description="Checkbox indicating this is an information change for Chinese operator service",
    )

    panic_signal_function_yes: BooleanLike = Field(
        default="", description="Select 'Yes' if panic signal function is enabled"
    )

    panic_signal_function_no: BooleanLike = Field(
        default="", description="Select 'No' if panic signal function is disabled"
    )

    send_security_guard: BooleanLike = Field(
        default="", description="Check if a security guard should be dispatched on alarm"
    )

    download_no: str = Field(
        default="",
        description=(
            "Download or programming number for the alarm panel .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    call_keyholder_only: BooleanLike = Field(
        default="", description="Check if operators should only call keyholders and not dispatch"
    )

    panel_model: str = Field(
        default="",
        description=(
            "Model number of the alarm control panel .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    version: str = Field(
        default="",
        description=(
            "Firmware or software version of the alarm panel .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Authorization(BaseModel):
    """Customer authorization and confirmation of information"""

    authorization_signature: str = Field(
        ...,
        description=(
            "Signature of the authorized person confirming the information and agreement "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    date_signature_section: str = Field(
        ..., description="Date the authorization form is signed"
    )  # YYYY-MM-DD format


class CanaforceSecuritysps(BaseModel):
    """
        CANAFORCE SECURITY
    (SPS)

        By your signature, you agree that the information on this sheet is correct. Also, you agree that all equipment, options, and services chosen, including the number of zones described in ‘Signal Zone Description’ section, are adequate for your site. Furthermore, you will not hold Canaforce Security Group Ltd. responsible for any losses that occur.
    """

    account__customer_information: AccountCustomerInformation = Field(
        ..., description="Account & Customer Information"
    )
    signal_zone_description: SignalZoneDescription = Field(
        ..., description="Signal Zone Description"
    )
    keyholder__passcards: KeyholderPasscards = Field(..., description="Keyholder / Passcards")
    special_instructions: SpecialInstructions = Field(..., description="Special Instructions")
    service_options__alarm_handling: ServiceOptionsAlarmHandling = Field(
        ..., description="Service Options & Alarm Handling"
    )
    authorization: Authorization = Field(..., description="Authorization")
