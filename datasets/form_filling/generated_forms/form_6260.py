from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MedicationAllergies(BaseModel):
    """Information about the child's allergies to medications"""

    is_your_child_allergic_to_any_medications: BooleanLike = Field(
        ..., description="Indicate whether your child is allergic to any medications."
    )

    is_your_child_allergic_to_any_medications_no: BooleanLike = Field(
        ..., description="Indicate whether your child is allergic to any medications."
    )

    if_yes_please_list_the_medications_and_describe_the_reaction_that_your_child_experiences: str = Field(
        default="",
        description=(
            "List the medications your child is allergic to and describe the reactions "
            'experienced. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class PartCOtherNeedsRequiringAssistanceWhileinCare(BaseModel):
    """Developmental and other assistance needs while the child is in care"""

    communication_eg_speech_language_delay: BooleanLike = Field(
        default="",
        description=(
            "Check if your child needs assistance with communication, such as speech or "
            "language delays."
        ),
    )

    social_emotional_eg_anxiety_disorder: BooleanLike = Field(
        default="",
        description=(
            "Check if your child needs assistance with social or emotional needs, such as anxiety."
        ),
    )

    behavior_eg_oppositional_defiant_disorder: BooleanLike = Field(
        default="", description="Check if your child needs assistance with behavioral needs."
    )

    developmental_eg_autism_spectrum_disorder: BooleanLike = Field(
        default="",
        description=(
            "Check if your child needs assistance with developmental needs, such as autism "
            "spectrum disorder."
        ),
    )

    learning_and_attention_eg_attention_deficit_hyperactivity_disorder: BooleanLike = Field(
        default="",
        description="Check if your child needs assistance with learning or attention, such as ADHD.",
    )

    if_you_checked_any_boxes_in_10_above_briefly_describe_the_type_of_assistance_your_child_will_need_while_in_care: str = Field(
        default="",
        description=(
            "Describe the specific assistance your child will need related to the checked "
            'developmental needs. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    briefly_describe_any_other_type_of_assistance_your_child_will_need_while_in_care_if_none_write_none: str = Field(
        default="",
        description=(
            "Describe any other assistance your child will need while in care, or write "
            '“None” if no assistance is needed. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class PartDEarlyInterventionandSpecialEducation(BaseModel):
    """Information about IFSP/IEP services the child is receiving"""

    is_your_child_receiving_services_through_ifsp_or_iep_yes: BooleanLike = Field(
        default="",
        description="Indicate whether your child is currently receiving IFSP or IEP services.",
    )

    is_your_child_receiving_services_through_ifsp_or_iep_no: BooleanLike = Field(
        default="",
        description="Indicate whether your child is currently receiving IFSP or IEP services.",
    )


class PartEEFMPEnrollment(BaseModel):
    """Exceptional Family Member Program enrollment status"""

    is_your_child_enrolled_in_the_efmp_yes: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether your child is enrolled in the Exceptional Family Member "
            "Program (EFMP)."
        ),
    )

    is_your_child_enrolled_in_the_efmp_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether your child is enrolled in the Exceptional Family Member "
            "Program (EFMP)."
        ),
    )


class SignaturesandAnnualReview(BaseModel):
    """Acknowledgment, staff review, and annual parent initials"""

    sponsors_signature_and_date: str = Field(
        ...,
        description=(
            "Sponsor signs and dates to certify the information provided is true and "
            'accurate. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    cyp_professionals_signature_and_date: str = Field(
        ...,
        description=(
            "CYP Professional signs and dates to confirm review of the information and need "
            'for accommodations. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    sponsors_initials_and_date_1: str = Field(
        default="",
        description=(
            "Sponsor’s initials and date for annual review (first entry). .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    sponsors_initials_and_date_2: str = Field(
        default="",
        description=(
            "Sponsor’s initials and date for annual review (second entry). .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    sponsors_initials_and_date_3: str = Field(
        default="",
        description=(
            "Sponsor’s initials and date for annual review (third entry). .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    sponsors_initials_and_date_4: str = Field(
        default="",
        description=(
            "Sponsor’s initials and date for annual review (fourth entry). .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class NavyChildAndYouthProgramHealthInformationForm170052(BaseModel):
    """
        NAVY CHILD AND YOUTH PROGRAM
    HEALTH INFORMATION FORM 1700/52

        PURPOSE: To provide Child and Youth Programs (CYP) with information about your child's overall health and needs that may affect his/her care at the CYP.
    """

    medication_allergies: MedicationAllergies = Field(..., description="Medication Allergies")
    part_c_other_needs_requiring_assistance_while_in_care: PartCOtherNeedsRequiringAssistanceWhileinCare = Field(
        ..., description="Part C: Other Needs Requiring Assistance While in Care"
    )
    part_d_early_intervention_and_special_education: PartDEarlyInterventionandSpecialEducation = (
        Field(..., description="Part D: Early Intervention and Special Education")
    )
    part_e_efmp_enrollment: PartEEFMPEnrollment = Field(..., description="Part E: EFMP Enrollment")
    signatures_and_annual_review: SignaturesandAnnualReview = Field(
        ..., description="Signatures and Annual Review"
    )
