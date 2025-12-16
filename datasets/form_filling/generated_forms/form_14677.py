from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AdoptionInterest(BaseModel):
    """Information about the pet the applicant is interested in and basic personal details"""

    interested_in: str = Field(
        ...,
        description=(
            "Type of animal or specific pet you are interested in adopting .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date: str = Field(..., description="Date this questionnaire is completed")  # YYYY-MM-DD format

    name: str = Field(
        ...,
        description=(
            'Your full legal name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    preferred_pronoun: str = Field(
        default="",
        description=(
            "Your preferred pronouns (e.g., she/her, he/him, they/them) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Your date of birth")  # YYYY-MM-DD format


class ContactAddressInformation(BaseModel):
    """Applicant’s address and contact details"""

    street_address: str = Field(
        ...,
        description=(
            "Street address where you currently live .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    apt_unit: str = Field(
        default="",
        description=(
            "Apartment or unit number, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    drivers_license_number: str = Field(
        ...,
        description=(
            'Your driver’s license number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of your current residence .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of your current residence")

    zip: str = Field(..., description="Zip code of your current residence")

    issuing_state: str = Field(..., description="State that issued your driver’s license")

    primary_phone: str = Field(
        ...,
        description=(
            "Primary phone number where you can be reached .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    primary_phone_type_cell_or_home: Literal["Cell", "Home", "N/A", ""] = Field(
        default="", description="Indicate whether your primary phone is a cell or home phone"
    )

    secondary_phone: str = Field(
        default="",
        description=(
            "Secondary phone number where you can be reached .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    secondary_phone_type_cell_or_home: Literal["Cell", "Home", "N/A", ""] = Field(
        default="", description="Indicate whether your secondary phone is a cell or home phone"
    )

    email: str = Field(
        ...,
        description=(
            "Email address where you can be contacted .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class HouseholdExistingPets(BaseModel):
    """Household composition, residence type, and current pets"""

    type_of_residence_house_apartment_etc: str = Field(
        ...,
        description=(
            "Describe your type of housing (e.g., house, apartment, condo) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    ages_of_children_in_the_home: str = Field(
        default="",
        description=(
            "List the ages of any children living in your home .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    cats_number_in_home: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of cats currently living in your home"
    )

    dogs_number_in_home: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of dogs currently living in your home"
    )

    other_number_in_home: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of other types of pets currently living in your home"
    )

    other_species: str = Field(
        default="",
        description=(
            "Species of other pets in your home (e.g., rabbit, bird, reptile) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    are_existing_pets_spayed_or_neutered_yes: BooleanLike = Field(
        default="", description="Check if your existing pets are spayed or neutered"
    )

    are_existing_pets_spayed_or_neutered_no: BooleanLike = Field(
        default="", description="Check if your existing pets are not spayed or neutered"
    )

    veterinary_clinics_name: str = Field(
        default="",
        description=(
            "Name of your current or preferred veterinary clinic .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class YouandYourHome(BaseModel):
    """Applicant’s experience with animals and time at home"""

    prior_animal_experience_childhood_pets: BooleanLike = Field(
        default="",
        description="Select if your prior animal experience is primarily with childhood pets",
    )

    prior_animal_experience_first_time_pet_owner: BooleanLike = Field(
        default="", description="Select if this will be your first time owning a pet"
    )

    prior_animal_experience_experienced_pet_owner: BooleanLike = Field(
        default="", description="Select if you are an experienced pet owner"
    )

    time_away_from_home_home_all_day: BooleanLike = Field(
        default="", description="Select if someone is home all day"
    )

    time_away_from_home_away_part_time_4_7_hours: BooleanLike = Field(
        default="", description="Select if you are away from home part time (4–7 hours per day)"
    )

    time_away_from_home_away_full_day_7_10_hours: BooleanLike = Field(
        default="", description="Select if you are away from home a full day (7–10 hours per day)"
    )

    time_away_from_home_travel_frequently: BooleanLike = Field(
        default="", description="Select if you travel frequently and are often away from home"
    )


class PetPreferences(BaseModel):
    """What the applicant is looking for in a pet and additional details"""

    what_are_you_looking_for_in_a_pet_couch_potato: BooleanLike = Field(
        default="", description="Select if you want a low-energy, relaxed pet"
    )

    what_are_you_looking_for_in_a_pet_occasional_adventurer: BooleanLike = Field(
        default="",
        description="Select if you want a pet that occasionally enjoys adventures or outings",
    )

    what_are_you_looking_for_in_a_pet_playful: BooleanLike = Field(
        default="", description="Select if you want a playful, energetic pet"
    )

    what_are_you_looking_for_in_a_pet_consistent_companion: BooleanLike = Field(
        default="", description="Select if you want a pet that is a steady, constant companion"
    )

    what_are_you_looking_for_in_a_pet_good_w_kids: BooleanLike = Field(
        default="", description="Select if you need a pet that is good with children"
    )

    what_are_you_looking_for_in_a_pet_working_dog: BooleanLike = Field(
        default="",
        description=(
            "Select if you are looking for a working dog (e.g., farm, service, or "
            "task-oriented work)"
        ),
    )

    what_are_you_looking_for_in_a_pet_snuggler: BooleanLike = Field(
        default="", description="Select if you want a pet that enjoys cuddling and close contact"
    )

    what_are_you_looking_for_in_a_pet_running_partner: BooleanLike = Field(
        default="", description="Select if you want a pet that can be a running or exercise partner"
    )

    what_are_you_looking_for_in_a_pet_social_butterfly: BooleanLike = Field(
        default="", description="Select if you want a pet that is very social and outgoing"
    )

    what_are_you_looking_for_in_a_pet_travel_buddy: BooleanLike = Field(
        default="", description="Select if you want a pet that can travel with you frequently"
    )

    what_are_you_looking_for_in_a_pet_good_w_other_animals: BooleanLike = Field(
        default="", description="Select if you need a pet that gets along well with other animals"
    )

    what_are_you_looking_for_in_a_pet_barn_cat: BooleanLike = Field(
        default="", description="Select if you are specifically looking for a barn cat"
    )

    tell_us_more_line_1: str = Field(
        default="",
        description=(
            "Additional information about what you are looking for in a pet (line 1) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    tell_us_more_line_2: str = Field(
        default="",
        description=(
            "Additional information about what you are looking for in a pet (line 2) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    tell_us_more_line_3: str = Field(
        default="",
        description=(
            "Additional information about what you are looking for in a pet (line 3) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    tell_us_more_line_4: str = Field(
        default="",
        description=(
            "Additional information about what you are looking for in a pet (line 4) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class DiscussionPoints(BaseModel):
    """Topics where the applicant would like more information and additional questions"""

    what_would_you_like_more_information_on_introduction_to_other_animals: BooleanLike = Field(
        default="",
        description="Select if you want information on introducing a new pet to other animals",
    )

    what_would_you_like_more_information_on_introduction_to_children: BooleanLike = Field(
        default="",
        description="Select if you want information on introducing a new pet to children",
    )

    what_would_you_like_more_information_on_medical_care_veterinarians: BooleanLike = Field(
        default="",
        description="Select if you want information on veterinary care and medical needs",
    )

    what_would_you_like_more_information_on_nail_trimming_grooming: BooleanLike = Field(
        default="", description="Select if you want information on nail trimming and grooming"
    )

    what_would_you_like_more_information_on_feeding: BooleanLike = Field(
        default="", description="Select if you want information on feeding and nutrition"
    )

    what_would_you_like_more_information_on_bite_inhibition: BooleanLike = Field(
        default="", description="Select if you want information on teaching bite inhibition"
    )

    what_would_you_like_more_information_on_appropriate_play: BooleanLike = Field(
        default="", description="Select if you want information on appropriate play behaviors"
    )

    what_would_you_like_more_information_on_training_resources: BooleanLike = Field(
        default="", description="Select if you want information on training classes or resources"
    )

    what_would_you_like_more_information_on_house_training_litterbox: BooleanLike = Field(
        default="", description="Select if you want information on house training or litterbox use"
    )

    additional_topics_or_questions_line_1: str = Field(
        default="",
        description=(
            "Additional questions or topics you would like to discuss (line 1) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    additional_topics_or_questions_line_2: str = Field(
        default="",
        description=(
            "Additional questions or topics you would like to discuss (line 2) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    additional_topics_or_questions_line_3: str = Field(
        default="",
        description=(
            "Additional questions or topics you would like to discuss (line 3) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    additional_topics_or_questions_line_4: str = Field(
        default="",
        description=(
            "Additional questions or topics you would like to discuss (line 4) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    additional_topics_or_questions_line_5: str = Field(
        default="",
        description=(
            "Additional questions or topics you would like to discuss (line 5) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class GreenhillHumaneSocietyAdoptionQuestionnaire(BaseModel):
    """
        Greenhill Humane Society
    Adoption Questionnaire

        Thank you for considering adoption! This questionnaire will help us work together to determine the best pet for your lifestyle as well as to provide you with resources and education to make your adoption successful.
    """

    adoption_interest: AdoptionInterest = Field(..., description="Adoption Interest")
    contact__address_information: ContactAddressInformation = Field(
        ..., description="Contact & Address Information"
    )
    household__existing_pets: HouseholdExistingPets = Field(
        ..., description="Household & Existing Pets"
    )
    you_and_your_home: YouandYourHome = Field(..., description="You and Your Home")
    pet_preferences: PetPreferences = Field(..., description="Pet Preferences")
    discussion_points: DiscussionPoints = Field(..., description="Discussion Points")
