from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicationFor(BaseModel):
    """Program selection and basic child information"""

    toddler_community_16_33_months_half_day_830am_1130am: BooleanLike = Field(
        default="",
        description=(
            "Select if applying for the Toddler Community half-day program (8:30am - 11:30am)."
        ),
    )

    toddler_community_16_33_months_full_day_830am_330pm: BooleanLike = Field(
        default="",
        description=(
            "Select if applying for the Toddler Community full-day program (8:30am - 3:30pm)."
        ),
    )

    toddler_community_16_33_months_extended_day_830am_530pm: BooleanLike = Field(
        default="",
        description=(
            "Select if applying for the Toddler Community extended day program (8:30am - 5:30pm)."
        ),
    )

    toddler_community_16_33_months_add_extended_morning_800_830am: BooleanLike = Field(
        default="",
        description=(
            "Select if requesting extended morning care (8:00am - 8:30am) for the Toddler "
            "Community."
        ),
    )

    childrens_house_3_6_years_half_day_830am_1230pm_lunch_recess: BooleanLike = Field(
        default="",
        description=(
            "Select if applying for the Children’s House half-day program (8:30am - "
            "12:30pm, includes lunch/recess)."
        ),
    )

    childrens_house_3_6_years_full_day_830am_330pm: BooleanLike = Field(
        default="",
        description="Select if applying for the Children’s House full-day program (8:30am - 3:30pm).",
    )

    childrens_house_3_6_years_all_day_childrens_house_830am_430pm: BooleanLike = Field(
        default="",
        description="Select if applying for the Children’s House all-day program (8:30am - 4:30pm).",
    )

    childrens_house_3_6_years_all_day_childrens_house_830am_530pm: BooleanLike = Field(
        default="",
        description="Select if applying for the Children’s House all-day program (8:30am - 5:30pm).",
    )

    childrens_house_3_6_years_add_extended_morning_730_830am: BooleanLike = Field(
        default="",
        description=(
            "Select if requesting extended morning care (7:30am - 8:30am) for the "
            "Children’s House program."
        ),
    )

    interested_starting_date: str = Field(
        default="", description="Desired date for your child to start attending."
    )  # YYYY-MM-DD format

    childs_full_name_first: str = Field(
        ...,
        description=(
            'Child’s legal first name. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    childs_full_name_middle: str = Field(
        default="",
        description=(
            'Child’s middle name. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    childs_full_name_last: str = Field(
        ...,
        description=(
            "Child’s legal last name (family name). .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    preferred_name_nickname: str = Field(
        default="",
        description=(
            "Name your child prefers to be called (nickname or preferred form). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Child’s date of birth.")  # YYYY-MM-DD format

    childs_age: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Child’s age at the time of application (in years, or years and months as applicable)."
        ),
    )

    male_female: Literal["Male", "Female", "N/A", ""] = Field(
        ..., description="Child’s sex as indicated on official records."
    )


class FamilyInformation(BaseModel):
    """Parent/guardian contact details and other children in the family"""

    parent_1_guardian_full_name: str = Field(
        ...,
        description=(
            "Full legal name of parent or guardian 1. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parent_2_guardian_full_name: str = Field(
        default="",
        description=(
            "Full legal name of parent or guardian 2 (if applicable). .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    parent_1_guardian_primary_phone: str = Field(
        ...,
        description=(
            "Primary phone number for parent or guardian 1. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parent_2_guardian_primary_phone: str = Field(
        default="",
        description=(
            "Primary phone number for parent or guardian 2. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parent_1_guardian_home_address: str = Field(
        ...,
        description=(
            "Street address for parent or guardian 1. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parent_2_guardian_home_address: str = Field(
        default="",
        description=(
            "Street address for parent or guardian 2. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parent_1_guardian_city_state_zip: str = Field(
        ...,
        description=(
            "City, state, and ZIP code for parent or guardian 1. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    parent_2_guardian_city_state_zip: str = Field(
        default="",
        description=(
            "City, state, and ZIP code for parent or guardian 2. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    parent_1_guardian_occupation: str = Field(
        default="",
        description=(
            "Occupation or job title of parent or guardian 1. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    parent_2_guardian_occupation: str = Field(
        default="",
        description=(
            "Occupation or job title of parent or guardian 2. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    parent_1_guardian_business: str = Field(
        default="",
        description=(
            "Employer or business name for parent or guardian 1. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    parent_2_guardian_business: str = Field(
        default="",
        description=(
            "Employer or business name for parent or guardian 2. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    parent_1_guardian_e_mail: str = Field(
        ...,
        description=(
            "Email address for parent or guardian 1. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parent_2_guardian_e_mail: str = Field(
        default="",
        description=(
            "Email address for parent or guardian 2. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    other_children_in_the_family_names: str = Field(
        default="",
        description=(
            "Names of other children in the family. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    other_children_in_the_family_birth_date: str = Field(
        default="", description="Birth date(s) of other children in the family."
    )  # YYYY-MM-DD format

    other_children_in_the_family_school_attending: str = Field(
        default="",
        description=(
            "Current school(s) attended by other children in the family. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class GettingtoKnowYourChildandFamily(BaseModel):
    """Child’s prior care experience and family’s concerns"""

    childs_current_or_previous_early_childhood_care_experience: str = Field(
        default="",
        description=(
            "Describe your child’s current or previous early childhood care arrangements "
            '(home, daycare, nanny, etc.). .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    reservations_or_concerns_about_having_your_child_in_a_school_setting: str = Field(
        default="",
        description=(
            "Share any specific reservations or concerns you have about your child being in "
            'a school setting. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class ApplicationForAdmissionCathedralHillMontessoriSchool(BaseModel):
    """
        Application for Admission
    Cathedral Hill Montessori School

        We strive to fully disclose our school and its programs to you and we ask you to provide information regarding your child’s education below. Children entering our Toddler Community must be walking steadily and at least 16 months old. Children entering our Children’s House program must be able to do the following independently: dress, eat, sleep, use the toilet and other basic self-care skills. To facilitate your child’s transition to a Montessori environment, please encourage your child’s independence in these areas.
    """

    application_for: ApplicationFor = Field(..., description="Application For")
    family_information: FamilyInformation = Field(..., description="Family Information")
    getting_to_know_your_child_and_family: GettingtoKnowYourChildandFamily = Field(
        ..., description="Getting to Know Your Child and Family"
    )
