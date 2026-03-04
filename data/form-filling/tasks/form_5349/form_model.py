from typing import List, Literal, Optional, Union

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
    """Details about the agency submitting the quote"""

    agency: str = Field(
        ...,
        description=(
            "Name of the retail agency submitting the quote .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    agency_phone: str = Field(
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

    contact_email: str = Field(
        ...,
        description=(
            'Email address for the agency contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class InsuredInformation(BaseModel):
    """Information about the insured and prior history"""

    insured: str = Field(
        ...,
        description=(
            "Named insured (person or entity to be insured) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    effective_date: str = Field(..., description="Policy effective date")  # YYYY-MM-DD format

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
            'Insured\'s primary phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    dob: str = Field(..., description="Date of birth of the insured")  # YYYY-MM-DD format

    felony_conviction: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether the insured has ever been charged with or convicted of a felony"
        ),
    )

    felony_conviction_no: BooleanLike = Field(
        default="",
        description="Indicate that the insured has not been charged with or convicted of a felony",
    )

    bankruptcy_foreclosure_repossession: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether the insured has had bankruptcy, foreclosure, or repossession "
            "within the past 3 years"
        ),
    )

    bankruptcy_foreclosure_repossession_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate that the insured has not had bankruptcy, foreclosure, or repossession "
            "within the past 3 years"
        ),
    )


class LossesinPast5Years(BaseModel):
    """Schedule of prior losses in the last 5 years"""

    losses_past_5_years: List[LossesPast5YearsRow] = Field(
        default="",
        description=(
            "Schedule of all losses in the past 5 years including date, details, amount "
            "paid, and status"
        ),
    )  # List of table rows

    details_of_loss: str = Field(
        default="",
        description=(
            "Brief description of each loss (covered in the losses table) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    amount_paid: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid on each loss (covered in the losses table)"
    )

    open_closed: str = Field(
        default="",
        description=(
            "Status of each loss (open or closed) (covered in the losses table) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Premises(BaseModel):
    """Premises details and occupancy/use information"""

    form_requested_homeowners: BooleanLike = Field(
        ..., description="Check if a Homeowners form is requested"
    )

    form_requested_dwelling: BooleanLike = Field(
        default="", description="Check if a Dwelling form is requested"
    )

    form_requested_condo: BooleanLike = Field(
        default="", description="Check if a Condo form is requested"
    )

    form_requested_builders_risk: BooleanLike = Field(
        default="", description="Check if a Builders Risk form is requested"
    )

    owner: BooleanLike = Field(..., description="Check if the premises is owner-occupied")

    secondary_without_rental: BooleanLike = Field(
        default="", description="Check if the premises is a secondary residence without rental"
    )

    secondary_with_rental: BooleanLike = Field(
        default="", description="Check if the premises is a secondary residence with rental"
    )

    tenant: BooleanLike = Field(default="", description="Check if the premises is tenant-occupied")

    vacant: BooleanLike = Field(default="", description="Check if the premises is vacant")

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

    premises_address_different: str = Field(
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
            'City for the premises address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    premises_state: str = Field(default="", description="State for the premises address")

    premises_zip: str = Field(default="", description="ZIP code for the premises address")

    year_built: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year the building was originally constructed"
    )

    construction_type: str = Field(
        ...,
        description=(
            "Type of building construction (e.g., frame, masonry) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    protection_class: str = Field(
        ...,
        description=(
            "ISO or local fire protection class for the premises .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    square_feet: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total finished square footage of the dwelling"
    )

    number_of_stories: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of stories of the dwelling"
    )

    first_exposed_to_water: BooleanLike = Field(
        ...,
        description="Indicate if the home is the first structure exposed to ocean, bay, or sound",
    )

    first_exposed_to_water_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate that the home is not the first structure exposed to ocean, bay, or sound"
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
            'Primary type of heating system .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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

    under_renovation: BooleanLike = Field(
        default="", description="Indicate if the home is currently under any type of renovation"
    )

    under_renovation_no: BooleanLike = Field(
        default="", description="Indicate that the home is not currently under renovation"
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
            "Description of the renovations being performed .If you cannot fill this, write "
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

    how_long_vacant: str = Field(
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
            "Planned future use of the vacant building .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProtectiveDevices(BaseModel):
    """Information on protective devices and security features"""

    central_fire_burglar_alarms: BooleanLike = Field(
        default="", description="Indicate if central fire and burglar alarms are installed"
    )

    central_fire_burglar_alarms_no: BooleanLike = Field(
        default="", description="Indicate that central fire and burglar alarms are not installed"
    )

    gated_community: BooleanLike = Field(
        default="", description="Indicate if the premises is located in a gated community"
    )

    gated_community_no: BooleanLike = Field(
        default="", description="Indicate that the premises is not in a gated community"
    )

    sprinkler_system: BooleanLike = Field(
        default="", description="Indicate if an automatic sprinkler system is installed"
    )

    sprinkler_system_no: BooleanLike = Field(
        default="", description="Indicate that an automatic sprinkler system is not installed"
    )

    automatic_water_shutoff: BooleanLike = Field(
        default="", description="Indicate if automatic water shutoff or leak detection is installed"
    )

    automatic_water_shutoff_no: BooleanLike = Field(
        default="",
        description="Indicate that automatic water shutoff or leak detection is not installed",
    )


class Exposures(BaseModel):
    """Special exposures and risk characteristics"""

    lapse_over_12_months: BooleanLike = Field(
        default="", description="Check if there has been a lapse in coverage greater than 12 months"
    )

    business_on_premises: BooleanLike = Field(
        default="", description="Check if any business is conducted on the premises"
    )

    arson_or_fraud: BooleanLike = Field(
        default="", description="Check if there is any history or concern of arson or fraud"
    )

    farming_ranching_hunting: BooleanLike = Field(
        default="", description="Check if there is farming, ranching, or hunting exposure"
    )

    home_day_care: BooleanLike = Field(
        default="", description="Check if home day care operations are present"
    )

    asbestos_eifs: BooleanLike = Field(
        default="",
        description=(
            "Check if there is asbestos or EIFS (Exterior Insulation and Finish System) exposure"
        ),
    )

    woodstove_kerosene_heater: BooleanLike = Field(
        default="", description="Check if a woodstove or kerosene heater is used on the premises"
    )

    aluminum_knob_tube: BooleanLike = Field(
        default="", description="Check if aluminum wiring or knob-and-tube wiring is present"
    )

    cabinet_making_auto_repair_chemical_processor: BooleanLike = Field(
        default="",
        description="Check if cabinet making, auto repair, or chemical processing occurs on premises",
    )


class Coverages(BaseModel):
    """Requested coverages, limits, and options"""

    dwelling_coverage: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Limit of insurance requested for the dwelling building"
    )

    other_structures: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Limit of insurance for other structures (e.g., detached garage)"
    )

    personal_property: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Limit of insurance for personal property/contents"
    )

    loss_of_use_rent: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Limit for loss of use or loss of rental income"
    )

    liability: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Personal liability limit requested"
    )

    med_pay: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Medical payments to others limit"
    )

    deductible_500: BooleanLike = Field(..., description="Select if a $500 deductible is requested")

    deductible_1000: BooleanLike = Field(
        default="", description="Select if a $1,000 deductible is requested"
    )

    deductible_2500: BooleanLike = Field(
        default="", description="Select if a $2,500 deductible is requested"
    )

    water_backup_5000: BooleanLike = Field(
        default="", description="Select $5,000 limit for water backup coverage"
    )

    water_backup_10000: BooleanLike = Field(
        default="", description="Select $10,000 limit for water backup coverage"
    )

    water_backup_15000: BooleanLike = Field(
        default="", description="Select $15,000 limit for water backup coverage"
    )

    extended_replacement_cost: BooleanLike = Field(
        default="", description="Check if extended replacement cost coverage is requested"
    )

    id_theft: BooleanLike = Field(
        default="", description="Indicate if identity theft coverage is requested"
    )

    id_theft_no: BooleanLike = Field(
        default="", description="Indicate that identity theft coverage is not requested"
    )

    personal_injury: BooleanLike = Field(
        default="", description="Indicate if personal injury coverage is requested"
    )

    personal_injury_no: BooleanLike = Field(
        default="", description="Indicate that personal injury coverage is not requested"
    )

    equipment_breakdown: BooleanLike = Field(
        default="", description="Indicate if equipment breakdown coverage is requested"
    )

    equipment_breakdown_no: BooleanLike = Field(
        default="", description="Indicate that equipment breakdown coverage is not requested"
    )

    ordinance_of_law: BooleanLike = Field(
        default="", description="Indicate if ordinance or law coverage is requested"
    )

    ordinance_of_law_no: BooleanLike = Field(
        default="", description="Indicate that ordinance or law coverage is not requested"
    )


class AdditionalInformationforUnderwriting(BaseModel):
    """Free-form additional underwriting details"""

    additional_information_for_underwriting: str = Field(
        default="",
        description=(
            "Any additional comments or information relevant to underwriting this risk .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PersonalLinesQuoteSheet(BaseModel):
    """
    Personal Lines Quote Sheet

    Personal Lines Quote Sheet
    """

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
