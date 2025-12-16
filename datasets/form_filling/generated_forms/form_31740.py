from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PolicyRecommendations(BaseModel):
    """Types of insurance coverage the applicant is interested in"""

    general_liability: BooleanLike = Field(
        default="", description="Check if you are interested in General Liability coverage."
    )

    accident_medical: BooleanLike = Field(
        default="", description="Check if you are interested in Accident Medical coverage."
    )

    earthquake: BooleanLike = Field(
        default="", description="Check if you are interested in Earthquake coverage."
    )

    inland_marine: BooleanLike = Field(
        default="", description="Check if you are interested in Inland Marine coverage."
    )

    workers_compensation: BooleanLike = Field(
        default="", description="Check if you are interested in Workers Compensation coverage."
    )

    commercial_auto: BooleanLike = Field(
        default="", description="Check if you are interested in Commercial Auto coverage."
    )

    epli: BooleanLike = Field(
        default="",
        description=(
            "Check if you are interested in Employment Practices Liability Insurance (EPLI) "
            "coverage."
        ),
    )

    flood: BooleanLike = Field(
        default="", description="Check if you are interested in Flood coverage."
    )

    hired_non_owned_auto: BooleanLike = Field(
        default="", description="Check if you are interested in Hired & Non-Owned Auto coverage."
    )

    umbrella: BooleanLike = Field(
        default="", description="Check if you are interested in Umbrella coverage."
    )

    abuse_molestation: BooleanLike = Field(
        default="", description="Check if you are interested in Abuse / Molestation coverage."
    )

    cyber_liability: BooleanLike = Field(
        default="", description="Check if you are interested in Cyber Liability coverage."
    )


class Section1BusinessInformation(BaseModel):
    """General and contact information about the business"""

    how_did_you_hear_about_us: str = Field(
        default="",
        description=(
            "Describe how you learned about this insurance agency. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    type_of_business_individual: BooleanLike = Field(
        ..., description="Check if the business type is Individual."
    )

    type_of_business_partnership: BooleanLike = Field(
        ..., description="Check if the business type is Partnership."
    )

    type_of_business_corporation: BooleanLike = Field(
        ..., description="Check if the business type is Corporation."
    )

    type_of_business_llc: BooleanLike = Field(..., description="Check if the business type is LLC.")

    business_name: str = Field(
        ...,
        description=(
            'Legal name of the business. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    dba_if_applicable: str = Field(
        default="",
        description=(
            "Doing Business As name, if different from legal business name. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    contact_name: str = Field(
        ...,
        description=(
            'Primary contact person\'s full name. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            'Primary contact email address. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    business_phone: str = Field(
        ...,
        description=(
            'Main business telephone number. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            'Business fax number. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    cell: str = Field(
        default="",
        description=(
            "Primary contact's mobile phone number. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    birth_date: str = Field(
        default="", description="Birth date of the primary contact or owner."
    )  # YYYY-MM-DD format

    proposed_effective_date: str = Field(
        ..., description="Requested effective date for the insurance coverage."
    )  # YYYY-MM-DD format

    mailing_address: str = Field(
        ...,
        description=(
            "Street mailing address for the business. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_city: str = Field(
        ...,
        description=(
            'City for the mailing address. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_state: str = Field(..., description="State for the mailing address.")

    mailing_address_zip: str = Field(..., description="ZIP code for the mailing address.")

    location_address_if_different: str = Field(
        default="",
        description=(
            "Physical location address of the business if different from mailing address. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    location_address_city: str = Field(
        default="",
        description=(
            "City for the physical location address. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    location_address_state: str = Field(
        default="", description="State for the physical location address."
    )

    location_address_zip: str = Field(
        default="", description="ZIP code for the physical location address."
    )

    year_business_started: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year the business began operations."
    )

    fein_ss: str = Field(
        ..., description="Federal Employer Identification Number or Social Security Number."
    )

    detailed_description_of_operations: str = Field(
        ...,
        description=(
            "Provide a detailed description of the business operations and activities. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Section2InsuranceandPropertyInformation(BaseModel):
    """Current insurance details, claims history, and property information"""

    current_insurance_carrier: str = Field(
        default="",
        description=(
            "Name of your current insurance carrier, if any. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    policy_number: str = Field(
        default="",
        description=(
            "Policy number of your current insurance policy. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    premium: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current policy premium amount."
    )

    expiration_date: str = Field(
        default="", description="Expiration date of your current insurance policy."
    )  # YYYY-MM-DD format

    any_incidents_or_claims_last_5_years_yes: BooleanLike = Field(
        default="",
        description="Select if there have been any incidents or claims in the last 5 years.",
    )

    any_incidents_or_claims_last_5_years_no: BooleanLike = Field(
        default="",
        description="Select if there have been no incidents or claims in the last 5 years.",
    )

    incidents_or_claims_last_5_years_explanation: str = Field(
        default="",
        description=(
            "If there were incidents or claims, provide details including dates and "
            'descriptions. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    any_policy_declined_cancelled_non_renewed_past_3_years_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if any policy has been declined, cancelled, or non-renewed in the past 3 years."
        ),
    )

    any_policy_declined_cancelled_non_renewed_past_3_years_no: BooleanLike = Field(
        default="",
        description=(
            "Select if no policy has been declined, cancelled, or non-renewed in the past 3 years."
        ),
    )

    are_you_within_city_limits_yes: BooleanLike = Field(
        default="", description="Select if the business location is within city limits."
    )

    are_you_within_city_limits_no: BooleanLike = Field(
        default="", description="Select if the business location is not within city limits."
    )

    do_you_own_or_lease_your_property_own: BooleanLike = Field(
        default="", description="Select if you own the property where the business operates."
    )

    do_you_own_or_lease_your_property_lease: BooleanLike = Field(
        default="", description="Select if you lease the property where the business operates."
    )

    name_of_lessor_landlord: str = Field(
        default="",
        description=(
            "Name of the property owner or landlord, if the property is leased. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    address_lessor_landlord: str = Field(
        default="",
        description=(
            "Mailing address of the lessor or landlord. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class TheCiaAirsoftApplication(BaseModel):
    """
        THE CIA
    AIRSOFT APPLICATION

        DIRECTIONS:
        1. Complete the enrollment form (all pages) in full by filling in the blue fields.
        2. Please fill in all the fields with the correct information.
        3. Email the application to apps@cossioinsurance.com or fax to 864-603-2348
    """

    policy_recommendations: PolicyRecommendations = Field(..., description="Policy Recommendations")
    section_1_business_information: Section1BusinessInformation = Field(
        ..., description="Section 1: Business Information"
    )
    section_2_insurance_and_property_information: Section2InsuranceandPropertyInformation = Field(
        ..., description="Section 2: Insurance and Property Information"
    )
