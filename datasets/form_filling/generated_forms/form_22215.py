from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class BrokerInsuredInformation(BaseModel):
    """Broker details, insured details, and basic policy information"""

    is_the_property_undergoing_any_renovation: BooleanLike = Field(
        ...,
        description="Indicate whether the property is currently undergoing any renovation work.",
    )

    brokerage: str = Field(
        ...,
        description=(
            "Name of the brokerage submitting this application. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    broker_contact: str = Field(
        ...,
        description=(
            "Name of the primary broker contact person. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    broker_address: str = Field(
        ...,
        description=(
            'Mailing address of the brokerage. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Email address for the broker contact. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    named_insured: str = Field(
        ...,
        description=(
            'Full legal name of the insured party. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    broker_code: str = Field(
        default="",
        description=(
            "Brokerage or producer code, if applicable. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            "Mailing address for the named insured. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    effective_date: str = Field(
        ..., description="Requested effective date of coverage."
    )  # YYYY-MM-DD format

    policy_term: str = Field(
        ...,
        description=(
            "Length of the policy term (e.g., 6 months, 1 year). .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    location_address: str = Field(
        ...,
        description=(
            "Physical address of the insured condo unit. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mortgagees: str = Field(
        default="",
        description=(
            "Name(s) of any mortgagee(s) with an interest in the property. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    mortgagees_address: str = Field(
        default="",
        description=(
            'Mailing address for the mortgagee(s). .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    other_policies_with_abex: str = Field(
        default="",
        description=(
            "List any other policies the insured has with ABEX. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    prior_insurance_expiry_date: str = Field(
        default="",
        description=(
            "Details of prior insurance coverage and its expiry date. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class UnderwritingDetails(BaseModel):
    """Ownership, vacancy, usage, risk and exposure information"""

    is_condo_corporation_registered: BooleanLike = Field(
        ..., description="Indicate whether the condo corporation is formally registered."
    )

    does_the_insured_own_the_condo_unit: BooleanLike = Field(
        ..., description="Confirm whether the applicant is the owner of the condo unit."
    )

    has_applicant_ever_had_insurance_declined_or_cancelled: BooleanLike = Field(
        ..., description="Indicate if the applicant has ever had insurance declined or cancelled."
    )

    building_type_single_family_row_house_highrise_etc: str = Field(
        ...,
        description=(
            "Describe the building type (e.g., single family, row house, highrise). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    hydrant_within_300_meters: BooleanLike = Field(
        ...,
        description="Indicate whether there is a fire hydrant within 300 meters of the property.",
    )

    how_long_has_the_risk_been_vacant: str = Field(
        ...,
        description=(
            "Length of time the condo unit has been vacant. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    firehall_within_8_kms: BooleanLike = Field(
        ..., description="Indicate whether there is a firehall within 8 kilometers of the property."
    )

    use_occupancy_prior_to_vacancy: str = Field(
        ...,
        description=(
            "Describe how the unit was used or occupied before it became vacant. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    is_it_a_voluntary_firehall: BooleanLike = Field(
        ..., description="Indicate whether the responding firehall is staffed by volunteers."
    )

    reason_for_vacancy: str = Field(
        ...,
        description=(
            "Explain why the condo unit is currently vacant. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    will_utilities_be_maintained: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether utilities (e.g., heat, electricity, water) will remain on "
            "during vacancy."
        ),
    )

    who_is_responsible_for_snow_removal: str = Field(
        ...,
        description=(
            "Identify the party responsible for snow removal at the property. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    is_there_a_sump_pump: BooleanLike = Field(
        ..., description="Indicate whether the property has a sump pump installed."
    )

    if_the_applicant_does_not_live_within_100_kms_of_the_property_who_will_be_responsible_for_maintaining_the_property: str = Field(
        ...,
        description=(
            "Provide details of the person or company responsible for maintaining the "
            "property if the applicant lives more than 100 km away. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    describe_future_plans_for_this_property: str = Field(
        ...,
        description=(
            "Describe any intended future use, sale, renovation, or occupancy plans for the "
            'property. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    is_there_a_pool_and_or_hot_tub_located_on_the_premises: BooleanLike = Field(
        ..., description="Indicate whether there is a swimming pool and/or hot tub on the property."
    )

    is_the_risk_located_in_an_active_flood_zone: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether the property is located in an active flood zone. If yes, the "
            "risk will be declined."
        ),
    )

    is_the_risk_located_within_50_kms_of_an_active_fire_zone: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether the property is within 50 km of an active fire zone. If yes, "
            "the risk will be declined."
        ),
    )


class ConstructionDetails(BaseModel):
    """Building construction, age, updates, and private protections"""

    year_built: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year the building was originally constructed."
    )

    unit_area_in_sq_feet: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total area of the condo unit in square feet."
    )

    construction: str = Field(
        ...,
        description=(
            "Type of construction (e.g., brick, frame, concrete). .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    no_of_stories: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of storeys in the building."
    )

    electrical_year_updated: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year in which the electrical system was last updated."
    )

    amperage_year_updated: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year in which the electrical amperage or panel was last updated."
    )

    plumbing_year_updated: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year in which the plumbing system was last updated."
    )

    heating_year_updated: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year in which the primary heating system was last updated."
    )

    supplementary_heating_year_updated: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Year in which any supplementary heating (e.g., space heaters, wood stoves) was "
            "last updated."
        ),
    )

    roof_year_updated: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year in which the roof was last updated or replaced."
    )

    fire_alarm: BooleanLike = Field(
        default="",
        description="Indicate whether the property is equipped with a fire alarm system.",
    )

    burglar_alarm: BooleanLike = Field(
        default="",
        description="Indicate whether the property has a burglar or intrusion alarm system.",
    )

    monitored: BooleanLike = Field(
        default="",
        description="Indicate whether the alarm systems are monitored by a central station.",
    )

    sprinklered: BooleanLike = Field(
        default="", description="Indicate whether the building is protected by a sprinkler system."
    )

    on_site_security: BooleanLike = Field(
        default="",
        description="Indicate whether there is on-site security personnel at the property.",
    )

    comments: str = Field(
        default="",
        description=(
            "Additional information or explanations, including details if insurance was "
            'previously declined or cancelled. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class AbexVacantCondoApplication(BaseModel):
    """ABEX

    Vacant Condo Application"""

    broker__insured_information: BrokerInsuredInformation = Field(
        ..., description="Broker & Insured Information"
    )
    underwriting_details: UnderwritingDetails = Field(..., description="Underwriting Details")
    construction_details: ConstructionDetails = Field(..., description="Construction Details")
