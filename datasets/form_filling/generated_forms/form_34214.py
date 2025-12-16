from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ComplaintHeader(BaseModel):
    """Basic information about the complaint report"""

    incident_number: str = Field(
        default="",
        description=(
            "Incident or case number associated with this complaint, if known .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_report_filed: str = Field(
        ..., description="Calendar date when this complaint form is being filed"
    )  # YYYY-MM-DD format


class ReportingPartyInformation(BaseModel):
    """Information about the person filing the complaint"""

    reporting_party_name_last_first_middle: str = Field(
        ...,
        description=(
            "Full legal name of the person submitting the complaint (last, first, middle) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    reporting_party_home_phone: str = Field(
        default="",
        description=(
            "Home telephone number of the reporting party .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reporting_party_business: str = Field(
        default="",
        description=(
            "Work or business telephone number of the reporting party .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reporting_party_mobile: str = Field(
        default="",
        description=(
            "Mobile or cell phone number of the reporting party .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reporting_party_address_street_city_state_zip_code: str = Field(
        ...,
        description=(
            "Mailing address of the reporting party including street, city, state, and ZIP "
            'code .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    reporting_party_date_of_birth: str = Field(
        ..., description="Date of birth of the reporting party"
    )  # YYYY-MM-DD format

    reporting_party_driver_license: str = Field(
        default="",
        description=(
            "Driver license number of the reporting party .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class VictimofMisconduct(BaseModel):
    """Information about the victim if different from the reporting party"""

    victim_of_misconduct_name_last_first_middle: str = Field(
        default="",
        description=(
            "Full name of the victim of misconduct, if different from the reporting party "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    victim_of_misconduct_home_phone: str = Field(
        default="",
        description=(
            "Home telephone number of the victim of misconduct .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    victim_of_misconduct_business: str = Field(
        default="",
        description=(
            "Work or business telephone number of the victim of misconduct .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    victim_of_misconduct_mobile: str = Field(
        default="",
        description=(
            "Mobile or cell phone number of the victim of misconduct .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    victim_of_misconduct_address_street_city_state_zip_code: str = Field(
        default="",
        description=(
            "Mailing address of the victim of misconduct including street, city, state, and "
            'ZIP code .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class IncidentDetails(BaseModel):
    """Date, time, and location of the incident"""

    day_and_date_of_incident: str = Field(
        ..., description="Day of the week and calendar date when the incident occurred"
    )  # YYYY-MM-DD format

    time_of_incident: str = Field(
        ...,
        description=(
            "Approximate time when the incident occurred .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    location_of_incident: str = Field(
        ...,
        description=(
            "Specific location where the incident occurred .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Witnesses(BaseModel):
    """Witness information for the incident"""

    witness_name_row_1: str = Field(
        default="",
        description=(
            'Name of the first witness .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    witness_address_row_1: str = Field(
        default="",
        description=(
            'Mailing address of the first witness .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    witness_phone_numbers_home_mobile_bus_row_1: str = Field(
        default="",
        description=(
            "Contact phone numbers for the first witness (home, mobile, and/or business) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    witness_name_row_2: str = Field(
        default="",
        description=(
            'Name of the second witness .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    witness_address_row_2: str = Field(
        default="",
        description=(
            'Mailing address of the second witness .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    witness_phone_numbers_home_mobile_bus_row_2: str = Field(
        default="",
        description=(
            "Contact phone numbers for the second witness (home, mobile, and/or business) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class DepartmentMembersComplainedOf(BaseModel):
    """Information about the officer(s) or employee(s) named in the complaint"""

    name_of_officer_employee: str = Field(
        ...,
        description=(
            "Name of the department member the complaint is about .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    car_number_if_known: str = Field(
        default="",
        description=(
            "Patrol car or vehicle number of the officer/employee, if known .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    badge_number_if_known: str = Field(
        default="",
        description=(
            "Badge number of the officer/employee, if known .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class DescriptionofEvents(BaseModel):
    """Narrative description of the events leading to the complaint"""

    description_of_events_line_1: str = Field(
        ...,
        description=(
            "First line of the narrative description of the events leading to the complaint "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    description_of_events_line_2: str = Field(
        default="",
        description=(
            "Second line of the narrative description of the events leading to the "
            'complaint .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    description_of_events_line_3: str = Field(
        default="",
        description=(
            "Third line of the narrative description of the events leading to the complaint "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class ReceivingOfficerInformation(BaseModel):
    """Information about the person receiving the complaint"""

    signature_of_person_receiving_complaint: str = Field(
        ...,
        description=(
            "Signature of the department member who received this complaint .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    badge_number_of_person_receiving_complaint: str = Field(
        ...,
        description=(
            "Badge number of the department member who received this complaint .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    business_phone_of_person_receiving_complaint: str = Field(
        ...,
        description=(
            "Business phone number of the department member who received this complaint .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class CitrusHeightsPoliceDepartmentCivilianComplaintForm(BaseModel):
    """
        Citrus Heights Police Department
    Civilian Complaint Form

        ''
    """

    complaint_header: ComplaintHeader = Field(..., description="Complaint Header")
    reporting_party_information: ReportingPartyInformation = Field(
        ..., description="Reporting Party Information"
    )
    victim_of_misconduct: VictimofMisconduct = Field(..., description="Victim of Misconduct")
    incident_details: IncidentDetails = Field(..., description="Incident Details")
    witnesses: Witnesses = Field(..., description="Witnesses")
    department_members_complained_of: DepartmentMembersComplainedOf = Field(
        ..., description="Department Member(s) Complained Of"
    )
    description_of_events: DescriptionofEvents = Field(..., description="Description of Events")
    receiving_officer_information: ReceivingOfficerInformation = Field(
        ..., description="Receiving Officer Information"
    )
