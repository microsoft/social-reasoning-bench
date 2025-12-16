from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class LossesPast5YearsTableRow1Row(BaseModel):
    """Single row in Date of Loss (row 1)"""

    date_of_loss: str = Field(default="", description="Date_Of_Loss")
    details_of_loss: str = Field(default="", description="Details_Of_Loss")
    amount_paid: str = Field(default="", description="Amount_Paid")
    open_closed: str = Field(default="", description="Open_Closed")


class AgencyInformation(BaseModel):
    """Details about the agency submitting the quote"""

    agency: str = Field(
        ...,
        description=(
            "Name of the insurance agency submitting the quote .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_agency: str = Field(
        ...,
        description=(
            'Primary phone number for the agency .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_person: str = Field(
        ...,
        description=(
            "Name of the primary contact person at the agency .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email_agency: str = Field(
        ...,
        description=(
            'Email address for the agency contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class InsuredInformation(BaseModel):
    """Details about the insured and prior history"""

    insured: str = Field(
        ...,
        description=(
            'Name of the insured person or entity .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    effective_date: str = Field(..., description="Policy effective date")  # YYYY-MM-DD format

    address_insured: str = Field(
        ...,
        description=(
            'Mailing address of the insured .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city_insured: str = Field(
        ...,
        description=(
            "City for the insured's mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state_insured: str = Field(..., description="State for the insured's mailing address")

    zip_insured: str = Field(..., description="ZIP code for the insured's mailing address")

    phone_insured: str = Field(
        ...,
        description=(
            'Primary phone number for the insured .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    dob: str = Field(
        default="", description="Date of birth of the insured (if applicable)"
    )  # YYYY-MM-DD format

    felony_yes: BooleanLike = Field(
        default="",
        description="Check if the insured has been charged with or convicted of a felony",
    )

    felony_no: BooleanLike = Field(
        default="",
        description="Check if the insured has not been charged with or convicted of a felony",
    )

    bankruptcy_3yrs_yes: BooleanLike = Field(
        default="",
        description=(
            "Check if the insured has had bankruptcy, foreclosure, or repossession within "
            "the past 3 years"
        ),
    )

    bankruptcy_3yrs_no: BooleanLike = Field(
        default="",
        description=(
            "Check if the insured has not had bankruptcy, foreclosure, or repossession "
            "within the past 3 years"
        ),
    )


class LossesinPast5Years(BaseModel):
    """Schedule of prior losses in the last 5 years"""

    losses_past_5_years_table_row_1: List[LossesPast5YearsTableRow1Row] = Field(
        default="",
        description=(
            "Table to list losses in the past 5 years including date, details, amount paid, "
            "and open/closed status"
        ),
    )  # List of table rows

    details_of_loss_row_1: str = Field(
        default="",
        description=(
            'Details of the first listed loss .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    amount_paid_row_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid on the first listed loss"
    )

    open_closed_row_1: str = Field(
        default="",
        description=(
            "Indicate whether the first listed loss is open or closed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_loss_row_2: str = Field(
        default="", description="Date of the second listed loss"
    )  # YYYY-MM-DD format

    details_of_loss_row_2: str = Field(
        default="",
        description=(
            'Details of the second listed loss .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    amount_paid_row_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid on the second listed loss"
    )

    open_closed_row_2: str = Field(
        default="",
        description=(
            "Indicate whether the second listed loss is open or closed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_loss_row_3: str = Field(
        default="", description="Date of the third listed loss"
    )  # YYYY-MM-DD format

    details_of_loss_row_3: str = Field(
        default="",
        description=(
            'Details of the third listed loss .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    amount_paid_row_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid on the third listed loss"
    )

    open_closed_row_3: str = Field(
        default="",
        description=(
            "Indicate whether the third listed loss is open or closed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_loss_row_4: str = Field(
        default="", description="Date of the fourth listed loss"
    )  # YYYY-MM-DD format

    details_of_loss_row_4: str = Field(
        default="",
        description=(
            'Details of the fourth listed loss .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    amount_paid_row_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid on the fourth listed loss"
    )

    open_closed_row_4: str = Field(
        default="",
        description=(
            "Indicate whether the fourth listed loss is open or closed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_loss_row_5: str = Field(
        default="", description="Date of the fifth listed loss"
    )  # YYYY-MM-DD format

    details_of_loss_row_5: str = Field(
        default="",
        description=(
            'Details of the fifth listed loss .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    amount_paid_row_5: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid on the fifth listed loss"
    )

    open_closed_row_5: str = Field(
        default="",
        description=(
            "Indicate whether the fifth listed loss is open or closed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Premises(BaseModel):
    """Information about the premises and occupancy"""

    form_requested_homeowners: BooleanLike = Field(
        default="", description="Select if a Homeowners form is requested"
    )

    form_requested_dwelling: BooleanLike = Field(
        default="", description="Select if a Dwelling form is requested"
    )

    form_requested_condo: BooleanLike = Field(
        default="", description="Select if a Condo form is requested"
    )

    form_requested_builders_risk: BooleanLike = Field(
        default="", description="Select if a Builders Risk form is requested"
    )

    owner: BooleanLike = Field(default="", description="Check if the premises is owner-occupied")

    secondary_without_rental: BooleanLike = Field(
        default="", description="Check if the premises is a secondary residence without rental"
    )

    secondary_with_rental: BooleanLike = Field(
        default="", description="Check if the premises is a secondary residence with rental"
    )

    tenant: BooleanLike = Field(default="", description="Check if the premises is tenant-occupied")

    vacant: BooleanLike = Field(default="", description="Check if the premises is vacant")

    weeks_rented_annually: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of weeks per year the property is rented"
    )

    address_if_different: str = Field(
        default="",
        description=(
            "Premises address if different from insured's mailing address .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    city_premises: str = Field(
        default="",
        description=(
            'City for the premises address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state_premises: str = Field(default="", description="State for the premises address")

    zip_premises: str = Field(default="", description="ZIP code for the premises address")

    year_built: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year the building was originally constructed"
    )

    construction_type: str = Field(
        default="",
        description=(
            "Type of building construction (e.g., frame, masonry) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    protection_class: str = Field(
        default="",
        description=(
            'ISO protection class for the property .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    short_term_rental_yes: BooleanLike = Field(
        default="",
        description="Check if the property is used as a short-term rental (e.g., Airbnb)",
    )

    short_term_rental_no: BooleanLike = Field(
        default="", description="Check if the property is not used as a short-term rental"
    )

    square_feet: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total finished square footage of the dwelling"
    )

    number_of_stories: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of stories in the dwelling"
    )

    first_exposed_ocean_yes: BooleanLike = Field(
        default="",
        description="Check if the home is the first structure exposed to ocean, bay, or sound",
    )

    first_exposed_ocean_no: BooleanLike = Field(
        default="",
        description="Check if the home is not the first structure exposed to ocean, bay, or sound",
    )

    plumbing_type: str = Field(
        default="",
        description=(
            'Type of plumbing in the building .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    roof_type: str = Field(
        default="",
        description=(
            "Type of roof covering (e.g., shingle, metal) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    wiring_type: str = Field(
        default="",
        description=(
            "Type of electrical wiring in the building .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    heating_type: str = Field(
        default="",
        description=(
            'Primary type of heating system .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    year_updated_plumbing: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year the plumbing was last updated"
    )

    year_updated_roof: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year the roof was last updated"
    )

    year_updated_wiring: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year the electrical wiring was last updated"
    )

    year_updated_heating: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year the heating system was last updated"
    )

    under_renovation_yes: BooleanLike = Field(
        default="", description="Check if the home is currently under any type of renovation"
    )

    under_renovation_no: BooleanLike = Field(
        default="", description="Check if the home is not currently under renovation"
    )

    renovation_cosmetic: BooleanLike = Field(
        default="", description="Check if renovations are cosmetic only"
    )

    renovation_structural: BooleanLike = Field(
        default="", description="Check if renovations are structural"
    )

    describe_renovations: str = Field(
        default="",
        description=(
            "Description of current or planned renovations .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class VacantOnly(BaseModel):
    """Additional information required when the premises is vacant"""

    term_desired_3_months: BooleanLike = Field(
        default="", description="Select if a 3-month term is desired (vacant only)"
    )

    term_desired_6_months: BooleanLike = Field(
        default="", description="Select if a 6-month term is desired (vacant only)"
    )

    term_desired_9_months: BooleanLike = Field(
        default="", description="Select if a 9-month term is desired (vacant only)"
    )

    term_desired_12_months: BooleanLike = Field(
        default="", description="Select if a 12-month term is desired (vacant only)"
    )

    vacant_how_long: str = Field(
        default="",
        description=(
            "Length of time the location has been vacant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    intended_use_building: str = Field(
        default="",
        description=(
            "Planned use or occupancy of the building .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProtectiveDevices(BaseModel):
    """Information about protective devices and safety systems"""

    central_fire_burglar_yes: BooleanLike = Field(
        default="", description="Check if central fire and burglar alarms are installed"
    )

    central_fire_burglar_no: BooleanLike = Field(
        default="", description="Check if central fire and burglar alarms are not installed"
    )

    gated_community_yes: BooleanLike = Field(
        default="", description="Check if the property is located in a gated community"
    )

    gated_community_no: BooleanLike = Field(
        default="", description="Check if the property is not located in a gated community"
    )

    sprinkler_system_yes: BooleanLike = Field(
        default="", description="Check if the building has a sprinkler system"
    )

    sprinkler_system_no: BooleanLike = Field(
        default="", description="Check if the building does not have a sprinkler system"
    )

    auto_water_shutoff_yes: BooleanLike = Field(
        default="", description="Check if automatic water shutoff or leak detection is installed"
    )

    auto_water_shutoff_no: BooleanLike = Field(
        default="",
        description="Check if automatic water shutoff or leak detection is not installed",
    )


class Exposures(BaseModel):
    """Special exposures and risk characteristics"""

    exposure_lapse_12_months: BooleanLike = Field(
        default="", description="Check if there has been a lapse in coverage greater than 12 months"
    )

    exposure_business_on_premises: BooleanLike = Field(
        default="", description="Check if there is any business conducted on the premises"
    )

    exposure_arson_fraud: BooleanLike = Field(
        default="", description="Check if there is any history or concern of arson or fraud"
    )

    exposure_farming_ranching_hunting: BooleanLike = Field(
        default="", description="Check if there is farming, ranching, or hunting exposure"
    )

    exposure_home_day_care: BooleanLike = Field(
        default="", description="Check if a home day care is operated at the premises"
    )

    exposure_asbestos_eifs: BooleanLike = Field(
        default="",
        description=(
            "Check if there is asbestos or EIFS (Exterior Insulation and Finish System) exposure"
        ),
    )

    exposure_woodstove_kerosene: BooleanLike = Field(
        default="", description="Check if there is a woodstove or kerosene heater in use"
    )

    exposure_aluminum_knob_tube: BooleanLike = Field(
        default="", description="Check if there is aluminum wiring or knob-and-tube wiring"
    )

    exposure_cabinet_auto_chemical: BooleanLike = Field(
        default="",
        description="Check if there is cabinet making, auto repair, or chemical processing exposure",
    )


class Coverages(BaseModel):
    """Requested coverages, limits, and options"""

    dwelling_coverage: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Coverage limit requested for the dwelling"
    )

    other_structures: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Coverage limit requested for other structures"
    )

    personal_property: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Coverage limit requested for personal property"
    )

    loss_of_use_rent: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Coverage limit requested for loss of use or rental value"
    )

    liability: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Coverage limit requested for liability"
    )

    med_pay: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Coverage limit requested for medical payments"
    )

    deductible_500: BooleanLike = Field(
        default="", description="Select if a $500 deductible is requested"
    )

    deductible_1000: BooleanLike = Field(
        default="", description="Select if a $1,000 deductible is requested"
    )

    deductible_2500: BooleanLike = Field(
        default="", description="Select if a $2,500 deductible is requested"
    )

    water_backup_5000: BooleanLike = Field(
        default="", description="Select if $5,000 water backup coverage is requested"
    )

    water_backup_10000: BooleanLike = Field(
        default="", description="Select if $10,000 water backup coverage is requested"
    )

    water_backup_15000: BooleanLike = Field(
        default="", description="Select if $15,000 water backup coverage is requested"
    )

    extended_repl_cost: str = Field(
        default="",
        description=(
            "Indicate if extended replacement cost is requested and any details/percentage "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    id_theft_yes: BooleanLike = Field(
        default="", description="Check to include identity theft coverage"
    )

    id_theft_no: BooleanLike = Field(
        default="", description="Check to exclude identity theft coverage"
    )

    personal_injury_yes: BooleanLike = Field(
        default="", description="Check to include personal injury coverage"
    )

    personal_injury_no: BooleanLike = Field(
        default="", description="Check to exclude personal injury coverage"
    )

    equipment_breakdown_yes: BooleanLike = Field(
        default="", description="Check to include equipment breakdown coverage"
    )

    equipment_breakdown_no: BooleanLike = Field(
        default="", description="Check to exclude equipment breakdown coverage"
    )

    ordinance_of_law_yes: BooleanLike = Field(
        default="", description="Check to include ordinance or law coverage"
    )

    ordinance_of_law_no: BooleanLike = Field(
        default="", description="Check to exclude ordinance or law coverage"
    )


class AdditionalInformationforUnderwriting(BaseModel):
    """Free-form additional underwriting details"""

    additional_info_underwriting_line_1: str = Field(
        default="",
        description=(
            "Additional underwriting information (first line) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_info_underwriting_line_2: str = Field(
        default="",
        description=(
            "Additional underwriting information (second line) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_info_underwriting_line_3: str = Field(
        default="",
        description=(
            "Additional underwriting information (third line) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PersonalLinesQuoteSheet(BaseModel):
    """Personal Lines Quote Sheet"""

    agency_information: AgencyInformation = Field(..., description="Agency Information")
    insured_information: InsuredInformation = Field(..., description="Insured Information")
    losses_in_past_5_years: LossesinPast5Years = Field(..., description="Losses in Past 5 Years")
    premises: Premises = Field(..., description="Premises")
    vacant_only: VacantOnly = Field(..., description="Vacant Only")
    protective_devices: ProtectiveDevices = Field(..., description="Protective Devices")
    exposures: Exposures = Field(..., description="Exposures")
    coverages: Coverages = Field(..., description="Coverages")
    additional_information_for_underwriting: AdditionalInformationforUnderwriting = Field(
        ..., description="Additional Information for Underwriting"
    )
