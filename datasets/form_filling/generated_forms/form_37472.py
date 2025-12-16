from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class IncidentInformation(BaseModel):
    """Basic incident details and operational period"""

    incident_name: str = Field(
        ...,
        description=(
            'Name or identifier of the incident .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    operational_period_date_from: str = Field(
        ..., description="Start date of the operational period"
    )  # YYYY-MM-DD format

    operational_period_date_to: str = Field(
        ..., description="End date of the operational period"
    )  # YYYY-MM-DD format

    operational_period_time_from: str = Field(
        ...,
        description=(
            'Start time of the operational period .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    operational_period_time_to: str = Field(
        ...,
        description=(
            'End time of the operational period .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class MedicalAidStations(BaseModel):
    """Medical aid station locations and contact information"""

    medical_aid_station_name_row_1: str = Field(
        default="",
        description=(
            "Name or identifier of the first medical aid station .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    medical_aid_station_location_row_1: str = Field(
        default="",
        description=(
            "Location of the first medical aid station .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    medical_aid_station_contact_numbers_frequency_row_1: str = Field(
        default="",
        description=(
            "Contact phone number(s) or radio frequency for the first medical aid station "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    medical_aid_station_paramedics_on_site_yes_row_1: BooleanLike = Field(
        default="",
        description="Indicate YES if paramedics are on site at the first medical aid station",
    )

    medical_aid_station_paramedics_on_site_no_row_1: BooleanLike = Field(
        default="",
        description="Indicate NO if paramedics are not on site at the first medical aid station",
    )

    medical_aid_station_name_row_2: str = Field(
        default="",
        description=(
            "Name or identifier of the second medical aid station .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    medical_aid_station_location_row_2: str = Field(
        default="",
        description=(
            "Location of the second medical aid station .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    medical_aid_station_contact_numbers_frequency_row_2: str = Field(
        default="",
        description=(
            "Contact phone number(s) or radio frequency for the second medical aid station "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    medical_aid_station_paramedics_on_site_yes_row_2: BooleanLike = Field(
        default="",
        description="Indicate YES if paramedics are on site at the second medical aid station",
    )

    medical_aid_station_paramedics_on_site_no_row_2: BooleanLike = Field(
        default="",
        description="Indicate NO if paramedics are not on site at the second medical aid station",
    )

    medical_aid_station_name_row_3: str = Field(
        default="",
        description=(
            "Name or identifier of the third medical aid station .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    medical_aid_station_location_row_3: str = Field(
        default="",
        description=(
            "Location of the third medical aid station .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    medical_aid_station_contact_numbers_frequency_row_3: str = Field(
        default="",
        description=(
            "Contact phone number(s) or radio frequency for the third medical aid station "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    medical_aid_station_paramedics_on_site_yes_row_3: BooleanLike = Field(
        default="",
        description="Indicate YES if paramedics are on site at the third medical aid station",
    )

    medical_aid_station_paramedics_on_site_no_row_3: BooleanLike = Field(
        default="",
        description="Indicate NO if paramedics are not on site at the third medical aid station",
    )

    medical_aid_station_name_row_4: str = Field(
        default="",
        description=(
            "Name or identifier of the fourth medical aid station .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    medical_aid_station_location_row_4: str = Field(
        default="",
        description=(
            "Location of the fourth medical aid station .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    medical_aid_station_contact_numbers_frequency_row_4: str = Field(
        default="",
        description=(
            "Contact phone number(s) or radio frequency for the fourth medical aid station "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    medical_aid_station_paramedics_on_site_yes_row_4: BooleanLike = Field(
        default="",
        description="Indicate YES if paramedics are on site at the fourth medical aid station",
    )

    medical_aid_station_paramedics_on_site_no_row_4: BooleanLike = Field(
        default="",
        description="Indicate NO if paramedics are not on site at the fourth medical aid station",
    )

    medical_aid_station_name_row_5: str = Field(
        default="",
        description=(
            "Name or identifier of the fifth medical aid station .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    medical_aid_station_location_row_5: str = Field(
        default="",
        description=(
            "Location of the fifth medical aid station .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    medical_aid_station_contact_numbers_frequency_row_5: str = Field(
        default="",
        description=(
            "Contact phone number(s) or radio frequency for the fifth medical aid station "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    medical_aid_station_paramedics_on_site_yes_row_5: BooleanLike = Field(
        default="",
        description="Indicate YES if paramedics are on site at the fifth medical aid station",
    )

    medical_aid_station_paramedics_on_site_no_row_5: BooleanLike = Field(
        default="",
        description="Indicate NO if paramedics are not on site at the fifth medical aid station",
    )

    medical_aid_station_name_row_6: str = Field(
        default="",
        description=(
            "Name or identifier of the sixth medical aid station .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    medical_aid_station_location_row_6: str = Field(
        default="",
        description=(
            "Location of the sixth medical aid station .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    medical_aid_station_contact_numbers_frequency_row_6: str = Field(
        default="",
        description=(
            "Contact phone number(s) or radio frequency for the sixth medical aid station "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    medical_aid_station_paramedics_on_site_yes_row_6: BooleanLike = Field(
        default="",
        description="Indicate YES if paramedics are on site at the sixth medical aid station",
    )

    medical_aid_station_paramedics_on_site_no_row_6: BooleanLike = Field(
        default="",
        description="Indicate NO if paramedics are not on site at the sixth medical aid station",
    )


class Transportation(BaseModel):
    """Ambulance and other medical transportation resources"""

    ambulance_service_row_1: str = Field(
        default="",
        description=(
            "Name of the first ambulance or transport service .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ambulance_service_location_row_1: str = Field(
        default="",
        description=(
            "Location of the first ambulance or transport service .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ambulance_service_contact_numbers_frequency_row_1: str = Field(
        default="",
        description=(
            "Contact phone number(s) or radio frequency for the first ambulance service .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    ambulance_service_level_of_service_als_row_1: BooleanLike = Field(
        default="",
        description="Check if the first ambulance service provides Advanced Life Support (ALS)",
    )

    ambulance_service_level_of_service_bls_row_1: BooleanLike = Field(
        default="",
        description="Check if the first ambulance service provides Basic Life Support (BLS)",
    )

    ambulance_service_row_2: str = Field(
        default="",
        description=(
            "Name of the second ambulance or transport service .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ambulance_service_location_row_2: str = Field(
        default="",
        description=(
            "Location of the second ambulance or transport service .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ambulance_service_contact_numbers_frequency_row_2: str = Field(
        default="",
        description=(
            "Contact phone number(s) or radio frequency for the second ambulance service "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    ambulance_service_level_of_service_als_row_2: BooleanLike = Field(
        default="",
        description="Check if the second ambulance service provides Advanced Life Support (ALS)",
    )

    ambulance_service_level_of_service_bls_row_2: BooleanLike = Field(
        default="",
        description="Check if the second ambulance service provides Basic Life Support (BLS)",
    )

    ambulance_service_row_3: str = Field(
        default="",
        description=(
            "Name of the third ambulance or transport service .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ambulance_service_location_row_3: str = Field(
        default="",
        description=(
            "Location of the third ambulance or transport service .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ambulance_service_contact_numbers_frequency_row_3: str = Field(
        default="",
        description=(
            "Contact phone number(s) or radio frequency for the third ambulance service .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    ambulance_service_level_of_service_als_row_3: BooleanLike = Field(
        default="",
        description="Check if the third ambulance service provides Advanced Life Support (ALS)",
    )

    ambulance_service_level_of_service_bls_row_3: BooleanLike = Field(
        default="",
        description="Check if the third ambulance service provides Basic Life Support (BLS)",
    )

    ambulance_service_row_4: str = Field(
        default="",
        description=(
            "Name of the fourth ambulance or transport service .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ambulance_service_location_row_4: str = Field(
        default="",
        description=(
            "Location of the fourth ambulance or transport service .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ambulance_service_contact_numbers_frequency_row_4: str = Field(
        default="",
        description=(
            "Contact phone number(s) or radio frequency for the fourth ambulance service "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    ambulance_service_level_of_service_als_row_4: BooleanLike = Field(
        default="",
        description="Check if the fourth ambulance service provides Advanced Life Support (ALS)",
    )

    ambulance_service_level_of_service_bls_row_4: BooleanLike = Field(
        default="",
        description="Check if the fourth ambulance service provides Basic Life Support (BLS)",
    )


class Hospitals(BaseModel):
    """Receiving hospitals and their capabilities"""

    hospital_name_row_1: str = Field(
        default="",
        description=(
            'Name of the first receiving hospital .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    hospital_address_latitude_longitude_if_helipad_row_1: str = Field(
        default="",
        description=(
            "Address and, if applicable, latitude/longitude for the first hospital helipad "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    hospital_contact_numbers_frequency_row_1: str = Field(
        default="",
        description=(
            "Contact phone number(s) or radio frequency for the first hospital .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    hospital_travel_time_air_row_1: str = Field(
        default="",
        description=(
            "Estimated air travel time to the first hospital .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    hospital_travel_time_ground_row_1: str = Field(
        default="",
        description=(
            "Estimated ground travel time to the first hospital .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    hospital_trauma_center_yes_row_1: BooleanLike = Field(
        default="", description="Check YES if the first hospital is a trauma center"
    )

    hospital_trauma_center_level_row_1: str = Field(
        default="",
        description=(
            "Trauma center level (e.g., I, II, III) for the first hospital .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    hospital_trauma_center_no_row_1: BooleanLike = Field(
        default="", description="Check NO if the first hospital is not a trauma center"
    )

    hospital_burn_center_yes_row_1: BooleanLike = Field(
        default="", description="Check YES if the first hospital is a burn center"
    )

    hospital_burn_center_no_row_1: BooleanLike = Field(
        default="", description="Check NO if the first hospital is not a burn center"
    )

    hospital_helipad_yes_row_1: BooleanLike = Field(
        default="", description="Check YES if the first hospital has a helipad"
    )

    hospital_helipad_no_row_1: BooleanLike = Field(
        default="", description="Check NO if the first hospital does not have a helipad"
    )

    hospital_name_row_2: str = Field(
        default="",
        description=(
            'Name of the second receiving hospital .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    hospital_address_latitude_longitude_if_helipad_row_2: str = Field(
        default="",
        description=(
            "Address and, if applicable, latitude/longitude for the second hospital helipad "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    hospital_contact_numbers_frequency_row_2: str = Field(
        default="",
        description=(
            "Contact phone number(s) or radio frequency for the second hospital .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    hospital_travel_time_air_row_2: str = Field(
        default="",
        description=(
            "Estimated air travel time to the second hospital .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    hospital_travel_time_ground_row_2: str = Field(
        default="",
        description=(
            "Estimated ground travel time to the second hospital .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    hospital_trauma_center_yes_row_2: BooleanLike = Field(
        default="", description="Check YES if the second hospital is a trauma center"
    )

    hospital_trauma_center_level_row_2: str = Field(
        default="",
        description=(
            "Trauma center level (e.g., I, II, III) for the second hospital .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    hospital_trauma_center_no_row_2: BooleanLike = Field(
        default="", description="Check NO if the second hospital is not a trauma center"
    )

    hospital_burn_center_yes_row_2: BooleanLike = Field(
        default="", description="Check YES if the second hospital is a burn center"
    )

    hospital_burn_center_no_row_2: BooleanLike = Field(
        default="", description="Check NO if the second hospital is not a burn center"
    )

    hospital_helipad_yes_row_2: BooleanLike = Field(
        default="", description="Check YES if the second hospital has a helipad"
    )

    hospital_helipad_no_row_2: BooleanLike = Field(
        default="", description="Check NO if the second hospital does not have a helipad"
    )

    hospital_name_row_3: str = Field(
        default="",
        description=(
            'Name of the third receiving hospital .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    hospital_address_latitude_longitude_if_helipad_row_3: str = Field(
        default="",
        description=(
            "Address and, if applicable, latitude/longitude for the third hospital helipad "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    hospital_contact_numbers_frequency_row_3: str = Field(
        default="",
        description=(
            "Contact phone number(s) or radio frequency for the third hospital .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    hospital_travel_time_air_row_3: str = Field(
        default="",
        description=(
            "Estimated air travel time to the third hospital .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    hospital_travel_time_ground_row_3: str = Field(
        default="",
        description=(
            "Estimated ground travel time to the third hospital .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    hospital_trauma_center_yes_row_3: BooleanLike = Field(
        default="", description="Check YES if the third hospital is a trauma center"
    )

    hospital_trauma_center_level_row_3: str = Field(
        default="",
        description=(
            "Trauma center level (e.g., I, II, III) for the third hospital .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    hospital_trauma_center_no_row_3: BooleanLike = Field(
        default="", description="Check NO if the third hospital is not a trauma center"
    )

    hospital_burn_center_yes_row_3: BooleanLike = Field(
        default="", description="Check YES if the third hospital is a burn center"
    )

    hospital_burn_center_no_row_3: BooleanLike = Field(
        default="", description="Check NO if the third hospital is not a burn center"
    )

    hospital_helipad_yes_row_3: BooleanLike = Field(
        default="", description="Check YES if the third hospital has a helipad"
    )

    hospital_helipad_no_row_3: BooleanLike = Field(
        default="", description="Check NO if the third hospital does not have a helipad"
    )

    hospital_name_row_4: str = Field(
        default="",
        description=(
            'Name of the fourth receiving hospital .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    hospital_address_latitude_longitude_if_helipad_row_4: str = Field(
        default="",
        description=(
            "Address and, if applicable, latitude/longitude for the fourth hospital helipad "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    hospital_contact_numbers_frequency_row_4: str = Field(
        default="",
        description=(
            "Contact phone number(s) or radio frequency for the fourth hospital .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    hospital_travel_time_air_row_4: str = Field(
        default="",
        description=(
            "Estimated air travel time to the fourth hospital .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    hospital_travel_time_ground_row_4: str = Field(
        default="",
        description=(
            "Estimated ground travel time to the fourth hospital .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    hospital_trauma_center_yes_row_4: BooleanLike = Field(
        default="", description="Check YES if the fourth hospital is a trauma center"
    )

    hospital_trauma_center_level_row_4: str = Field(
        default="",
        description=(
            "Trauma center level (e.g., I, II, III) for the fourth hospital .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    hospital_trauma_center_no_row_4: BooleanLike = Field(
        default="", description="Check NO if the fourth hospital is not a trauma center"
    )

    hospital_burn_center_yes_row_4: BooleanLike = Field(
        default="", description="Check YES if the fourth hospital is a burn center"
    )

    hospital_burn_center_no_row_4: BooleanLike = Field(
        default="", description="Check NO if the fourth hospital is not a burn center"
    )

    hospital_helipad_yes_row_4: BooleanLike = Field(
        default="", description="Check YES if the fourth hospital has a helipad"
    )

    hospital_helipad_no_row_4: BooleanLike = Field(
        default="", description="Check NO if the fourth hospital does not have a helipad"
    )


class SpecialMedicalEmergencyProcedures(BaseModel):
    """Special procedures and aviation asset usage"""

    special_medical_emergency_procedures: str = Field(
        default="",
        description=(
            "Describe any special medical emergency procedures for this incident .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    check_box_if_aviation_assets_are_utilized_for_rescue: BooleanLike = Field(
        default="",
        description="Check if aviation assets (e.g., helicopters) are used for rescue operations",
    )


class ApprovalsandDocumentation(BaseModel):
    """Prepared by, approved by, and form tracking information"""

    prepared_by_medical_unit_leader_name: str = Field(
        ...,
        description=(
            "Name of the Medical Unit Leader who prepared this form .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    prepared_by_medical_unit_leader_signature: str = Field(
        ...,
        description=(
            "Signature of the Medical Unit Leader who prepared this form .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    approved_by_safety_officer_name: str = Field(
        ...,
        description=(
            "Name of the Safety Officer approving this form .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    approved_by_safety_officer_signature: str = Field(
        ...,
        description=(
            "Signature of the Safety Officer approving this form .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    iap_page: Union[float, Literal["N/A", ""]] = Field(
        default="", description="IAP page number for this ICS 206 form"
    )

    date_time: str = Field(
        default="",
        description=(
            "Date and time this form was completed or updated .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class MedicalPlanics206(BaseModel):
    """MEDICAL PLAN (ICS 206)"""

    incident_information: IncidentInformation = Field(..., description="Incident Information")
    medical_aid_stations: MedicalAidStations = Field(..., description="Medical Aid Stations")
    transportation: Transportation = Field(..., description="Transportation")
    hospitals: Hospitals = Field(..., description="Hospitals")
    special_medical_emergency_procedures: SpecialMedicalEmergencyProcedures = Field(
        ..., description="Special Medical Emergency Procedures"
    )
    approvals_and_documentation: ApprovalsandDocumentation = Field(
        ..., description="Approvals and Documentation"
    )
