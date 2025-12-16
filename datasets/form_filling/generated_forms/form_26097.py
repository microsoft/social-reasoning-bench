from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ClaimantMailingAddress(BaseModel):
    """Claimant name and primary mailing address as shown at the top of the form"""

    claimant_name_and_mailing_address: str = Field(
        ...,
        description=(
            "Claimant’s full name and complete mailing address, with any necessary "
            "corrections to the printed information. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AssessorsUseOnly(BaseModel):
    """For assessor office processing and decision"""

    date_received: str = Field(
        default="",
        description="Date the assessor’s office received this claim (assessor use only).",
    )  # YYYY-MM-DD format

    approved: BooleanLike = Field(
        default="", description="Indicates whether the claim is approved (assessor use only)."
    )

    denied: BooleanLike = Field(
        default="", description="Indicates whether the claim is denied (assessor use only)."
    )

    reason_for_denial: str = Field(
        default="",
        description=(
            "Explanation by the assessor’s office if the claim is denied. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ClaimantandSpouseInformation(BaseModel):
    """Identifying information for the claimant and spouse"""

    claimant_s_name: str = Field(
        ...,
        description=(
            'Full legal name of the claimant. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    social_security_number_claimant: str = Field(
        ..., description="Claimant’s Social Security Number."
    )

    spouse_s_name: str = Field(
        default="",
        description=(
            "Full legal name of the claimant’s spouse, if applicable. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    social_security_number_spouse: str = Field(
        default="", description="Spouse’s Social Security Number, if applicable."
    )


class PropertyAddress(BaseModel):
    """Location of the dwelling for which the exemption is claimed"""

    street_address_of_dwelling_if_different_from_mailing_address: str = Field(
        ...,
        description=(
            "Street address of the dwelling that is the subject of this exemption, if "
            'different from the mailing address. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City where the dwelling is located. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zip_code: str = Field(..., description="ZIP Code for the dwelling’s location.")

    assessors_parcel_number: str = Field(
        ...,
        description=(
            "Assessor’s Parcel Number (APN) for the property being claimed. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class UnmarriedSurvivingSpouseVeteranInformation(BaseModel):
    """Veteran details when the claimant is an unmarried surviving spouse"""

    name_of_the_veteran_as_shown_on_the_discharge_documents: str = Field(
        default="",
        description=(
            "Full name of the veteran exactly as it appears on the discharge documents (for "
            "unmarried surviving spouse claimants). .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    social_security_number_veteran: str = Field(
        default="",
        description="Veteran’s Social Security Number (for unmarried surviving spouse claimants).",
    )


class ClaimForDisabledVeteransPropertyTaxExemption2021(BaseModel):
    """
    2021 CLAIM FOR DISABLED VETERANS' PROPERTY TAX EXEMPTION

    Article XIII of the California Constitution, section 4(a), and Revenue and Taxation Code section 205.5 provide an exemption for property which constitutes the home of a veteran, or the home of the unmarried surviving spouse of a veteran, who, because of injury or disease incurred in military service, is blind in both eyes, has lost the use of two or more limbs, or is totally disabled. There are two exemption levels - a basic exemption and one for low-income household claimants, both of which are adjusted annually for inflation*. The exemption does not apply to direct levies or special taxes. Once granted, the Basic Exemption remains in effect without annual filing until terminated. Annual filing is required for any year in which a Low-Income Exemption is claimed. Please refer to the attached schedule for the current amount and household income limits.
    Totally disabled means that the United States Veterans Administration or the military service from which discharged has rated the disability at 100 percent or has rated the disability compensation at 100 percent by reason of being unable to secure or follow a substantially gainful occupation.
    The Disabled Veterans’ Property Tax Exemption is also available to the unmarried surviving spouse of a veteran who, as a result of service-connected injury or disease: 1) died either while on active duty in the military service or after being discharged in other than dishonorable conditions and 2) served either in time of war or in time of peace in a campaign or expedition for which a medal has been issued by Congress. This law provides that the Veterans Administration shall determine whether an injury or disease is service-connected.
    The Disabled Veterans’ Property Tax Exemption provides for the cancellation or refund of taxes paid 1) when property becomes eligible after the lien date (new acquisition or occupancy of a previously owned property) or 2) upon a veteran’s disability rating or death. This further provides for the termination of the exemption on the date of sale or transfer of property to a third party who is not eligible for the exemption or on the date a person previously eligible for the exemption becomes ineligible.
    * As provided by Revenue and Taxation Code section 205.5, the exemption amount and the household income limit shall be compounded annually by an inflation factor tied to the California Consumer Price Index.
    """

    claimant_mailing_address: ClaimantMailingAddress = Field(
        ..., description="Claimant Mailing Address"
    )
    assessors_use_only: AssessorsUseOnly = Field(..., description="Assessor's Use Only")
    claimant_and_spouse_information: ClaimantandSpouseInformation = Field(
        ..., description="Claimant and Spouse Information"
    )
    property_address: PropertyAddress = Field(..., description="Property Address")
    unmarried_surviving_spouse__veteran_information: UnmarriedSurvivingSpouseVeteranInformation = (
        Field(..., description="Unmarried Surviving Spouse / Veteran Information")
    )
