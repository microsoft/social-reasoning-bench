from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


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

    agency_phone: str = Field(
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
            "Name of the primary contact at the agency .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    agency_email: str = Field(
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
            "Name of the insured individual or entity .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    effective_date: str = Field(
        ..., description="Requested policy effective date"
    )  # YYYY-MM-DD format

    insured_address: str = Field(
        ...,
        description=(
            'Mailing address of the insured .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    insured_city: str = Field(
        ...,
        description=(
            "City for the insured's mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    insured_state: str = Field(..., description="State for the insured's mailing address")

    insured_zip: str = Field(..., description="ZIP code for the insured's mailing address")

    insured_phone: str = Field(
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
        description="Indicate YES if the insured has ever been charged with or convicted of a felony",
    )

    felony_no: BooleanLike = Field(
        default="",
        description="Indicate NO if the insured has not been charged with or convicted of a felony",
    )

    bankruptcy_3yrs_yes: BooleanLike = Field(
        default="",
        description=(
            "Indicate YES if the insured has had bankruptcy, foreclosure, or repossession "
            "within the past 3 years"
        ),
    )

    bankruptcy_3yrs_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate NO if the insured has not had bankruptcy, foreclosure, or "
            "repossession within the past 3 years"
        ),
    )


class LossesinPast5Years(BaseModel):
    """Prior loss history for the insured"""

    date_of_loss: str = Field(
        default="", description="Date each loss occurred within the past 5 years"
    )  # YYYY-MM-DD format

    details_of_loss: str = Field(
        default="",
        description=(
            "Brief description of each loss within the past 5 years .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    amount_paid: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid on each loss"
    )

    open_closed: Literal["Open", "Closed", "N/A", ""] = Field(
        default="", description="Status of each loss (open or closed)"
    )


class Premises(BaseModel):
    """Information about the premises and occupancy"""

    form_requested_homeowners: BooleanLike = Field(
        default="", description="Check if Homeowners form is requested"
    )

    form_requested_dwelling: BooleanLike = Field(
        default="", description="Check if Dwelling form is requested"
    )

    form_requested_condo: BooleanLike = Field(
        default="", description="Check if Condo form is requested"
    )

    form_requested_builders_risk: BooleanLike = Field(
        default="", description="Check if Builders Risk form is requested"
    )

    occupancy_owner: BooleanLike = Field(
        default="", description="Check if premises is owner-occupied"
    )

    occupancy_secondary_no_rental: BooleanLike = Field(
        default="", description="Check if premises is a secondary residence without rental"
    )

    occupancy_secondary_with_rental: BooleanLike = Field(
        default="", description="Check if premises is a secondary residence with rental"
    )

    occupancy_tenant: BooleanLike = Field(
        default="", description="Check if premises is tenant-occupied"
    )

    occupancy_vacant: BooleanLike = Field(default="", description="Check if premises is vacant")

    weeks_rented_annually: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of weeks per year the property is rented"
    )

    premises_address_if_different: str = Field(
        default="",
        description=(
            "Premises address if different from insured mailing address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    premises_city: str = Field(
        default="",
        description=(
            "City where the insured premises is located .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    premises_state: str = Field(
        default="", description="State where the insured premises is located"
    )

    premises_zip: str = Field(
        default="", description="ZIP code where the insured premises is located"
    )

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
            "ISO protection class for the property location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    short_term_rental_yes: BooleanLike = Field(
        default="",
        description="Indicate YES if the property is used as a short-term rental (e.g., Airbnb)",
    )

    short_term_rental_no: BooleanLike = Field(
        default="", description="Indicate NO if the property is not used as a short-term rental"
    )

    square_feet: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total finished square footage of the dwelling"
    )

    number_of_stories: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of stories in the dwelling"
    )

    first_exposed_ocean_yes: BooleanLike = Field(
        default="",
        description="Indicate YES if the home is the first structure exposed to ocean, bay, or sound",
    )

    first_exposed_ocean_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate NO if the home is not the first structure exposed to ocean, bay, or sound"
        ),
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
            "Type of roof covering (e.g., shingle, metal) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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
            "Primary type of heating system in the dwelling .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    year_updated_plumbing: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Most recent year the plumbing was updated"
    )

    year_updated_roof: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Most recent year the roof was updated"
    )

    year_updated_wiring: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Most recent year the wiring was updated"
    )

    year_updated_heating: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Most recent year the heating system was updated"
    )

    under_renovation_yes: BooleanLike = Field(
        default="", description="Indicate YES if the home is currently under any type of renovation"
    )

    under_renovation_no: BooleanLike = Field(
        default="", description="Indicate NO if the home is not currently under renovation"
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
            "Detailed description of current or planned renovations .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
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

    vacant_duration: str = Field(
        default="",
        description=(
            "Length of time the location has been vacant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    intended_use_of_building: str = Field(
        default="",
        description=(
            "Planned or current use of the vacant building .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProtectiveDevices(BaseModel):
    """Protective systems and devices at the premises"""

    central_fire_burglar_yes: BooleanLike = Field(
        default="", description="Indicate YES if central fire and burglar alarms are installed"
    )

    central_fire_burglar_no: BooleanLike = Field(
        default="", description="Indicate NO if central fire and burglar alarms are not installed"
    )

    gated_community_yes: BooleanLike = Field(
        default="", description="Indicate YES if the property is located in a gated community"
    )

    gated_community_no: BooleanLike = Field(
        default="", description="Indicate NO if the property is not located in a gated community"
    )

    sprinkler_system_yes: BooleanLike = Field(
        default="", description="Indicate YES if an automatic sprinkler system is installed"
    )

    sprinkler_system_no: BooleanLike = Field(
        default="", description="Indicate NO if an automatic sprinkler system is not installed"
    )

    auto_water_shutoff_yes: BooleanLike = Field(
        default="",
        description="Indicate YES if automatic water shutoff or leak detection is installed",
    )

    auto_water_shutoff_no: BooleanLike = Field(
        default="",
        description="Indicate NO if automatic water shutoff or leak detection is not installed",
    )


class Exposures(BaseModel):
    """Special exposures and risk characteristics"""

    exposure_lapse_12_months: BooleanLike = Field(
        default="", description="Check if there has been a lapse in coverage greater than 12 months"
    )

    exposure_business_on_premises: BooleanLike = Field(
        default="", description="Check if any business is conducted on the premises"
    )

    exposure_arson_or_fraud: BooleanLike = Field(
        default="", description="Check if there is any history or concern of arson or fraud"
    )

    exposure_farming_ranching_hunting: BooleanLike = Field(
        default="",
        description="Check if farming, ranching, or hunting activities occur on the premises",
    )

    exposure_home_day_care: BooleanLike = Field(
        default="", description="Check if a home day care is operated at the premises"
    )

    exposure_asbestos_eifs: BooleanLike = Field(
        default="",
        description="Check if asbestos or EIFS (Exterior Insulation and Finish System) is present",
    )

    exposure_woodstove_kerosene: BooleanLike = Field(
        default="", description="Check if a woodstove or kerosene heater is used on the premises"
    )

    exposure_aluminum_knob_tube: BooleanLike = Field(
        default="", description="Check if aluminum wiring or knob-and-tube wiring is present"
    )

    exposure_cabinet_auto_chemical: BooleanLike = Field(
        default="",
        description="Check if cabinet making, auto repair, or chemical processing occurs on premises",
    )


class Coverages(BaseModel):
    """Requested coverages, limits, and options"""

    coverage_dwelling: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Limit of insurance requested for the dwelling building"
    )

    coverage_other_structures: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Limit of insurance requested for other structures"
    )

    coverage_personal_property: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Limit of insurance requested for personal property"
    )

    coverage_loss_of_use_rent: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Limit of insurance requested for loss of use or rental value"
    )

    coverage_liability: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Limit of liability coverage requested"
    )

    coverage_med_pay: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Limit of medical payments coverage requested"
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

    extended_replacement_cost: BooleanLike = Field(
        default="", description="Check if extended replacement cost coverage is requested"
    )

    id_theft_yes: BooleanLike = Field(
        default="", description="Indicate YES if identity theft coverage is requested"
    )

    id_theft_no: BooleanLike = Field(
        default="", description="Indicate NO if identity theft coverage is not requested"
    )

    personal_injury_yes: BooleanLike = Field(
        default="", description="Indicate YES if personal injury coverage is requested"
    )

    personal_injury_no: BooleanLike = Field(
        default="", description="Indicate NO if personal injury coverage is not requested"
    )

    equipment_breakdown_yes: BooleanLike = Field(
        default="", description="Indicate YES if equipment breakdown coverage is requested"
    )

    equipment_breakdown_no: BooleanLike = Field(
        default="", description="Indicate NO if equipment breakdown coverage is not requested"
    )

    ordinance_of_law_yes: BooleanLike = Field(
        default="", description="Indicate YES if ordinance or law coverage is requested"
    )

    ordinance_of_law_no: BooleanLike = Field(
        default="", description="Indicate NO if ordinance or law coverage is not requested"
    )


class AdditionalInformationforUnderwriting(BaseModel):
    """Free-form additional underwriting details"""

    additional_underwriting_info: str = Field(
        default="",
        description=(
            "Any additional information or comments relevant to underwriting this risk .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
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
