from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AboutYouTheClient(BaseModel):
    """Information about the client's background, strengths, and circumstances"""

    have_you_ever_served_for_a_day_or_more_in_the_armed_forces_or_reserves_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if the client has served for a day or more in the Armed Forces or Reserves."
        ),
    )

    have_you_ever_served_for_a_day_or_more_in_the_armed_forces_or_reserves_no: BooleanLike = Field(
        default="",
        description=(
            "Select if the client has not served for a day or more in the Armed Forces or Reserves."
        ),
    )

    what_are_your_strengths_skills_talents_aspirations_or_goals: str = Field(
        default="",
        description=(
            "Describe the client’s strengths, including skills, talents, aspirations, or "
            'goals. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    what_are_your_interests_hobbies: str = Field(
        default="",
        description=(
            "List the client’s interests and hobbies. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    are_you_a_carer_or_have_carers_responsibilities: str = Field(
        default="",
        description=(
            "Explain if the client is a carer or has caring responsibilities and provide "
            'brief details. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    how_did_you_hear_about_journeymen: str = Field(
        default="",
        description=(
            "Indicate how the client found out about JourneyMEN (e.g. friend, GP, online). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class ClientDemographicMonitoringInformation(BaseModel):
    """Demographic information used to align service delivery to client needs"""

    gender_male: BooleanLike = Field(default="", description="Tick if the client’s gender is male.")

    gender_non_binary: BooleanLike = Field(
        default="", description="Tick if the client’s gender is non-binary."
    )

    gender_transgender: BooleanLike = Field(
        default="", description="Tick if the client identifies as transgender."
    )

    gender_other: BooleanLike = Field(
        default="",
        description="Tick if the client’s gender is not listed and is described as other.",
    )

    gender_prefer_not_to_say: BooleanLike = Field(
        default="", description="Tick if the client prefers not to disclose their gender."
    )

    marital_relationship_single: BooleanLike = Field(
        default="", description="Tick if the client is single."
    )

    marital_relationship_married: BooleanLike = Field(
        default="", description="Tick if the client is married."
    )

    marital_relationship_divorced: BooleanLike = Field(
        default="", description="Tick if the client is divorced."
    )

    marital_relationship_widowed: BooleanLike = Field(
        default="", description="Tick if the client is widowed."
    )

    marital_relationship_living_with_partner: BooleanLike = Field(
        default="", description="Tick if the client is living with a partner."
    )

    marital_relationship_in_a_relationship: BooleanLike = Field(
        default="",
        description="Tick if the client is in a relationship but not covered by other options.",
    )

    marital_relationship_prefer_not_to_say: BooleanLike = Field(
        default="",
        description="Tick if the client prefers not to disclose their marital/relationship status.",
    )

    sexual_orientation_heterosexual_straight: BooleanLike = Field(
        default="", description="Tick if the client’s sexual orientation is heterosexual/straight."
    )

    sexual_orientation_homosexual_gay: BooleanLike = Field(
        default="", description="Tick if the client’s sexual orientation is homosexual/gay."
    )

    sexual_orientation_bisexual: BooleanLike = Field(
        default="", description="Tick if the client’s sexual orientation is bisexual."
    )

    sexual_orientation_asexual: BooleanLike = Field(
        default="", description="Tick if the client’s sexual orientation is asexual."
    )

    sexual_orientation_prefer_not_to_say: BooleanLike = Field(
        default="",
        description="Tick if the client prefers not to disclose their sexual orientation.",
    )

    religion_belief_christianity: BooleanLike = Field(
        default="", description="Tick if the client’s religion or belief is Christianity."
    )

    religion_belief_muslim: BooleanLike = Field(
        default="", description="Tick if the client’s religion or belief is Muslim/Islam."
    )

    religion_belief_buddhist: BooleanLike = Field(
        default="", description="Tick if the client’s religion or belief is Buddhist."
    )

    religion_belief_hindu: BooleanLike = Field(
        default="", description="Tick if the client’s religion or belief is Hindu."
    )

    religion_belief_jewish: BooleanLike = Field(
        default="", description="Tick if the client’s religion or belief is Jewish."
    )

    religion_belief_no_religion_affiliation_or_belief: BooleanLike = Field(
        default="", description="Tick if the client has no religion, affiliation, or belief."
    )

    religion_belief_atheist: BooleanLike = Field(
        default="", description="Tick if the client identifies as atheist."
    )

    religion_belief_prefer_not_to_say: BooleanLike = Field(
        default="",
        description="Tick if the client prefers not to disclose their religion or belief.",
    )

    ethnicity_asian_or_asian_british: BooleanLike = Field(
        default="", description="Tick if the client’s ethnicity is Asian or Asian British."
    )

    ethnicity_asian_or_asian_british_further_details: str = Field(
        default="",
        description=(
            "Provide further details of the client’s Asian or Asian British ethnicity. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    ethnicity_mixed_or_multiple_ethnic_groups: BooleanLike = Field(
        default="",
        description="Tick if the client’s ethnicity is mixed or from multiple ethnic groups.",
    )

    ethnicity_mixed_or_multiple_ethnic_groups_further_details: str = Field(
        default="",
        description=(
            "Provide further details of the client’s mixed or multiple ethnic groups. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    ethnicity_black_african_caribbean_or_black_british: BooleanLike = Field(
        default="",
        description="Tick if the client’s ethnicity is Black, African, Caribbean, or Black British.",
    )

    ethnicity_black_african_caribbean_or_black_british_further_details: str = Field(
        default="",
        description=(
            "Provide further details of the client’s Black, African, Caribbean, or Black "
            'British ethnicity. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    ethnicity_white_british_or_white_other: BooleanLike = Field(
        default="",
        description="Tick if the client’s ethnicity is White British or any other White background.",
    )

    ethnicity_white_british_or_white_other_further_details: str = Field(
        default="",
        description=(
            "Provide further details of the client’s White British or White other "
            'ethnicity. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    ethnicity_any_other_ethnic_group: BooleanLike = Field(
        default="",
        description=(
            "Tick if the client’s ethnicity is not listed and falls under any other ethnic group."
        ),
    )

    ethnicity_any_other_ethnic_group_further_details: str = Field(
        default="",
        description=(
            "Provide further details of the client’s ethnicity if it is not covered by the "
            'listed groups. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class JourneymenCicReferralForm(BaseModel):
    """
    JourneyMEN CIC – Referral Form

    We gather this information to ensure we can align the delivery of our service to your needs.
    """

    about_you_the_client: AboutYouTheClient = Field(..., description="About You (The Client)")
    client_demographic_monitoring_information: ClientDemographicMonitoringInformation = Field(
        ..., description="Client Demographic Monitoring Information"
    )
