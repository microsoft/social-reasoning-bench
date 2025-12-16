from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class BrokerInformation(BaseModel):
    """Details about the brokerage and broker contact for this application"""

    brokerage: str = Field(
        ...,
        description=(
            "Name of the brokerage firm submitting this application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    broker_contact: str = Field(
        ...,
        description=(
            "Name of the primary broker contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    broker_address: str = Field(
        ...,
        description=(
            'Mailing address of the brokerage .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    broker_code: str = Field(
        default="",
        description=(
            "Brokerage code or producer code, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    policy_number_for_renewal_purposes_only: str = Field(
        default="",
        description=(
            "Existing policy number if this is a renewal .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    effective_date: str = Field(
        ..., description="Requested effective date of coverage"
    )  # YYYY-MM-DD format


class InsuredInformation(BaseModel):
    """Basic information about the insureds and their mailing address"""

    full_names_of_all_insureds: str = Field(
        ...,
        description=(
            "Full legal names of all individuals or entities to be insured .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    names_of_principals: str = Field(
        ...,
        description=(
            "Names of the principal owners, partners, or officers of the insured .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            'Mailing address for the insured .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class UnderwritingDetails(BaseModel):
    """Current insurance details and general underwriting information"""

    expiry_date: str = Field(
        ..., description="Expiry date of current Commercial General Liability insurance"
    )  # YYYY-MM-DD format

    limit: str = Field(
        ...,
        description=(
            "Limit of liability on the current Commercial General Liability policy .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    deductible: str = Field(
        ...,
        description=(
            "Deductible amount on the current Commercial General Liability policy .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    premium: str = Field(
        ...,
        description=(
            "Annual premium for the current Commercial General Liability policy .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    insurer: str = Field(
        ...,
        description=(
            "Name of the current Commercial General Liability insurer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    nature_of_your_business_activities_including_website_address: str = Field(
        ...,
        description=(
            "Full description of business operations and website URL; attach brochure if no "
            'website .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    number_of_years_in_business_and_experience_of_insured: str = Field(
        ...,
        description=(
            "Number of years the business has operated and relevant experience of the "
            'insured .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    does_the_insured_have_a_local_authority_license_to_operate_where_applicable: str = Field(
        ...,
        description=(
            "Indicate whether a local authority license is held and provide details if "
            'applicable .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class BusinessActivitiesandRevenue(BaseModel):
    """Breakdown of business activities and percentage of revenue for each"""

    pet_trainer_answer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of trainers for Pet Trainer activities"
    )

    pet_trainer_percentage_of_revenue: str = Field(
        default="",
        description=(
            "Percentage of total revenue derived from Pet Trainer activities .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    pet_daycare_answer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of pets for Pet Daycare operations"
    )

    pet_daycare_percentage_of_revenue: str = Field(
        default="",
        description=(
            "Percentage of total revenue derived from Pet Daycare operations .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    pet_groomers_answer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of groomers employed"
    )

    pet_groomers_percentage_of_revenue: str = Field(
        default="",
        description=(
            "Percentage of total revenue derived from Pet Grooming .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    pet_therapies_ex_equine_vets_answer: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of therapists providing pet therapies (excluding equine and vets)",
    )

    pet_therapies_ex_equine_vets_percentage_of_revenue: str = Field(
        default="",
        description=(
            "Percentage of total revenue from pet therapy services (excluding equine and "
            'vets) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    dog_walkers_answer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of dog walkers engaged"
    )

    dog_walkers_percentage_of_revenue: str = Field(
        default="",
        description=(
            "Percentage of total revenue derived from dog walking .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    dog_kennels_answer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of dogs accommodated in kennels"
    )

    dog_kennels_percentage_of_revenue: str = Field(
        default="",
        description=(
            "Percentage of total revenue derived from dog kennel operations .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    catteries_answer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of cats accommodated in catteries"
    )

    catteries_percentage_of_revenue: str = Field(
        default="",
        description=(
            "Percentage of total revenue derived from cattery operations .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    dog_clubs_societies_answer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of members in dog clubs and societies"
    )

    dog_clubs_societies_percentage_of_revenue: str = Field(
        default="",
        description=(
            "Percentage of total revenue from dog clubs and societies .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    pet_transportation_answer: str = Field(
        default="",
        description=(
            "Description or count related to pet transportation business as per rating "
            'basis .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    pet_transportation_percentage_of_revenue: str = Field(
        default="",
        description=(
            "Percentage of total revenue derived from pet transportation .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    microchipping_answer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of trainers performing microchipping"
    )

    microchipping_percentage_of_revenue: str = Field(
        default="",
        description=(
            "Percentage of total revenue derived from microchipping services .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    manufacture_of_pet_accessories_answer: str = Field(
        default="",
        description=(
            "Turnover amount for manufacture of pet accessories .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    manufacture_of_pet_accessories_percentage_of_revenue: str = Field(
        default="",
        description=(
            "Percentage of total revenue from manufacture of pet accessories .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    greyhound_dog_assessment_answer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of assessors performing greyhound dog assessments"
    )

    greyhound_dog_assessment_percentage_of_revenue: str = Field(
        default="",
        description=(
            "Percentage of total revenue from greyhound dog assessments .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    pound_dog_assessment_answer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of assessors performing pound dog assessments"
    )

    pound_dog_assessment_percentage_of_revenue: str = Field(
        default="",
        description=(
            "Percentage of total revenue from pound dog assessments .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    security_dog_training_answer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of trainers involved in security dog training"
    )

    security_dog_training_percentage_of_revenue: str = Field(
        default="",
        description=(
            "Percentage of total revenue from security dog training .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    manufacture_of_dry_dog_food_treats_answer: str = Field(
        default="",
        description=(
            "Turnover amount for manufacture of dry dog food and treats .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    manufacture_of_dry_dog_food_treats_percentage_of_revenue: str = Field(
        default="",
        description=(
            "Percentage of total revenue from manufacture of dry dog food and treats .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    products_sales_up_to_50000_answer: str = Field(
        default="",
        description=(
            "Turnover amount for product sales up to $50,000 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    products_sales_up_to_50000_percentage_of_revenue: str = Field(
        default="",
        description=(
            "Percentage of total revenue from product sales up to $50,000 .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class EventCoverage(BaseModel):
    """Information about event coverage requirements"""

    event_coverage_required_yes: BooleanLike = Field(
        default="", description="Check if event coverage is required"
    )

    event_coverage_required_no: BooleanLike = Field(
        default="", description="Check if event coverage is not required"
    )

    number_of_events_hosted_per_year: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of events hosted annually"
    )

    number_of_attendees_per_event: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Average number of attendees at each event"
    )


class PetCareProfessionalApplication(BaseModel):
    """
    Pet Care Professional Application

    Pet Care Professional Application
    """

    broker_information: BrokerInformation = Field(..., description="Broker Information")
    insured_information: InsuredInformation = Field(..., description="Insured Information")
    underwriting_details: UnderwritingDetails = Field(..., description="Underwriting Details")
    business_activities_and_revenue: BusinessActivitiesandRevenue = Field(
        ..., description="Business Activities and Revenue"
    )
    event_coverage: EventCoverage = Field(..., description="Event Coverage")
