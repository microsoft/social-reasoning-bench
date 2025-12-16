from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PartACityProfile(BaseModel):
    """City profile information including quality of life, administration, vision, and self-assessment"""

    part_a_city_profile_1_quality_of_life: str = Field(
        ...,
        description=(
            "Describe the city's current quality of life, including key indicators and "
            'conditions. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    part_a_city_profile_2_administrative_efficiency: str = Field(
        ...,
        description=(
            "Explain the city's administrative efficiency, governance structures, and "
            'processes. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    part_a_city_profile_3_swot: str = Field(
        ...,
        description=(
            "Provide a SWOT analysis (Strengths, Weaknesses, Opportunities, Threats) for "
            'the city. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    part_a_city_profile_4_strategic_focus_and_blueprint: str = Field(
        ...,
        description=(
            "Outline the strategic focus areas and overall blueprint for the city's "
            'development. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    part_a_city_profile_5_city_vision_and_goals: str = Field(
        ...,
        description=(
            "State the long-term vision and specific goals for the city. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    part_a_city_profile_6_citizen_engagement: str = Field(
        ...,
        description=(
            "Describe the processes and outcomes of citizen engagement in the Smart City "
            'proposal. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    part_a_city_profile_7_self_assessment_baseline: str = Field(
        ...,
        description=(
            "Provide the baseline self-assessment of the city's current status against "
            'Smart City criteria. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    part_a_city_profile_8_self_assessment_aspirations_imperatives: str = Field(
        ...,
        description=(
            "Detail the city's aspirations and key imperatives identified through "
            'self-assessment. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class PartBAreaBasedProposal(BaseModel):
    """Details of the area based proposal including approach, components, convergence, risks, and impact"""

    part_b_area_based_proposal_9_summary: str = Field(
        ...,
        description=(
            "Summarize the area-based proposal, including scope and key elements. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    part_b_area_based_proposal_10_approach_methodology: str = Field(
        ...,
        description=(
            "Explain the approach and methodology adopted for the area-based proposal. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    part_b_area_based_proposal_11_key_components: str = Field(
        ...,
        description=(
            "List and describe the key components of the area-based proposal. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    part_b_area_based_proposal_12_smart_urban_form: str = Field(
        ...,
        description=(
            "Describe the proposed smart urban form, including spatial planning and design "
            'aspects. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    part_b_area_based_proposal_13_convergence_agenda: str = Field(
        ...,
        description=(
            "Detail the convergence agenda, including alignment with other schemes and "
            'programs. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    part_b_area_based_proposal_14_convergence_implementation: str = Field(
        ...,
        description=(
            "Explain how convergence will be implemented operationally and institutionally. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    part_b_area_based_proposal_15_risks: str = Field(
        ...,
        description=(
            "Identify key risks associated with the area-based proposal and possible "
            'mitigation measures. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    part_b_area_based_proposal_16_essential_features_achievement_plan: str = Field(
        ...,
        description=(
            "Provide the plan for achieving essential Smart City features in the area-based "
            'proposal. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    part_b_area_based_proposal_17_success_factors: str = Field(
        ...,
        description=(
            "Describe the critical success factors for the area-based proposal. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    part_b_area_based_proposal_18_measurable_impact: str = Field(
        ...,
        description=(
            "Specify the expected measurable impacts and indicators for the area-based "
            'proposal. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class PartCPanCityProposals(BaseModel):
    """Pan-city proposal details including summary, components, and methodology"""

    part_c_pan_city_proposals_19_summary: str = Field(
        ...,
        description=(
            "Summarize the pan-city proposal(s), including objectives and scope. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    part_c_pan_city_proposals_20_components: str = Field(
        ...,
        description=(
            "List and describe the components of the pan-city proposal(s). .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    part_c_pan_city_proposals_21_approach_methodology: str = Field(
        ...,
        description=(
            "Explain the approach and methodology for the pan-city proposal(s). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class IndiaSmartCityMissionChecklist(BaseModel):
    """
        INDIA SMART CITY MISSION

    CHECKLIST

        All fields in the SCP format document have to be filled. The chart below will assist you in verifying that all questions have been answered and all fields have been filled.
    """

    part_a_city_profile: PartACityProfile = Field(..., description="Part A: City Profile")
    part_b_area_based_proposal: PartBAreaBasedProposal = Field(
        ..., description="Part B: Area Based Proposal"
    )
    part_c_pan_city_proposals: PartCPanCityProposals = Field(
        ..., description="Part C: Pan-City Proposal(s)"
    )
