from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


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
    """Combat zone locations where the decedent served, with details and service indication"""

    location_of_combat_zone_world_war_ii_or_name_country_below_if_desired_details_and_time_period: str = Field(
        default="",
        description=(
            "Details and time period of World War II service, including specific campaigns "
            'or named country if desired .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    location_of_combat_zone_world_war_ii_or_name_country_below_if_desired_check_if_served: BooleanLike = Field(
        default="", description="Indicate whether the decedent served in a World War II combat zone"
    )

    location_of_combat_zone_korea_details_and_time_period: str = Field(
        default="",
        description=(
            "Details and time period of Korea service .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    location_of_combat_zone_korea_check_if_served: BooleanLike = Field(
        default="", description="Indicate whether the decedent served in the Korea combat zone"
    )

    location_of_combat_zone_vietnam_details_and_time_period: str = Field(
        default="",
        description=(
            "Details and time period of Vietnam service .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    location_of_combat_zone_vietnam_check_if_served: BooleanLike = Field(
        default="", description="Indicate whether the decedent served in the Vietnam combat zone"
    )

    location_of_combat_zone_lebanon_details_and_time_period: str = Field(
        default="",
        description=(
            "Details and time period of Lebanon service .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    location_of_combat_zone_lebanon_check_if_served: BooleanLike = Field(
        default="", description="Indicate whether the decedent served in the Lebanon combat zone"
    )

    location_of_combat_zone_grenada_details_and_time_period: str = Field(
        default="",
        description=(
            "Details and time period of Grenada service .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    location_of_combat_zone_grenada_check_if_served: BooleanLike = Field(
        default="", description="Indicate whether the decedent served in the Grenada combat zone"
    )

    location_of_combat_zone_panama_details_and_time_period: str = Field(
        default="",
        description=(
            "Details and time period of Panama service .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    location_of_combat_zone_panama_check_if_served: BooleanLike = Field(
        default="", description="Indicate whether the decedent served in the Panama combat zone"
    )

    location_of_combat_zone_persian_gulf_details_and_time_period: str = Field(
        default="",
        description=(
            "Details and time period of Persian Gulf service .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    location_of_combat_zone_persian_gulf_check_if_served: BooleanLike = Field(
        default="",
        description="Indicate whether the decedent served in the Persian Gulf combat zone",
    )

    location_of_combat_zone_somalia_details_and_time_period: str = Field(
        default="",
        description=(
            "Details and time period of Somalia service .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    location_of_combat_zone_somalia_check_if_served: BooleanLike = Field(
        default="", description="Indicate whether the decedent served in the Somalia combat zone"
    )

    location_of_combat_zone_bosnia_details_and_time_period: str = Field(
        default="",
        description=(
            "Details and time period of Bosnia service .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    location_of_combat_zone_bosnia_check_if_served: BooleanLike = Field(
        default="", description="Indicate whether the decedent served in the Bosnia combat zone"
    )

    location_of_combat_zone_yugoslavia_now_bosnia_herzegovina_croatia_details_and_time_period: str = Field(
        default="",
        description=(
            "Details and time period of Yugoslavia service, including operations and areas "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    location_of_combat_zone_yugoslavia_now_bosnia_herzegovina_croatia_check_if_served: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the decedent served in the Yugoslavia (Bosnia-Herzegovina & "
            "Croatia) combat zone"
        ),
    )

    location_of_combat_zone_kosovo_details_and_time_period: str = Field(
        default="",
        description=(
            "Details and time period of Kosovo service, including operations and areas .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    location_of_combat_zone_kosovo_check_if_served: BooleanLike = Field(
        default="", description="Indicate whether the decedent served in the Kosovo combat zone"
    )

    location_of_combat_zone_afghanistan_or_name_below_details_and_time_period: str = Field(
        default="",
        description=(
            "Details and time period of Afghanistan service, including Operation Enduring "
            'Freedom locations .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    location_of_combat_zone_afghanistan_or_name_below_check_if_served: BooleanLike = Field(
        default="",
        description="Indicate whether the decedent served in the Afghanistan combat zone",
    )

    location_of_combat_zone_iraq_details_and_time_period: str = Field(
        default="",
        description=(
            "Details and time period of Iraq service, including specific operations .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    location_of_combat_zone_iraq_check_if_served: BooleanLike = Field(
        default="", description="Indicate whether the decedent served in the Iraq combat zone"
    )

    location_of_combat_zone_global_war_on_terrorism_name_below_details_and_time_period: str = Field(
        default="",
        description=(
            "Details and time period of Global War on Terrorism service, including specific "
            'expeditions or locations .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    location_of_combat_zone_global_war_on_terrorism_name_below_check_if_served: BooleanLike = Field(
        default="",
        description="Indicate whether the decedent served in a Global War on Terrorism combat zone",
    )

    name_any_other_locations_in_this_space: str = Field(
        default="",
        description=(
            "List any additional combat zone locations not covered above, with details and "
            'time periods if known .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
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
