from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AgencyInformation(BaseModel):
    """Basic information about the requesting agency and point of contact"""

    agency: str = Field(
        ...,
        description=(
            'Name of the requesting agency .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    agency_point_of_contact: str = Field(
        ...,
        description=(
            "Primary contact person for this request .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Phone number for the agency point of contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Email address for the agency point of contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class TrainingRequestDetails(BaseModel):
    """Information about the requested class and preferred dates"""

    requested_class: str = Field(
        ...,
        description=(
            "Describe the requested class or combination of classes and training days .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    preferred_dates_1st_choice: str = Field(
        ...,
        description=(
            "First choice for preferred training date(s) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    preferred_dates_2nd_choice: str = Field(
        default="",
        description=(
            "Second choice for preferred training date(s) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    preferred_dates_3rd_choice: str = Field(
        default="",
        description=(
            "Third choice for preferred training date(s) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class TrainingSiteLogistics(BaseModel):
    """Details about hosting facilities, equipment, capacity, and attendance"""

    have_facilities_yes: BooleanLike = Field(
        ...,
        description="Select if the agency has facilities available to host the requested training",
    )

    have_facilities_no: BooleanLike = Field(
        ...,
        description=(
            "Select if the agency does not have facilities available to host the requested training"
        ),
    )

    location_name_and_address: str = Field(
        default="",
        description=(
            "Name and full address of the training location, if facilities are available "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    additional_site_information_parking_building_entrance_and_any_covid_protocols_eg_face_masks_required_etc: str = Field(
        default="",
        description=(
            "Additional information about the site such as parking, building entrance, and "
            'any COVID or other protocols .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    technical_equipment_other: str = Field(
        default="",
        description=(
            "List any additional technical equipment available at the training site .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    lcd_projector: BooleanLike = Field(
        default="", description="Indicate if an LCD projector is available at the training site"
    )

    screen: BooleanLike = Field(
        default="", description="Indicate if a projection screen is available at the training site"
    )

    computer_powerpoint_presentation: BooleanLike = Field(
        default="",
        description="Indicate if a computer capable of running PowerPoint presentations is available",
    )

    speakers: BooleanLike = Field(
        default="", description="Indicate if audio speakers are available at the training site"
    )

    wifi: BooleanLike = Field(
        default="", description="Indicate if WiFi internet access is available at the training site"
    )

    printer: BooleanLike = Field(
        default="", description="Indicate if a printer is available at the training site"
    )

    site_seating_with_social_distancing: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Maximum number of attendees the site can seat while maintaining social distancing"
        ),
    )

    may_training_be_opened_for_other_agencies: str = Field(
        ...,
        description=(
            "Indicate yes or no, or provide conditions, for allowing other agencies to "
            'attend .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    number_attending_from_hosting_agency: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Estimated number of attendees from the hosting agency"
    )


class SCJAMobileTrainingRequestForm(BaseModel):
    """
        South Carolina Criminal Justice Academy
    Mobile Training Unit - Training Request Form

        The South Carolina Criminal Justice Academy’s Mobile Training Unit is flexible based on each agency’s needs and schedule. There are NO SCCJA associated fees for hosting or attending classes taught by the Mobile Training Unit. Classes may be taught as stand-alone or combined, as in-house only or opened to the field to suit the needs of an agency. For class description and associated CLEE credit hours, please refer to the Mobile Training Unit Course Catalog. Please complete this form and email to MobileTraining@SCCJA.SC.gov.
    """

    agency_information: AgencyInformation = Field(..., description="Agency Information")
    training_request_details: TrainingRequestDetails = Field(
        ..., description="Training Request Details"
    )
    training_site__logistics: TrainingSiteLogistics = Field(
        ..., description="Training Site & Logistics"
    )
