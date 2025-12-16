from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class BrokerPolicyInformation(BaseModel):
    """Broker details and basic policy information"""

    broker: str = Field(
        ...,
        description=(
            "Name of the insurance broker handling this application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    broker_number: str = Field(
        ...,
        description=(
            "Identification or code number assigned to the broker .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    broker_license_number: str = Field(
        ...,
        description=(
            'Official license number of the broker .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    policy_and_or_renewal_number: str = Field(
        default="",
        description=(
            "Existing policy or renewal number, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    requested_effective_date: str = Field(
        ..., description="Date on which coverage should begin"
    )  # YYYY-MM-DD format


class ApplicantInformation(BaseModel):
    """Applicant identity, contact, and ownership structure"""

    applicant: str = Field(
        ...,
        description=(
            "Name of the individual applying for coverage .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    business_name: str = Field(
        default="",
        description=(
            "Legal or trade name of the business entity .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            "Primary mailing street address for the applicant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            "City for the applicant's mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    county: str = Field(
        ...,
        description=(
            "County for the applicant's mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State for the applicant's mailing address")

    zip: str = Field(..., description="ZIP or postal code for the applicant's mailing address")

    phone: str = Field(
        ...,
        description=(
            "Primary contact phone number for the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    website: str = Field(
        default="",
        description=(
            'Applicant or business website URL .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Primary email address for the applicant or contact .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_person: str = Field(
        ...,
        description=(
            "Name of the primary contact person for this application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    applicants_ownership_structure_individual: BooleanLike = Field(
        ..., description="Check if the applicant is an individual owner"
    )

    applicants_ownership_structure_corporation: BooleanLike = Field(
        ..., description="Check if the applicant is a corporation"
    )

    applicants_ownership_structure_association: BooleanLike = Field(
        ..., description="Check if the applicant is an association"
    )

    applicants_ownership_structure_partnership: BooleanLike = Field(
        ..., description="Check if the applicant is a partnership"
    )


class EventLocationFacilityInformation(BaseModel):
    """Location of the event and facility ownership/lease details"""

    use: str = Field(
        ...,
        description=(
            "Description of the use or nature of the equine event .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_location_of_event: str = Field(
        default="",
        description=(
            "Street address of the event location if different from mailing address .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    city_location_of_event: str = Field(
        default="",
        description=(
            'City where the event will be held .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    county_location_of_event: str = Field(
        default="",
        description=(
            'County where the event will be held .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state_location_of_event: str = Field(
        default="", description="State where the event will be held"
    )

    zip_location_of_event: str = Field(
        default="", description="ZIP or postal code for the event location"
    )

    does_the_applicant_own_the_facilities_utilized_by_the_applicant: BooleanLike = Field(
        ..., description="Indicate if the applicant owns the facilities used for the event"
    )

    does_the_applicant_lease_the_facilities_utilized_by_the_applicant: BooleanLike = Field(
        ..., description="Indicate if the applicant leases the facilities used for the event"
    )


class CurrentInsuranceLossHistory(BaseModel):
    """Existing insurance coverage and prior claims/cancellations"""

    is_applicant_currently_insured_yes: BooleanLike = Field(
        ..., description="Check if the applicant is currently insured"
    )

    is_applicant_currently_insured_no: BooleanLike = Field(
        ..., description="Check if the applicant is not currently insured"
    )

    most_recent_or_present_insurance_company: str = Field(
        default="",
        description=(
            "Name of the most recent or current liability insurance company .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    annual_premium: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Annual premium amount for the most recent or current policy"
    )

    has_the_applicant_had_any_liability_claims_or_reported_incidents_in_the_past_five_years_yes: BooleanLike = Field(
        ...,
        description=(
            "Check if the applicant has had liability claims or incidents in the past five years"
        ),
    )

    has_the_applicant_had_any_liability_claims_or_reported_incidents_in_the_past_five_years_no: BooleanLike = Field(
        ...,
        description=(
            "Check if the applicant has not had liability claims or incidents in the past "
            "five years"
        ),
    )

    has_the_applicant_had_coverage_cancelled_or_refused_in_the_past_five_years_yes: BooleanLike = (
        Field(
            ...,
            description="Check if coverage has been cancelled or refused in the past five years",
        )
    )

    has_the_applicant_had_coverage_cancelled_or_refused_in_the_past_five_years_no: BooleanLike = Field(
        ...,
        description="Check if coverage has not been cancelled or refused in the past five years",
    )


class LimitsofLiability(BaseModel):
    """Selected liability limits and aggregate options"""

    each_occurrence_limit_300000: BooleanLike = Field(
        ..., description="Select this option for a $300,000 each occurrence limit"
    )

    each_occurrence_limit_500000: BooleanLike = Field(
        ..., description="Select this option for a $500,000 each occurrence limit"
    )

    each_occurrence_limit_1000000: BooleanLike = Field(
        ..., description="Select this option for a $1,000,000 each occurrence limit"
    )

    general_aggregate_limit_300000: BooleanLike = Field(
        ..., description="Select this option for a $300,000 general aggregate limit"
    )

    general_aggregate_limit_500000: BooleanLike = Field(
        ..., description="Select this option for a $500,000 general aggregate limit"
    )

    general_aggregate_limit_1000000: BooleanLike = Field(
        ..., description="Select this option for a $1,000,000 general aggregate limit"
    )

    fire_damage_limit_any_one_fire_50000_option_1: BooleanLike = Field(
        default="",
        description=(
            "First $50,000 fire damage limit option (aligned with occurrence/aggregate selection)"
        ),
    )

    fire_damage_limit_any_one_fire_50000_option_2: BooleanLike = Field(
        default="",
        description=(
            "Second $50,000 fire damage limit option (aligned with occurrence/aggregate selection)"
        ),
    )

    fire_damage_limit_any_one_fire_50000_option_3: BooleanLike = Field(
        default="",
        description=(
            "Third $50,000 fire damage limit option (aligned with occurrence/aggregate selection)"
        ),
    )

    medical_payments_any_one_person_5000_option_1: BooleanLike = Field(
        default="",
        description=(
            "First $5,000 medical payments limit option (aligned with occurrence/aggregate "
            "selection)"
        ),
    )

    medical_payments_any_one_person_5000_option_2: BooleanLike = Field(
        default="",
        description=(
            "Second $5,000 medical payments limit option (aligned with occurrence/aggregate "
            "selection)"
        ),
    )

    medical_payments_any_one_person_5000_option_3: BooleanLike = Field(
        default="",
        description=(
            "Third $5,000 medical payments limit option (aligned with occurrence/aggregate "
            "selection)"
        ),
    )

    double_aggregate_limit_desired_yes: BooleanLike = Field(
        default="", description="Check to request a double aggregate limit"
    )

    double_aggregate_limit_desired_no: BooleanLike = Field(
        default="", description="Check to decline a double aggregate limit"
    )

    double_aggregate_limit_600000: BooleanLike = Field(
        default="", description="Select a double aggregate limit of $600,000"
    )

    double_aggregate_limit_1000000: BooleanLike = Field(
        default="", description="Select a double aggregate limit of $1,000,000"
    )

    double_aggregate_limit_2000000: BooleanLike = Field(
        default="", description="Select a double aggregate limit of $2,000,000"
    )

    triple_aggregate_limit_desired_yes: BooleanLike = Field(
        default="",
        description=(
            "Check to request a triple aggregate limit (only available with $1,000,000 "
            "occurrence limit)"
        ),
    )

    triple_aggregate_limit_desired_no: BooleanLike = Field(
        default="", description="Check to decline a triple aggregate limit"
    )

    triple_aggregate_limit_na_option_1: BooleanLike = Field(
        default="",
        description=(
            "First N/A option for triple aggregate limit (not applicable for certain "
            "occurrence limits)"
        ),
    )

    triple_aggregate_limit_na_option_2: BooleanLike = Field(
        default="",
        description=(
            "Second N/A option for triple aggregate limit (not applicable for certain "
            "occurrence limits)"
        ),
    )

    triple_aggregate_limit_3000000: BooleanLike = Field(
        default="", description="Select a triple aggregate limit of $3,000,000"
    )


class OptionalCoverages(BaseModel):
    """Additional coverage options requested"""

    products_and_completed_operations_desired_yes: BooleanLike = Field(
        default="", description="Check to include Products and Completed Operations coverage"
    )

    products_and_completed_operations_desired_no: BooleanLike = Field(
        default="", description="Check to exclude Products and Completed Operations coverage"
    )

    personal_and_advertising_injury_desired_yes: BooleanLike = Field(
        default="", description="Check to include Personal and Advertising Injury coverage"
    )

    personal_and_advertising_injury_desired_no: BooleanLike = Field(
        default="", description="Check to exclude Personal and Advertising Injury coverage"
    )


class AdditionalInsureds(BaseModel):
    """Additional insured parties and their relationship to the event"""

    additional_insured_1_name: str = Field(
        default="",
        description=(
            'Name of the first additional insured .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    additional_insured_1_address: str = Field(
        default="",
        description=(
            "Address of the first additional insured .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    additional_insured_1_relationship: str = Field(
        default="",
        description=(
            "Relationship of the first additional insured to the event (e.g., land owner, "
            'facility owner) .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    additional_insured_2_name: str = Field(
        default="",
        description=(
            'Name of the second additional insured .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    additional_insured_2_address: str = Field(
        default="",
        description=(
            "Address of the second additional insured .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    additional_insured_2_relationship: str = Field(
        default="",
        description=(
            "Relationship of the second additional insured to the event .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_insured_3_name: str = Field(
        default="",
        description=(
            'Name of the third additional insured .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    additional_insured_3_address: str = Field(
        default="",
        description=(
            "Address of the third additional insured .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    additional_insured_3_relationship: str = Field(
        default="",
        description=(
            "Relationship of the third additional insured to the event .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class EquineEventLiabilityApplication(BaseModel):
    """
    Equine Event Liability Application

    ''
    """

    broker__policy_information: BrokerPolicyInformation = Field(
        ..., description="Broker & Policy Information"
    )
    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    event_location__facility_information: EventLocationFacilityInformation = Field(
        ..., description="Event Location & Facility Information"
    )
    current_insurance__loss_history: CurrentInsuranceLossHistory = Field(
        ..., description="Current Insurance & Loss History"
    )
    limits_of_liability: LimitsofLiability = Field(..., description="Limits of Liability")
    optional_coverages: OptionalCoverages = Field(..., description="Optional Coverages")
    additional_insureds: AdditionalInsureds = Field(..., description="Additional Insureds")
