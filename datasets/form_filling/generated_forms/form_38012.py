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


class ApplicantContactInformation(BaseModel):
    """Applicant identity and primary contact details"""

    applicant: str = Field(
        ...,
        description=(
            'Name of the primary applicant/insured .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    business_name: str = Field(
        default="",
        description=(
            "Legal or trade name of the business, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            "Mailing address for all correspondence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_person: str = Field(
        ...,
        description=(
            "Primary contact person for this policy .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City for the mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    county: str = Field(
        ...,
        description=(
            'County for the mailing address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="Two-letter state abbreviation for the mailing address")

    zip: str = Field(..., description="ZIP or postal code for the mailing address")

    phone: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    website: str = Field(
        default="",
        description=(
            'Business or personal website URL .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Primary email address for correspondence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class LocationInformation(BaseModel):
    """Farm/ranch locations and acreage"""

    location_address_1: str = Field(
        ...,
        description=(
            'First insured location address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    county_location_address_1: str = Field(
        ...,
        description=(
            'County for Location Address #1 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    acres_location_address_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total acreage at Location Address #1"
    )

    location_address_2: str = Field(
        default="",
        description=(
            "Second insured location address, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    county_location_address_2: str = Field(
        default="",
        description=(
            'County for Location Address #2 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    acres_location_address_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total acreage at Location Address #2"
    )

    does_insured_own: BooleanLike = Field(
        ..., description="Indicate if the insured owns the property"
    )

    does_insured_lease: BooleanLike = Field(
        ..., description="Indicate if the insured leases the property"
    )


class CoverageClaimsHistory(BaseModel):
    """Current/past insurance, premiums, and loss history"""

    pay_plan_desired_yes: BooleanLike = Field(
        default="", description="Check if a payment plan is desired (Yes)"
    )

    pay_plan_desired_no: BooleanLike = Field(
        default="", description="Check if a payment plan is not desired (No)"
    )

    past_and_or_current_insurance_company: str = Field(
        default="",
        description=(
            "Name of the past and/or current insurance company .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    annual_premium: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Annual premium amount with the past or current insurer"
    )

    claims_past_5_years_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate Yes if there have been any claims or reported incidents in the past 5 years"
        ),
    )

    claims_past_5_years_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate No if there have been no claims or reported incidents in the past 5 years"
        ),
    )

    explain_claims_incidents: str = Field(
        default="",
        description=(
            "If Yes, provide details of all claims or incidents including dates, cause of "
            'loss, and amounts paid .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    coverage_cancelled_refused_yes: BooleanLike = Field(
        ...,
        description="Indicate Yes if coverage has been cancelled or refused in the past 5 years",
    )

    coverage_cancelled_refused_no: BooleanLike = Field(
        ...,
        description="Indicate No if coverage has not been cancelled or refused in the past 5 years",
    )

    explain_coverage_cancelled_refused: str = Field(
        default="",
        description=(
            "If Yes, explain the circumstances of coverage being cancelled or refused .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Lienholders(BaseModel):
    """Mortgagee and loss payee information"""

    mortgagee_name_and_address: str = Field(
        default="",
        description=(
            "Full name and mailing address of the mortgagee .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    loss_payee_name_and_address: str = Field(
        default="",
        description=(
            "Full name and mailing address of the loss payee .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class BusinessUseofPremises(BaseModel):
    """Non-farm and other business activities on the property"""

    personal_non_farm_business_yes: BooleanLike = Field(
        ..., description="Indicate Yes if you have any personal non-farm business pursuits"
    )

    personal_non_farm_business_no: BooleanLike = Field(
        ..., description="Indicate No if you do not have any personal non-farm business pursuits"
    )

    other_farming_or_business_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate Yes if there are any non-equine farming pursuits or other businesses "
            "on the property"
        ),
    )

    other_farming_or_business_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate No if there are no non-equine farming pursuits or other businesses on "
            "the property"
        ),
    )

    describe_activities_and_revenues: str = Field(
        default="",
        description=(
            "If Yes, describe the activities and provide associated annual revenues .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class LeasedPortionsofProperty(BaseModel):
    """Information about leased portions of the farm/ranch and lessee insurance"""

    leased_portions_yes: BooleanLike = Field(
        ..., description="Indicate Yes if any portion of the farm/ranch is leased to others"
    )

    leased_portions_no: BooleanLike = Field(
        ..., description="Indicate No if no portion of the farm/ranch is leased to others"
    )

    describe_leased_portions: str = Field(
        default="",
        description=(
            "If Yes, describe the leased portions and their use .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    lessee_has_own_insurance_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the lessee has their own insurance coverage"
    )

    lessee_has_own_insurance_no: BooleanLike = Field(
        default="",
        description="Indicate No if the lessee does not have their own insurance coverage",
    )


class FarmPropertyApplication(BaseModel):
    """
    Farm Property Application

    ''
    """

    broker__policy_information: BrokerPolicyInformation = Field(
        ..., description="Broker & Policy Information"
    )
    applicant__contact_information: ApplicantContactInformation = Field(
        ..., description="Applicant & Contact Information"
    )
    location_information: LocationInformation = Field(..., description="Location Information")
    coverage__claims_history: CoverageClaimsHistory = Field(
        ..., description="Coverage & Claims History"
    )
    lienholders: Lienholders = Field(..., description="Lienholders")
    business__use_of_premises: BusinessUseofPremises = Field(
        ..., description="Business & Use of Premises"
    )
    leased_portions_of_property: LeasedPortionsofProperty = Field(
        ..., description="Leased Portions of Property"
    )
