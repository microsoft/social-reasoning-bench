from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Detailsrelatingtoanyrisksofselfharmincludingselfneglectsuicide(BaseModel):
    """Specific recent history and details of self-harm, suicidal behaviour, and self-neglect"""

    thoughts_of_self_harm: BooleanLike = Field(
        default="", description="Tick if the person currently has thoughts of self-harm"
    )

    more_details_thoughts_of_self_harm: str = Field(
        default="",
        description=(
            "Provide more details about any current thoughts of self-harm .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    self_harmed_in_last_6_months: BooleanLike = Field(
        default="", description="Tick if the person has self-harmed in the last 6 months"
    )

    more_details_self_harmed_in_last_6_months: str = Field(
        default="",
        description=(
            "Provide more details about any self-harm in the last 6 months .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    self_harmed_in_last_12_months: BooleanLike = Field(
        default="", description="Tick if the person has self-harmed in the last 12 months"
    )

    more_details_self_harmed_in_last_12_months: str = Field(
        default="",
        description=(
            "Provide more details about any self-harm in the last 12 months .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    any_suicidal_behaviours_attempts: BooleanLike = Field(
        default="", description="Tick if there have been any suicidal behaviours or attempts"
    )

    more_details_any_suicidal_behaviours_attempts: str = Field(
        default="",
        description=(
            "Provide more details about any suicidal behaviours or attempts .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    any_self_neglect: BooleanLike = Field(
        default="", description="Tick if there are concerns about self-neglect"
    )

    more_details_any_self_neglect: str = Field(
        default="",
        description=(
            "Provide more details about any self-neglect .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AdditionalPotentialRisks(BaseModel):
    """Other risk factors and brief details"""

    alcohol_misuse: BooleanLike = Field(
        default="", description="Tick if there are concerns about alcohol misuse"
    )

    brief_details_alcohol_misuse: str = Field(
        default="",
        description=(
            "Provide brief details about alcohol misuse .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    drug_misuse: BooleanLike = Field(
        default="", description="Tick if there are concerns about drug misuse"
    )

    brief_details_drug_misuse: str = Field(
        default="",
        description=(
            "Provide brief details about drug misuse .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    self_harm_additional_potential_risks: BooleanLike = Field(
        default="", description="Tick if self-harm is an additional potential risk"
    )

    brief_details_self_harm_additional_potential_risks: str = Field(
        default="",
        description=(
            "Provide brief details about self-harm as an additional potential risk .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    suicidal_thoughts: BooleanLike = Field(
        default="", description="Tick if there are concerns about suicidal thoughts"
    )

    brief_details_suicidal_thoughts: str = Field(
        default="",
        description=(
            "Provide brief details about suicidal thoughts .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    suicide_attempts: BooleanLike = Field(
        default="", description="Tick if there have been any suicide attempts"
    )

    brief_details_suicide_attempts: str = Field(
        default="",
        description=(
            "Provide brief details about any suicide attempts .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mental_health: BooleanLike = Field(
        default="", description="Tick if there are mental health concerns as a risk factor"
    )

    brief_details_mental_health: str = Field(
        default="",
        description=(
            "Provide brief details about mental health concerns .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    aggression_violence: BooleanLike = Field(
        default="", description="Tick if there are concerns about aggression or violence"
    )

    brief_details_aggression_violence: str = Field(
        default="",
        description=(
            "Provide brief details about aggression or violence .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    anti_social_behaviour: BooleanLike = Field(
        default="", description="Tick if there are concerns about anti-social behaviour"
    )

    brief_details_anti_social_behaviour: str = Field(
        default="",
        description=(
            "Provide brief details about anti-social behaviour .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    harassment_of_others: BooleanLike = Field(
        default="", description="Tick if there are concerns about harassment of others"
    )

    brief_details_harassment_of_others: str = Field(
        default="",
        description=(
            "Provide brief details about harassment of others .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    gambling_issues: BooleanLike = Field(
        default="", description="Tick if there are concerns about gambling issues"
    )

    brief_details_gambling_issues: str = Field(
        default="",
        description=(
            "Provide brief details about gambling issues .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    sexual_offender: BooleanLike = Field(
        default="", description="Tick if the person is a known or suspected sexual offender"
    )

    brief_details_sexual_offender: str = Field(
        default="",
        description=(
            "Provide brief details regarding sexual offending status or concerns .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    victim_of_sexual_assault: BooleanLike = Field(
        default="", description="Tick if the person is a victim of sexual assault"
    )

    brief_details_victim_of_sexual_assault: str = Field(
        default="",
        description=(
            "Provide brief details about experiences of sexual assault .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    victim_of_sexual_offending: BooleanLike = Field(
        default="", description="Tick if the person is a victim of sexual offending"
    )

    brief_details_victim_of_sexual_offending: str = Field(
        default="",
        description=(
            "Provide brief details about experiences of sexual offending .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    adverse_childhood_experiences: BooleanLike = Field(
        default="", description="Tick if there is a history of adverse childhood experiences"
    )

    brief_details_adverse_childhood_experiences: str = Field(
        default="",
        description=(
            "Provide brief details about adverse childhood experiences .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SupportNeeds(BaseModel):
    """Support needs, health conditions, medications, and disability information"""

    brief_description_and_details_of_mental_health_support_needs: str = Field(
        default="",
        description=(
            "Describe the person’s mental health support needs .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    description_of_any_other_diagnosed_health_conditions: str = Field(
        default="",
        description=(
            "Describe any other diagnosed physical or mental health conditions .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    details_of_all_prescription_medications_being_taken: str = Field(
        default="",
        description=(
            "List all current prescription medications and dosages if known .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    do_you_consider_yourself_to_be_disabled_if_so_please_give_brief_details_below: str = Field(
        default="",
        description=(
            "State whether you consider yourself disabled and provide brief details .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class JourneymenCicReferralForm(BaseModel):
    """
    JourneyMEN CIC – Referral Form

    ''
    """

    details_relating_to_any_risks_of_self_harm_including_self_neglect__suicide: Detailsrelatingtoanyrisksofselfharmincludingselfneglectsuicide = Field(
        ...,
        description="Details relating to any risks of self-harm, including self-neglect & suicide",
    )
    additional_potential_risks: AdditionalPotentialRisks = Field(
        ..., description="Additional Potential Risks"
    )
    support_needs: SupportNeeds = Field(..., description="Support Needs")
