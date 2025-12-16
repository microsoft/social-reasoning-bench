from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OtherPets(BaseModel):
    """Information about current and past pets, behavior, and training"""

    what_other_pets_do_you_currently_have_specify_type_number_and_age_please: str = Field(
        default="",
        description=(
            "List all other current pets, including species, number of each, and their "
            'ages. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    are_these_pets_up_to_date_on_vaccines_and_spayed_neutered: str = Field(
        default="",
        description=(
            "Explain whether your current pets are vaccinated and spayed/neutered, and "
            'provide details if needed. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    if_you_do_not_have_current_pets_have_you_owned_a_dog_before_please_elaborate_when_in_your_life_type_etc: str = Field(
        default="",
        description=(
            "Describe any previous dog ownership, including when in your life and what type "
            'of dog. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    have_you_ever_surrendered_a_pet_if_so_why: str = Field(
        default="",
        description=(
            "Indicate whether you have ever surrendered a pet and explain the "
            'circumstances. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    have_you_ever_had_a_pet_euthanized_if_so_why: str = Field(
        default="",
        description=(
            "Explain any past experience having a pet euthanized and the reasons. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    have_you_ever_lost_a_pet_to_an_accident: str = Field(
        default="",
        description=(
            "Describe any experience losing a pet due to an accident. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    how_do_you_discipline_correct_your_pets: str = Field(
        default="",
        description=(
            "Describe your methods for disciplining or correcting your pets. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    reasons_to_rehome_return_dog: Literal[
        "Chewing",
        "destructive",
        "barking",
        "aggressive with humans",
        "aggressive with other dogs",
        "digging",
        "escaping the yard",
        "biting",
        "going potty in the house",
        "owner is moving",
        "N/A",
        "",
    ] = Field(
        default="",
        description="Indicate which of these you consider valid reasons to rehome or return a dog.",
    )

    other_reason_to_rehome_return_dog: str = Field(
        default="",
        description=(
            "Specify any other reason you consider valid to rehome or return a dog. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    have_you_ever_had_to_seek_out_training_for_an_animal_how_did_that_go: str = Field(
        default="",
        description=(
            "Describe any experience seeking professional training for an animal and how it "
            'went. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    are_you_willing_to_invest_in_training_doggy_daycare_and_a_dog_walker_if_ever_necessary: str = (
        Field(
            default="",
            description=(
                "Explain your willingness to invest in training, doggy daycare, or a dog walker "
                'if needed. .If you cannot fill this, write "N/A". If this field should not '
                "be filled by you (for example, it belongs to another person or office), leave "
                'it blank (empty string "").'
            ),
        )
    )

    if_you_are_applying_for_a_puppy_have_you_ever_survived_puppyhood_before: str = Field(
        default="",
        description=(
            "Describe any prior experience raising a puppy through the puppy stage. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AbouttheDogCatYouWishtoAdopt(BaseModel):
    """Preferences and motivations for the animal you want to adopt"""

    please_describe_what_drew_you_to_this_particular_animal_and_why_you_want_this_animal: str = (
        Field(
            default="",
            description=(
                "Explain why you are interested in this specific animal and your reasons for "
                'wanting to adopt. .If you cannot fill this, write "N/A". If this field '
                "should not be filled by you (for example, it belongs to another person or "
                'office), leave it blank (empty string "").'
            ),
        )
    )

    what_is_your_idea_of_an_ideal_dog_cat_with_respect_to_personality: str = Field(
        default="",
        description=(
            "Describe the personality traits you consider ideal in a dog or cat. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    desired_age_and_sex: str = Field(
        default="",
        description=(
            "Indicate the preferred age range and sex of the animal you wish to adopt. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    desired_size: str = Field(
        default="",
        description=(
            "Indicate the preferred size of the animal (e.g., small, medium, large). .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class OtherPetsAboutTheDogcatYouWishToAdopt(BaseModel):
    """Other Pets

    About the Dog/Cat You Wish to Adopt"""

    other_pets: OtherPets = Field(..., description="Other Pets")
    about_the_dogcat_you_wish_to_adopt: AbouttheDogCatYouWishtoAdopt = Field(
        ..., description="About the Dog/Cat You Wish to Adopt"
    )
