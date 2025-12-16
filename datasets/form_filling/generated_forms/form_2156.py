from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class VolunteerHistory(BaseModel):
    """Previous volunteer experience, including current or most recent and prior volunteer roles"""

    have_you_previously_served_as_a_volunteer: BooleanLike = Field(
        default="", description="Indicate whether you have previously served as a volunteer."
    )

    where_and_when: str = Field(
        default="",
        description=(
            "If you have volunteered before, briefly describe where and when. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    current_or_most_recent_agency_organization: str = Field(
        default="",
        description=(
            "Name of the current or most recent agency or organization where you "
            'volunteered. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    current_or_most_recent_your_title: str = Field(
        default="",
        description=(
            "Your title or role at the current or most recent volunteer "
            'agency/organization. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    current_or_most_recent_telephone: str = Field(
        default="",
        description=(
            "Telephone number for the current or most recent volunteer agency/organization. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    current_or_most_recent_mailing_address: str = Field(
        default="",
        description=(
            "Mailing address of the current or most recent volunteer agency/organization. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    current_or_most_recent_city_state_zip: str = Field(
        default="",
        description=(
            "City, state, and ZIP code for the current or most recent volunteer "
            'agency/organization. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    current_or_most_recent_date_began: str = Field(
        default="", description="Date you began volunteering at this agency/organization."
    )  # YYYY-MM-DD format

    current_or_most_recent_date_ended: str = Field(
        default="", description="Date you ended volunteering at this agency/organization."
    )  # YYYY-MM-DD format

    current_or_most_recent_number_supervised_by_you: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of individuals you supervised in this volunteer role, if any.",
    )

    current_or_most_recent_duties_line_1: str = Field(
        default="",
        description=(
            "Description of your primary duties in this volunteer role (first line). .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    current_or_most_recent_duties_line_2: str = Field(
        default="",
        description=(
            "Additional description of your duties in this volunteer role (second line). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    current_or_most_recent_reason_for_leaving_line_1: str = Field(
        default="",
        description=(
            "Reason you left this volunteer position (first line). .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    current_or_most_recent_reason_for_leaving_line_2: str = Field(
        default="",
        description=(
            "Additional details about your reason for leaving this volunteer position "
            '(second line). .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    volunteer_history_agency_organization_2: str = Field(
        default="",
        description=(
            "Name of a second volunteer agency or organization. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    volunteer_history_your_title_2: str = Field(
        default="",
        description=(
            "Your title or role at the second volunteer agency/organization. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    volunteer_history_telephone_2: str = Field(
        default="",
        description=(
            "Telephone number for the second volunteer agency/organization. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    volunteer_history_mailing_address_2: str = Field(
        default="",
        description=(
            "Mailing address of the second volunteer agency/organization. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    volunteer_history_city_state_zip_2: str = Field(
        default="",
        description=(
            "City, state, and ZIP code for the second volunteer agency/organization. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    volunteer_history_date_began_2: str = Field(
        default="", description="Date you began volunteering at the second agency/organization."
    )  # YYYY-MM-DD format

    volunteer_history_date_ended_2: str = Field(
        default="", description="Date you ended volunteering at the second agency/organization."
    )  # YYYY-MM-DD format

    volunteer_history_number_supervised_by_you_2: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of individuals you supervised in this second volunteer role, if any.",
    )

    volunteer_history_duties_2_line_1: str = Field(
        default="",
        description=(
            "Description of your primary duties in the second volunteer role (first line). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    volunteer_history_duties_2_line_2: str = Field(
        default="",
        description=(
            "Additional description of your duties in the second volunteer role (second "
            'line). .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    volunteer_history_reason_for_leaving_2_line_1: str = Field(
        default="",
        description=(
            "Reason you left the second volunteer position (first line). .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    volunteer_history_reason_for_leaving_2_line_2: str = Field(
        default="",
        description=(
            "Additional details about your reason for leaving the second volunteer position "
            '(second line). .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    volunteer_history_agency_organization_3: str = Field(
        default="",
        description=(
            "Name of a third volunteer agency or organization. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    volunteer_history_your_title_3: str = Field(
        default="",
        description=(
            "Your title or role at the third volunteer agency/organization. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    volunteer_history_telephone_3: str = Field(
        default="",
        description=(
            "Telephone number for the third volunteer agency/organization. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    volunteer_history_mailing_address_3: str = Field(
        default="",
        description=(
            "Mailing address of the third volunteer agency/organization. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    volunteer_history_city_state_zip_3: str = Field(
        default="",
        description=(
            "City, state, and ZIP code for the third volunteer agency/organization. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    volunteer_history_date_began_3: str = Field(
        default="", description="Date you began volunteering at the third agency/organization."
    )  # YYYY-MM-DD format

    volunteer_history_date_ended_3: str = Field(
        default="", description="Date you ended volunteering at the third agency/organization."
    )  # YYYY-MM-DD format

    volunteer_history_number_supervised_by_you_3: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of individuals you supervised in this third volunteer role, if any.",
    )

    volunteer_history_duties_3_line_1: str = Field(
        default="",
        description=(
            "Description of your primary duties in the third volunteer role (first line). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    volunteer_history_duties_3_line_2: str = Field(
        default="",
        description=(
            "Additional description of your duties in the third volunteer role (second "
            'line). .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    volunteer_history_reason_for_leaving_3_line_1: str = Field(
        default="",
        description=(
            "Reason you left the third volunteer position (first line). .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    volunteer_history_reason_for_leaving_3_line_2: str = Field(
        default="",
        description=(
            "Additional details about your reason for leaving the third volunteer position "
            '(second line). .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class WorkHistory(BaseModel):
    """Employment history and related duties"""

    work_history_agency_organization_1: str = Field(
        default="",
        description=(
            "Name of the first work (paid employment) agency or organization. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    work_history_your_title_1: str = Field(
        default="",
        description=(
            "Your job title at the first work agency/organization. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_history_telephone_1: str = Field(
        default="",
        description=(
            "Telephone number for the first work agency/organization. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_history_mailing_address_1: str = Field(
        default="",
        description=(
            "Mailing address of the first work agency/organization. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_history_city_state_zip_1: str = Field(
        default="",
        description=(
            "City, state, and ZIP code for the first work agency/organization. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    work_history_date_began_1: str = Field(
        default="", description="Date you began working at the first agency/organization."
    )  # YYYY-MM-DD format

    work_history_date_ended_1: str = Field(
        default="", description="Date you ended working at the first agency/organization."
    )  # YYYY-MM-DD format

    work_history_number_supervised_by_you_1: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of individuals you supervised in this first work role, if any.",
    )

    work_history_duties_1_line_1: str = Field(
        default="",
        description=(
            "Description of your primary duties in the first work role (first line). .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    work_history_duties_1_line_2: str = Field(
        default="",
        description=(
            "Additional description of your duties in the first work role (second line). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    work_history_reason_for_leaving_1_line_1: str = Field(
        default="",
        description=(
            "Reason you left the first work position (first line). .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_history_reason_for_leaving_1_line_2: str = Field(
        default="",
        description=(
            "Additional details about your reason for leaving the first work position "
            '(second line). .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    work_history_agency_organization_2: str = Field(
        default="",
        description=(
            "Name of the second work (paid employment) agency or organization. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    work_history_your_title_2: str = Field(
        default="",
        description=(
            "Your job title at the second work agency/organization. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_history_telephone_2: str = Field(
        default="",
        description=(
            "Telephone number for the second work agency/organization. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_history_mailing_address_2: str = Field(
        default="",
        description=(
            "Mailing address of the second work agency/organization. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_history_city_state_zip_2: str = Field(
        default="",
        description=(
            "City, state, and ZIP code for the second work agency/organization. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    work_history_date_began_2: str = Field(
        default="", description="Date you began working at the second agency/organization."
    )  # YYYY-MM-DD format

    work_history_date_ended_2: str = Field(
        default="", description="Date you ended working at the second agency/organization."
    )  # YYYY-MM-DD format

    work_history_number_supervised_by_you_2: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of individuals you supervised in this second work role, if any.",
    )

    work_history_duties_2_line_1: str = Field(
        default="",
        description=(
            "Description of your primary duties in the second work role (first line). .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    work_history_duties_2_line_2: str = Field(
        default="",
        description=(
            "Additional description of your duties in the second work role (second line). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    work_history_reason_for_leaving_2_line_1: str = Field(
        default="",
        description=(
            "Reason you left the second work position (first line). .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_history_reason_for_leaving_2_line_2: str = Field(
        default="",
        description=(
            "Additional details about your reason for leaving the second work position "
            '(second line). .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class VolunteerHistory(BaseModel):
    """
    Volunteer History

    Have you previously served as a volunteer? Where and when? Please list below.
    """

    volunteer_history: VolunteerHistory = Field(..., description="Volunteer History")
    work_history: WorkHistory = Field(..., description="Work History")
