from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class LocationOfCombatZoneRow(BaseModel):
    """Single row in Location of Combat Zone"""

    location_of_combat_zone: str = Field(default="", description="Location_Of_Combat_Zone")
    details_and_time_period: str = Field(default="", description="Details_And_Time_Period")
    check_if_served: str = Field(default="", description="Check_If_Served")


class DetailsAndTimePeriodRow(BaseModel):
    """Single row in Details and Time Period"""

    location_of_combat_zone: str = Field(default="", description="Location_Of_Combat_Zone")
    details_and_time_period: str = Field(default="", description="Details_And_Time_Period")
    check_if_served: str = Field(default="", description="Check_If_Served")


class CheckIfServedRow(BaseModel):
    """Single row in Check if Served"""

    location_of_combat_zone: str = Field(default="", description="Location_Of_Combat_Zone")
    details_and_time_period: str = Field(default="", description="Details_And_Time_Period")
    check_if_served: str = Field(default="", description="Check_If_Served")


class Signatures(BaseModel):
    """Signatures and dates for informant and funeral director"""

    informant_signature: str = Field(
        ...,
        description=(
            "Signature of the informant completing the worksheet .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    informant_signature_date: str = Field(
        ..., description="Date the informant signed the worksheet"
    )  # YYYY-MM-DD format

    funeral_director_signature: str = Field(
        ...,
        description=(
            'Signature of the funeral director .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    funeral_director_signature_date: str = Field(
        ..., description="Date the funeral director signed the worksheet"
    )  # YYYY-MM-DD format


class VeteransStatusLocationofCombatZone(BaseModel):
    """Combat zone service details for the decedent’s U.S. Armed Forces service"""

    location_of_combat_zone: List[LocationOfCombatZoneRow] = Field(
        default="",
        description=(
            "Table listing combat zones where the decedent served, with details and "
            "indication if served"
        ),
    )  # List of table rows

    details_and_time_period: List[DetailsAndTimePeriodRow] = Field(
        default="",
        description=(
            "Table column describing campaign details and applicable time period for each "
            "combat zone"
        ),
    )  # List of table rows

    check_if_served: List[CheckIfServedRow] = Field(
        default="",
        description="Table column to indicate whether the decedent served in each listed combat zone",
    )  # List of table rows

    world_war_ii_or_name_country_below_if_desired_check_if_served: BooleanLike = Field(
        default="",
        description=(
            "Indicate if the decedent served in World War II or a specified country during "
            "that conflict"
        ),
    )

    asiatic_pacific_campaign_check_if_served: BooleanLike = Field(
        default="",
        description=(
            "Indicate if the decedent served in the Asiatic-Pacific Campaign during World War II"
        ),
    )

    american_campaign_check_if_served: BooleanLike = Field(
        default="",
        description="Indicate if the decedent served in the American Campaign during World War II",
    )

    american_merchant_marines_in_oceangoing_service_from_12_7_1941_to_8_15_1946_check_if_served: BooleanLike = Field(
        default="",
        description=(
            "Indicate if the decedent served in the American Merchant Marines in oceangoing "
            "service during the specified World War II period"
        ),
    )

    korea_check_if_served: BooleanLike = Field(
        default="",
        description=(
            "Indicate if the decedent served in the Korean conflict during the specified period"
        ),
    )

    vietnam_check_if_served: BooleanLike = Field(
        default="",
        description="Indicate if the decedent served in Vietnam during the specified period",
    )

    lebanon_check_if_served: BooleanLike = Field(
        default="",
        description="Indicate if the decedent served in Lebanon during the specified period",
    )

    grenada_check_if_served: BooleanLike = Field(
        default="",
        description="Indicate if the decedent served in Grenada during the specified period",
    )

    panama_check_if_served: BooleanLike = Field(
        default="",
        description="Indicate if the decedent served in Panama during the specified period",
    )

    persian_gulf_check_if_served: BooleanLike = Field(
        default="",
        description="Indicate if the decedent served in the Persian Gulf beginning 8/2/1990",
    )

    somalia_check_if_served: BooleanLike = Field(
        default="", description="Indicate if the decedent served in Somalia beginning 9/17/1992"
    )

    bosnia_check_if_served: BooleanLike = Field(
        default="",
        description="Indicate if the decedent served in Bosnia during the specified period",
    )

    yugoslavia_now_bosnia_herzegovina_croatia_check_if_served: BooleanLike = Field(
        default="",
        description=(
            "Indicate if the decedent served in Yugoslavia (now Bosnia-Herzegovina) or "
            "Croatia during the listed operations and period"
        ),
    )

    kosovo_check_if_served: BooleanLike = Field(
        default="", description="Indicate if the decedent served in Kosovo beginning 3/24/1999"
    )

    operations_joint_endeavor_joint_guard_or_joint_forge_either_in_its_waters_or_airspace_beginning_3_24_1999_ongoing_check_if_served: BooleanLike = Field(
        default="",
        description=(
            "Indicate if the decedent served in Operations Joint Endeavor, Joint Guard, or "
            "Joint Forge in the specified waters or airspace beginning 3/24/1999"
        ),
    )

    afghanistan_or_name_below_check_if_served: BooleanLike = Field(
        default="",
        description=(
            "Indicate if the decedent served in Afghanistan or another named location "
            "during Operation Enduring Freedom"
        ),
    )

    iraq_check_if_served: BooleanLike = Field(
        default="",
        description="Indicate if the decedent served in Iraq during Operation Iraqi Freedom",
    )

    operation_new_dawn_beginning_02_17_2010_ongoing_check_if_served: BooleanLike = Field(
        default="",
        description="Indicate if the decedent served in Operation New Dawn beginning 02/17/2010",
    )

    global_war_on_terrorism_name_below_check_if_served: BooleanLike = Field(
        default="",
        description=(
            "Indicate if the decedent served in the Global War on Terrorism in a named location"
        ),
    )

    name_any_other_locations_in_this_space: str = Field(
        default="",
        description=(
            "List any additional combat zones or locations where the decedent served that "
            'are not already listed .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    name_any_other_locations_in_this_space_check_if_served: BooleanLike = Field(
        default="",
        description=(
            "Indicate if the decedent served in any additional named locations listed in "
            "the space provided"
        ),
    )


class OregonDeathCertificateWorksheetForFuneralHomes(BaseModel):
    """
    OREGON DEATH CERTIFICATE WORKSHEET FOR FUNERAL HOMES

    The following is a list of combat zones as defined by the U.S. Department of Veterans Affairs. Please list any or all locations from the left column that the decedent served while in the U.S. Armed Forces. You are free to report any locations not named at the bottom of this form.
    """

    signatures: Signatures = Field(..., description="Signatures")
    veterans_status___location_of_combat_zone: VeteransStatusLocationofCombatZone = Field(
        ..., description="Veteran’s Status – Location of Combat Zone"
    )
