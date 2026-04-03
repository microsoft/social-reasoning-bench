from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class LossesPast5YearsRow(BaseModel):
    """Single row in Date of Loss"""

    date_of_loss: str = Field(default="", description="Date_Of_Loss")
    details_of_loss: str = Field(default="", description="Details_Of_Loss")
    amount_paid: str = Field(default="", description="Amount_Paid")
    open_closed: str = Field(default="", description="Open_Closed")


class AgencyInformation(BaseModel):
    """Producing agency contact details"""

    agency: str = Field(
        ...,
        description=(
            "Name of the agency submitting the quote .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_agency: str = Field(
        ...,
        description=(
            'Agency phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    contact_person: str = Field(
        ...,
        description=(
            'Primary contact person at the agency .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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
    """Primary insured details and prior history"""

    insured: str = Field(
        ...,
        description=(
            'Name of the insured .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    effective_date: str = Field(..., description="Policy effective date")  # YYYY-MM-DD format

    address_mailing: str = Field(
        ...,
        description=(
            'Mailing street address of the insured .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city_mailing: str = Field(
        ...,
        description=(
            'Mailing city of the insured .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    phone_insured: str = Field(
        ...,
        description=(
            'Insured\'s phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    dob: str = Field(default="", description="Date of birth of the insured")  # YYYY-MM-DD format

    state_mailing: str = Field(..., description="Mailing state of the insured")

    zip_mailing: str = Field(..., description="Mailing ZIP code of the insured")

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
            "Check if there has been bankruptcy, foreclosure, or repossession within the "
            "past 3 years"
        ),
    )

    bankruptcy_3yrs_no: BooleanLike = Field(
        default="",
        description=(
            "Check if there has not been bankruptcy, foreclosure, or repossession within "
            "the past 3 years"
        ),
    )

    losses_past_5_years: List[LossesPast5YearsRow] = Field(
        default_factory=list,
        description=(
            "Schedule of losses in the past 5 years including date, details, amount paid, "
            "and status"
        ),
    )  # List of table rows


class Premises(BaseModel):
    """Location, occupancy, and building characteristics"""

    form_requested_homeowners: BooleanLike = Field(
        default="", description="Select if Homeowners form is requested"
    )

    form_requested_dwelling: BooleanLike = Field(
        default="", description="Select if Dwelling form is requested"
    )

    form_requested_condo: BooleanLike = Field(
        default="", description="Select if Condo form is requested"
    )

    form_requested_builders_risk: BooleanLike = Field(
        default="", description="Select if Builders Risk form is requested"
    )

    owner: BooleanLike = Field(default="", description="Check if premises is owner-occupied")

    secondary_without_rental: BooleanLike = Field(
        default="", description="Check if premises is a secondary residence without rental"
    )

    secondary_with_rental: BooleanLike = Field(
        default="", description="Check if premises is a secondary residence with rental"
    )

    tenant: BooleanLike = Field(default="", description="Check if premises is tenant-occupied")

    vacant: BooleanLike = Field(default="", description="Check if premises is vacant")

    if_rental: str = Field(
        default="",
        description=(
            "Additional details if the property is rented .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    weeks_rented_annually: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of weeks per year the property is rented"
    )

    address_premises: str = Field(
        default="",
        description=(
            "Premises address if different from mailing address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_premises: str = Field(
        default="",
        description=(
            'City of the insured premises .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state_premises: str = Field(default="", description="State of the insured premises")

    zip_premises: str = Field(default="", description="ZIP code of the insured premises")

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
            'Type of plumbing in the dwelling .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    roof_type: str = Field(
        default="",
        description=(
            'Type of roof on the dwelling .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    wiring_type: str = Field(
        default="",
        description=(
            "Type of electrical wiring in the dwelling .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    heating_type: str = Field(
        default="",
        description=(
            "Type of heating system in the dwelling .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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
    """Additional details when the premises is vacant"""

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
            "Planned or current use of the vacant building .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProtectiveDevices(BaseModel):
    """Protective systems and community security features"""

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
        default="", description="Check if a sprinkler system is installed"
    )

    sprinkler_system_no: BooleanLike = Field(
        default="", description="Check if a sprinkler system is not installed"
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

    exposure_arson_or_fraud: BooleanLike = Field(
        default="", description="Check if there is any history or concern of arson or fraud"
    )

    exposure_farming_ranching_hunting: BooleanLike = Field(
        default="", description="Check if there is farming, ranching, or hunting exposure"
    )

    exposure_home_day_care: BooleanLike = Field(
        default="", description="Check if there is a home day care operation"
    )

    exposure_asbestos_eifs: BooleanLike = Field(
        default="", description="Check if there is asbestos or EIFS exposure"
    )

    exposure_woodstove_kerosene: BooleanLike = Field(
        default="", description="Check if there is a woodstove or kerosene heater on premises"
    )

    exposure_aluminum_knob_tube: BooleanLike = Field(
        default="", description="Check if there is aluminum or knob-and-tube wiring"
    )

    exposure_cabinet_auto_chemical: BooleanLike = Field(
        default="",
        description="Check if there is cabinet making, auto repair, or chemical processing exposure",
    )


class Coverages(BaseModel):
    """Requested coverage limits and options"""

    dwelling_limit: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Requested dwelling coverage limit"
    )

    other_structures_limit: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Requested coverage limit for other structures"
    )

    personal_property_limit: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Requested personal property coverage limit"
    )

    loss_of_use_rent_limit: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Requested loss of use or rental income coverage limit"
    )

    liability_limit: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Requested liability coverage limit"
    )

    med_pay_limit: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Requested medical payments coverage limit"
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

    extended_repl_cost_yes: BooleanLike = Field(
        default="", description="Check to include extended replacement cost coverage"
    )

    extended_repl_cost_no: BooleanLike = Field(
        default="", description="Check if extended replacement cost coverage is not requested"
    )

    id_theft_yes: BooleanLike = Field(
        default="", description="Check to include identity theft coverage"
    )

    id_theft_no: BooleanLike = Field(
        default="", description="Check if identity theft coverage is not requested"
    )

    personal_injury_yes: BooleanLike = Field(
        default="", description="Check to include personal injury coverage"
    )

    personal_injury_no: BooleanLike = Field(
        default="", description="Check if personal injury coverage is not requested"
    )

    equipment_breakdown_yes: BooleanLike = Field(
        default="", description="Check to include equipment breakdown coverage"
    )

    equipment_breakdown_no: BooleanLike = Field(
        default="", description="Check if equipment breakdown coverage is not requested"
    )

    ordinance_of_law_yes: BooleanLike = Field(
        default="", description="Check to include ordinance or law coverage"
    )

    ordinance_of_law_no: BooleanLike = Field(
        default="", description="Check if ordinance or law coverage is not requested"
    )


class AdditionalInformationforUnderwriting(BaseModel):
    """Free-form underwriting notes"""

    additional_info_line_1: str = Field(
        default="",
        description=(
            "Additional underwriting information (line 1) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    additional_info_line_2: str = Field(
        default="",
        description=(
            "Additional underwriting information (line 2) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    additional_info_line_3: str = Field(
        default="",
        description=(
            "Additional underwriting information (line 3) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    additional_info_line_4: str = Field(
        default="",
        description=(
            "Additional underwriting information (line 4) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    additional_info_line_5: str = Field(
        default="",
        description=(
            "Additional underwriting information (line 5) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PersonalLinesQuoteSheet(BaseModel):
    """
    Personal Lines Quote Sheet

    ''
    """

    agency_information: AgencyInformation = Field(..., description="Agency Information")
    insured_information: InsuredInformation = Field(..., description="Insured Information")
    premises: Premises = Field(..., description="Premises")
    vacant_only: VacantOnly = Field(..., description="Vacant Only")
    protective_devices: ProtectiveDevices = Field(..., description="Protective Devices")
    exposures: Exposures = Field(..., description="Exposures")
    coverages: Coverages = Field(..., description="Coverages")
    additional_information_for_underwriting: AdditionalInformationforUnderwriting = Field(
        ..., description="Additional Information for Underwriting"
    )
