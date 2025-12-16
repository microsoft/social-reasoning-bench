from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ComplainantContractorInformation(BaseModel):
    """Information about you (the complainant) and the contractor"""

    your_name_last: str = Field(
        ...,
        description=(
            'Complainant\'s last name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    your_name_first: str = Field(
        ...,
        description=(
            'Complainant\'s first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    your_name_middle: str = Field(
        default="",
        description=(
            'Complainant\'s middle name or initial .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contractor_business_name_as_shown_on_contract_invoice: str = Field(
        ...,
        description=(
            "Full legal business name of the contractor as it appears on the contract or "
            'invoice .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    contractor_business_address_number: str = Field(
        default="",
        description=(
            "Street number of the contractor's business address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contractor_business_address_street: str = Field(
        default="",
        description=(
            "Street name of the contractor's business address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contractor_name: str = Field(
        ...,
        description=(
            "Name of the individual contractor (if different from business name) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    contractor_license_no_used_if_any: str = Field(
        default="",
        description=(
            "Contractor license number that appears on the contract or was used, if any .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    contractor_business_address_city: str = Field(
        default="",
        description=(
            "City of the contractor's business address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contractor_business_address_county: str = Field(
        default="",
        description=(
            "County of the contractor's business address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contractor_business_address_state: str = Field(
        default="", description="State of the contractor's business address"
    )

    contractor_business_address_zip_code: str = Field(
        default="", description="ZIP code of the contractor's business address"
    )

    contractor_address_number: str = Field(
        default="",
        description=(
            "Street number of the contractor's mailing or physical address .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    contractor_address_street: str = Field(
        default="",
        description=(
            "Street name of the contractor's mailing or physical address .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    contractor_address_city: str = Field(
        default="",
        description=(
            "City of the contractor's mailing or physical address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contractor_address_state: str = Field(
        default="", description="State of the contractor's mailing or physical address"
    )

    contractor_address_zip_code: str = Field(
        default="", description="ZIP code of the contractor's mailing or physical address"
    )

    phone_where_you_can_be_reached_8_am_5_pm_area_code: str = Field(
        ...,
        description=(
            "Area code for the daytime phone number where you can be reached between 8 a.m. "
            'and 5 p.m. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    phone_where_you_can_be_reached_8_am_5_pm_number: str = Field(
        ...,
        description=(
            "Daytime phone number where you can be reached between 8 a.m. and 5 p.m. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other_phone_area_code: str = Field(
        default="",
        description=(
            "Area code for an alternate phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    other_phone_number: str = Field(
        default="",
        description=(
            'Alternate phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    email_address_complainant: str = Field(
        default="",
        description=(
            'Complainant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    phone_contractor_area_code: str = Field(
        default="",
        description=(
            "Area code for the contractor's phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_contractor_number: str = Field(
        default="",
        description=(
            'Contractor\'s phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email_address_contractor: str = Field(
        default="",
        description=(
            'Contractor\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    i_am_65_years_of_age_or_older_optional: BooleanLike = Field(
        default="", description="Check if the complainant is 65 years of age or older"
    )

    who_presented_negotiated_or_explained_the_contract: str = Field(
        default="",
        description=(
            "Name of the person who presented, negotiated, or explained the contract .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AuthorizedAssistantHowContractorWasFound(BaseModel):
    """Person authorized to assist with the complaint and how you located the contractor"""

    authorized_assistant_name_last: str = Field(
        default="",
        description=(
            "Last name of the person authorized to assist with the complaint .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    authorized_assistant_name_first: str = Field(
        default="",
        description=(
            "First name of the person authorized to assist with the complaint .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    authorized_assistant_relationship: str = Field(
        default="",
        description=(
            "Relationship of the authorized assistant to the complainant .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    where_was_the_contract_negotiated: str = Field(
        default="",
        description=(
            "Location where the contract was negotiated .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    how_did_you_find_the_contractor_door_to_door_sales: BooleanLike = Field(
        default="", description="Check if you found the contractor through door-to-door sales"
    )

    how_did_you_find_the_contractor_home_sales: BooleanLike = Field(
        default="", description="Check if you found the contractor through home sales"
    )

    how_did_you_find_the_contractor_website: BooleanLike = Field(
        default="", description="Check if you found the contractor through a website"
    )

    how_did_you_find_the_contractor_website_address: str = Field(
        default="",
        description=(
            "Website address where you found the contractor .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    how_did_you_find_the_contractor_other: BooleanLike = Field(
        default="", description="Check if you found the contractor through another method"
    )

    how_did_you_find_the_contractor_other_description: str = Field(
        default="",
        description=(
            "Describe how you found the contractor if 'Other' is selected .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    authorized_assistant_phone_8_am_5_pm_area_code: str = Field(
        default="",
        description=(
            "Area code for the authorized assistant's daytime phone number .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    authorized_assistant_phone_8_am_5_pm_number: str = Field(
        default="",
        description=(
            "Authorized assistant's daytime phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    authorized_assistant_home_phone_area_code: str = Field(
        default="",
        description=(
            "Area code for the authorized assistant's home phone number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    authorized_assistant_home_phone_number: str = Field(
        default="",
        description=(
            "Authorized assistant's home phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ConstructionSiteOwnerInformation(BaseModel):
    """Owner of the construction site and the site address/contact details"""

    owner_of_construction_site_i_am_the_owner: BooleanLike = Field(
        default="", description="Check if you are the owner of the construction site"
    )

    owner_name: str = Field(
        ...,
        description=(
            "Name of the owner of the construction site .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    construction_site_address_number: str = Field(
        ...,
        description=(
            "Street number of the construction site address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    construction_site_address_street: str = Field(
        ...,
        description=(
            "Street name of the construction site address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    construction_site_address_city: str = Field(
        ...,
        description=(
            'City of the construction site address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    construction_site_address_state: str = Field(
        ..., description="State of the construction site address"
    )

    construction_site_address_zip: str = Field(
        ..., description="ZIP code of the construction site address"
    )

    construction_site_address_same_as_my_address: BooleanLike = Field(
        default="",
        description="Check if the construction site address is the same as your mailing address",
    )

    mailing_address_city: str = Field(
        default="",
        description=(
            "City of your mailing address (if different from construction site) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    mailing_address_state: str = Field(
        default="",
        description="State of your mailing address (if different from construction site)",
    )

    mailing_address_zip: str = Field(
        default="",
        description="ZIP code of your mailing address (if different from construction site)",
    )

    construction_site_phone_1_area_code: str = Field(
        default="",
        description=(
            "Area code for the first phone number associated with the construction site .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    construction_site_phone_1_number: str = Field(
        default="",
        description=(
            "First phone number associated with the construction site .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    construction_site_phone_2_area_code: str = Field(
        default="",
        description=(
            "Area code for the second phone number associated with the construction site "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    construction_site_phone_2_number: str = Field(
        default="",
        description=(
            "Second phone number associated with the construction site .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ComplaintDetails(BaseModel):
    """Nature of your complaint and requested remedy"""

    what_is_your_primary_complaint_workmanship: BooleanLike = Field(
        ..., description="Select if your primary complaint is about workmanship"
    )

    what_is_your_primary_complaint_abandonment: BooleanLike = Field(
        ..., description="Select if your primary complaint is about abandonment of the project"
    )

    what_is_your_primary_complaint_unlicensed_activity: BooleanLike = Field(
        ..., description="Select if your primary complaint is about unlicensed activity"
    )

    what_is_your_primary_complaint_unregistered_salesperson: BooleanLike = Field(
        ..., description="Select if your primary complaint is about an unregistered salesperson"
    )

    what_is_your_primary_complaint_misrepresentation: BooleanLike = Field(
        ..., description="Select if your primary complaint is about misrepresentation"
    )

    what_is_your_primary_complaint_other: BooleanLike = Field(
        ...,
        description=(
            "Select if your primary complaint is about something other than the listed categories"
        ),
    )

    what_is_your_primary_complaint_other_description: str = Field(
        default="",
        description=(
            "Describe your primary complaint if 'Other' is selected .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contract_date: str = Field(..., description="Date the contract was signed")  # YYYY-MM-DD format

    amount_of_contract: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total dollar amount of the contract"
    )

    amount_paid_as_deposit: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Dollar amount paid as a deposit"
    )

    date_work_started: str = Field(
        ..., description="Date the work on the project started"
    )  # YYYY-MM-DD format

    date_work_stopped: str = Field(
        default="", description="Date the work on the project stopped"
    )  # YYYY-MM-DD format

    how_did_you_pay_for_the_system_cash_check_credit_card: BooleanLike = Field(
        ..., description="Select if you paid for the system with cash, check, or credit card"
    )

    how_did_you_pay_for_the_system_lease: BooleanLike = Field(
        ..., description="Select if you paid for the system through a lease"
    )

    how_did_you_pay_for_the_system_power_purchase_agreement_ppa: BooleanLike = Field(
        ...,
        description="Select if you paid for the system through a Power Purchase Agreement (PPA)",
    )

    how_did_you_pay_for_the_system_finance: BooleanLike = Field(
        ..., description="Select if you financed the system"
    )

    if_financed_type_property_assessed_clean_energy_pace: BooleanLike = Field(
        default="",
        description="Select if the financing type was Property Assessed Clean Energy (PACE)",
    )

    pace_provider_used: str = Field(
        default="",
        description=(
            'Name of the PACE provider used .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    if_financed_type_other_green_financing: str = Field(
        default="",
        description=(
            "Description of other 'green' financing used .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    if_financed_type_other_financing: str = Field(
        default="",
        description=(
            "Description of any other type of financing used .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    remedy_sought: str = Field(
        ...,
        description=(
            "Describe what outcome or remedy you are seeking .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ForOfficeUseOnly(BaseModel):
    """Internal processing information completed by CSLB staff"""

    complaint_number: str = Field(
        default="",
        description=(
            "Internal complaint number assigned by CSLB .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    type: str = Field(
        default="",
        description=(
            'Internal complaint type code .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    n: str = Field(
        default="",
        description=(
            "Internal code field 'N' .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    g: str = Field(
        default="",
        description=(
            "Internal code field 'G' .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    r: str = Field(
        default="",
        description=(
            "Internal code field 'R' .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    o: str = Field(
        default="",
        description=(
            "Internal code field 'O' .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    cnst: str = Field(
        default="",
        description=(
            "Internal code field 'CNST' .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    prjty: str = Field(
        default="",
        description=(
            'Internal priority code .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date_received_month: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month the complaint was received"
    )

    date_received_day: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day the complaint was received"
    )

    date_received_year: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year the complaint was received"
    )

    special_project: str = Field(
        default="",
        description=(
            "Internal special project code or description .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dt_stat_exp_month: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month of statute expiration date"
    )

    dt_stat_exp_day: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day of statute expiration date"
    )

    dt_stat_exp_year: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year of statute expiration date"
    )

    csr_init: str = Field(
        default="",
        description=(
            "Initials of the customer service representative .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    assigned_to_month: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month the complaint was assigned"
    )

    assigned_to_day: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day the complaint was assigned"
    )

    assigned_to_year: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year the complaint was assigned"
    )

    er_init: str = Field(
        default="",
        description=(
            "Initials of the enforcement representative .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    assigned_to_er_month: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month the complaint was assigned to the enforcement representative"
    )

    assigned_to_er_day: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day the complaint was assigned to the enforcement representative"
    )

    assigned_to_er_year: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year the complaint was assigned to the enforcement representative"
    )

    license_number: str = Field(
        default="",
        description=(
            "Contractor license number associated with the complaint .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    closure_letter: str = Field(
        default="",
        description=(
            "Internal code or reference for the closure letter .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    disposition: str = Field(
        default="",
        description=(
            "Final disposition or outcome of the complaint .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_closed_month: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month the complaint was closed"
    )

    date_closed_day: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day the complaint was closed"
    )

    date_closed_year: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year the complaint was closed"
    )

    status_change: str = Field(
        default="",
        description=(
            "Internal status change code or description .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    stp: str = Field(
        default="",
        description=(
            "Internal field 'STP' .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    c1: str = Field(
        default="",
        description=(
            "Internal code C1 for sections violated .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    c2: str = Field(
        default="",
        description=(
            "Internal code C2 for sections violated .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    c3: str = Field(
        default="",
        description=(
            "Internal code C3 for sections violated .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    c4: str = Field(
        default="",
        description=(
            "Internal code C4 for sections violated .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    c5: str = Field(
        default="",
        description=(
            "Internal code C5 for sections violated .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    c6: str = Field(
        default="",
        description=(
            "Internal code C6 for sections violated .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    c7: str = Field(
        default="",
        description=(
            "Internal code C7 for sections violated .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    c8: str = Field(
        default="",
        description=(
            "Internal code C8 for sections violated .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    c9: str = Field(
        default="",
        description=(
            "Internal code C9 for sections violated .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    sections_violated_date_1: str = Field(
        default="", description="First date associated with sections violated"
    )  # YYYY-MM-DD format

    sections_violated_date_2: str = Field(
        default="", description="Second date associated with sections violated"
    )  # YYYY-MM-DD format

    sections_violated_date_3: str = Field(
        default="", description="Third date associated with sections violated"
    )  # YYYY-MM-DD format


class ContractorsStateLicenseBoardStateOfCaliforniaSolarComplaintForm(BaseModel):
    """
        CONTRACTORS STATE LICENSE BOARD

    STATE OF CALIFORNIA

    Solar Complaint Form

        PLEASE COMPLETE ALL SECTIONS OF THIS FORM. A CSLB REPRESENTATIVE WILL CONTACT YOU TO REVIEW ALL INFORMATION PROVIDED. DO NOT SEND ORIGINALS—DOCUMENTS RECEIVED WILL NOT BE COPIED OR RETURNED.
        Please attach COPIES of all pages of the solar contract and change orders (front and back), finance documents or canceled checks (front and back), invoices, advertisements, business cards, or other relevant documents.
    """

    complainant__contractor_information: ComplainantContractorInformation = Field(
        ..., description="Complainant & Contractor Information"
    )
    authorized_assistant__how_contractor_was_found: AuthorizedAssistantHowContractorWasFound = (
        Field(..., description="Authorized Assistant & How Contractor Was Found")
    )
    construction_site__owner_information: ConstructionSiteOwnerInformation = Field(
        ..., description="Construction Site & Owner Information"
    )
    complaint_details: ComplaintDetails = Field(..., description="Complaint Details")
    for_office_use_only: ForOfficeUseOnly = Field(..., description="For Office Use Only")
