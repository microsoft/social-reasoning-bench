from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class BHCAMembershipHistory(BaseModel):
    """Whether applicant or co-applicant have previously been BHCA members"""

    applicant_bhca_member_applicant_yes: BooleanLike = Field(
        default="", description="Check if the applicant has ever been a BHCA member."
    )

    applicant_bhca_member_applicant_no: BooleanLike = Field(
        default="", description="Check if the applicant has never been a BHCA member."
    )

    applicant_bhca_member_co_applicant_yes: BooleanLike = Field(
        default="", description="Check if the co-applicant has ever been a BHCA member."
    )

    applicant_bhca_member_co_applicant_no: BooleanLike = Field(
        default="", description="Check if the co-applicant has never been a BHCA member."
    )


class BassetHoundOwnership(BaseModel):
    """Experience and current ownership of Basset Hounds and other breeds"""

    how_long_have_you_had_basset_hounds_lt1_yr: BooleanLike = Field(
        default="", description="Select if you have had Basset Hounds for less than 1 year."
    )

    how_long_have_you_had_basset_hounds_1_5_yrs: BooleanLike = Field(
        default="", description="Select if you have had Basset Hounds for 1–5 years."
    )

    how_long_have_you_had_basset_hounds_6_10_yrs: BooleanLike = Field(
        default="", description="Select if you have had Basset Hounds for 6–10 years."
    )

    how_long_have_you_had_basset_hounds_11_20_yrs: BooleanLike = Field(
        default="", description="Select if you have had Basset Hounds for 11–20 years."
    )

    how_long_have_you_had_basset_hounds_20_yrs_plus: BooleanLike = Field(
        default="", description="Select if you have had Basset Hounds for more than 20 years."
    )

    how_many_basset_hounds_currently_own_1: BooleanLike = Field(
        default="", description="Select if your household currently owns 1 Basset Hound."
    )

    how_many_basset_hounds_currently_own_2_3: BooleanLike = Field(
        default="", description="Select if your household currently owns 2–3 Basset Hounds."
    )

    how_many_basset_hounds_currently_own_4_6: BooleanLike = Field(
        default="", description="Select if your household currently owns 4–6 Basset Hounds."
    )

    how_many_basset_hounds_currently_own_7_9: BooleanLike = Field(
        default="", description="Select if your household currently owns 7–9 Basset Hounds."
    )

    how_many_basset_hounds_currently_own_10_plus: BooleanLike = Field(
        default="", description="Select if your household currently owns 10 or more Basset Hounds."
    )

    other_breeds_owned_line_1: str = Field(
        default="",
        description=(
            "List other dog breeds you currently own or have owned (first line). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other_breeds_owned_line_2: str = Field(
        default="",
        description=(
            "Continue listing other dog breeds you currently own or have owned (second "
            'line). .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class AcquisitionofBassetHounds(BaseModel):
    """Sources from which you have acquired your Basset Hounds"""

    acquired_from_private_breeder: BooleanLike = Field(
        default="", description="Check if you acquired any Basset Hounds from a private breeder."
    )

    acquired_from_commercial_kennel: BooleanLike = Field(
        default="", description="Check if you acquired any Basset Hounds from a commercial kennel."
    )

    acquired_from_pet_store: BooleanLike = Field(
        default="", description="Check if you acquired any Basset Hounds from a pet store."
    )

    acquired_from_internet: BooleanLike = Field(
        default="", description="Check if you acquired any Basset Hounds via the internet."
    )

    acquired_from_rescue: BooleanLike = Field(
        default="",
        description="Check if you acquired any Basset Hounds through a rescue organization.",
    )


class InterestsandActivities(BaseModel):
    """Primary interests and activities with Basset Hounds"""

    primary_interests_companion: BooleanLike = Field(
        default="", description="Select if your primary interest in Basset Hounds is as companions."
    )

    primary_interests_rescue: BooleanLike = Field(
        default="",
        description="Select if your primary interest in Basset Hounds involves rescue activities.",
    )

    primary_interests_conformation: BooleanLike = Field(
        default="",
        description="Select if you are interested in conformation showing with Basset Hounds.",
    )

    primary_interests_obedience_rally: BooleanLike = Field(
        default="",
        description=(
            "Select if you are interested in obedience or rally activities with Basset Hounds."
        ),
    )

    primary_interests_therapy: BooleanLike = Field(
        default="", description="Select if you are interested in therapy work with Basset Hounds."
    )

    primary_interests_scent_work: BooleanLike = Field(
        default="", description="Select if you are interested in scent work with Basset Hounds."
    )

    primary_interests_tracking: BooleanLike = Field(
        default="",
        description="Select if you are interested in tracking activities with Basset Hounds.",
    )

    primary_interests_agility: BooleanLike = Field(
        default="", description="Select if you are interested in agility with Basset Hounds."
    )

    primary_interests_trick_dog: BooleanLike = Field(
        default="",
        description="Select if you are interested in trick dog activities with Basset Hounds.",
    )

    primary_interests_field_trial_hunting: BooleanLike = Field(
        default="",
        description="Select if you are interested in field trials or hunting with Basset Hounds.",
    )

    primary_interests_breeding: BooleanLike = Field(
        default="", description="Select if you are interested in breeding Basset Hounds."
    )


class BreedingExperienceandPractices(BaseModel):
    """Breeding history, AKC registration, stud services, and resale practices"""

    have_you_bred_basset_hounds_yes: BooleanLike = Field(
        default="", description="Check if you have bred any Basset Hounds or other dog breeds."
    )

    have_you_bred_basset_hounds_no: BooleanLike = Field(
        default="", description="Check if you have not bred any Basset Hounds or other dog breeds."
    )

    how_many_litters_in_total: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Enter the total number of litters you have bred."
    )

    how_often_have_you_bred_a_litter: str = Field(
        default="",
        description=(
            "Describe how frequently, on average, you have bred litters (e.g., once per "
            'year). .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    akc_registration_percentage_100: BooleanLike = Field(
        default="",
        description="Select if 100% of the puppies you bred were registered with the AKC.",
    )

    akc_registration_percentage_75_99: BooleanLike = Field(
        default="",
        description="Select if 75–99% of the puppies you bred were registered with the AKC.",
    )

    akc_registration_percentage_50_74: BooleanLike = Field(
        default="",
        description="Select if 50–74% of the puppies you bred were registered with the AKC.",
    )

    akc_registration_percentage_less_than_50: BooleanLike = Field(
        default="",
        description="Select if less than 50% of the puppies you bred were registered with the AKC.",
    )

    akc_registration_percentage_do_not_track: BooleanLike = Field(
        default="",
        description="Select if you do not track AKC registration percentages for puppies you bred.",
    )

    have_you_sold_stud_services_yes: BooleanLike = Field(
        default="", description="Check if you have sold stud services."
    )

    have_you_sold_stud_services_no: BooleanLike = Field(
        default="", description="Check if you have not sold stud services."
    )

    consigned_or_sold_dogs_for_resale_yes: BooleanLike = Field(
        default="",
        description=(
            "Check if you currently or previously consigned or sold dogs for resale through "
            "pet stores, auctions, or similar outlets."
        ),
    )

    consigned_or_sold_dogs_for_resale_no: BooleanLike = Field(
        default="",
        description=(
            "Check if you have never consigned or sold dogs for resale through pet stores, "
            "auctions, or similar outlets."
        ),
    )

    consigned_or_sold_dogs_explanation_ref_11: str = Field(
        default="",
        description=(
            "If you answered yes to consigning or selling dogs for resale, provide details "
            'in the referenced comment box. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    breeding_considered_hobby: BooleanLike = Field(
        default="", description="Select if you consider your breeding activities to be a hobby."
    )

    breeding_considered_commercial_venture: BooleanLike = Field(
        default="",
        description="Select if you consider your breeding activities to be a commercial venture.",
    )


class ClubMembershipsandJudging(BaseModel):
    """Other kennel club memberships and judging approvals"""

    kennel_clubs_belong_to_line_1: str = Field(
        default="",
        description=(
            "List all-breed kennel clubs you belong to and any offices held (first line). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    kennel_clubs_belong_to_line_2: str = Field(
        default="",
        description=(
            "Continue listing all-breed kennel clubs and offices held (second line). .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    akc_or_foreign_approved_judge_yes: BooleanLike = Field(
        default="", description="Check if you are an AKC or foreign-approved judge."
    )

    akc_or_foreign_approved_judge_no: BooleanLike = Field(
        default="", description="Check if you are not an AKC or foreign-approved judge."
    )

    judge_approvals_explanation_ref_13: str = Field(
        default="",
        description=(
            "If you are an approved judge, list organizations, breeds, and disciplines in "
            'the referenced comment box. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class BHCAApplicationMotivation(BaseModel):
    """Reasons for applying for BHCA membership"""

    reasons_for_applying_bhca_line_1: str = Field(
        default="",
        description=(
            "Describe your primary reasons for applying for BHCA membership (first line). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    reasons_for_applying_bhca_line_2: str = Field(
        default="",
        description=(
            "Continue describing your reasons for applying for BHCA membership (second "
            'line). .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class AdditionalComments(BaseModel):
    """Open-ended comments and any additional information"""

    comment_box_additional_info_line_1: str = Field(
        default="",
        description=(
            "Provide any additional information you would like BHCA to know about you "
            '(first line). .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    comment_box_additional_info_line_2: str = Field(
        default="",
        description=(
            "Continue providing any additional information you would like BHCA to know "
            '(second line). .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class ApplicantcoapplicantInformationForm(BaseModel):
    """
    Applicant/Co-Applicant Information Form

    ''
    """

    bhca_membership_history: BHCAMembershipHistory = Field(
        ..., description="BHCA Membership History"
    )
    basset_hound_ownership: BassetHoundOwnership = Field(..., description="Basset Hound Ownership")
    acquisition_of_basset_hounds: AcquisitionofBassetHounds = Field(
        ..., description="Acquisition of Basset Hounds"
    )
    interests_and_activities: InterestsandActivities = Field(
        ..., description="Interests and Activities"
    )
    breeding_experience_and_practices: BreedingExperienceandPractices = Field(
        ..., description="Breeding Experience and Practices"
    )
    club_memberships_and_judging: ClubMembershipsandJudging = Field(
        ..., description="Club Memberships and Judging"
    )
    bhca_application_motivation: BHCAApplicationMotivation = Field(
        ..., description="BHCA Application Motivation"
    )
    additional_comments: AdditionalComments = Field(..., description="Additional Comments")
