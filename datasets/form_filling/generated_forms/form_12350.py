from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ReportDetails(BaseModel):
    """Basic details about the report submission"""

    is_this_a_drill_report: BooleanLike = Field(
        default="",
        description="Indicate whether this report is for a drill rather than an actual incident",
    )

    yes_is_this_a_drill_report: BooleanLike = Field(
        default="", description="Select if the report is for a drill"
    )

    no_is_this_a_drill_report: BooleanLike = Field(
        default="", description="Select if the report is for an actual incident, not a drill"
    )

    e_mail_address: str = Field(
        default="",
        description=(
            "Primary email address for contact regarding this report .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ReportingParty(BaseModel):
    """Contact and organization information for the reporting party"""

    reporting_party_phone_1: str = Field(
        default="",
        description=(
            "Primary phone number for the reporting party .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reporting_party_phone_1_type: str = Field(
        default="",
        description=(
            "Type of primary phone (e.g., mobile, work, home) for the reporting party .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reporting_party_last_name: str = Field(
        default="",
        description=(
            "Last name (surname) of the reporting party .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reporting_party_first_name: str = Field(
        default="",
        description=(
            "First (given) name of the reporting party .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reporting_party_phone_2: str = Field(
        default="",
        description=(
            "Secondary phone number for the reporting party .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reporting_party_phone_2_type: str = Field(
        default="",
        description=(
            "Type of secondary phone (e.g., mobile, work, home) for the reporting party .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reporting_party_phone_3: str = Field(
        default="",
        description=(
            "Additional phone number for the reporting party .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reporting_party_phone_3_type: str = Field(
        default="",
        description=(
            "Type of additional phone (e.g., mobile, work, home) for the reporting party "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    reporting_party_company: str = Field(
        default="",
        description=(
            "Company name of the reporting party, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reporting_party_org_type: str = Field(
        default="",
        description=(
            "Type of organization for the reporting party (e.g., government, private, NGO) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    reporting_party_address: str = Field(
        default="",
        description=(
            "Street mailing address of the reporting party .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reporting_party_city: str = Field(
        default="",
        description=(
            'City of the reporting party\'s address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reporting_party_state: str = Field(
        default="", description="State or territory of the reporting party's address"
    )

    reporting_party_zip: str = Field(
        default="", description="ZIP or postal code of the reporting party's address"
    )

    are_you_calling_on_behalf_of_responsible_party: BooleanLike = Field(
        default="",
        description="Indicate if you are calling as a representative of the responsible party",
    )

    yes_are_you_calling_on_behalf_of_responsible_party: BooleanLike = Field(
        default="", description="Select if you are calling on behalf of the responsible party"
    )

    no_are_you_calling_on_behalf_of_responsible_party: BooleanLike = Field(
        default="", description="Select if you are not calling on behalf of the responsible party"
    )

    are_you_or_your_company_responsible_for_material_released: BooleanLike = Field(
        default="",
        description="Indicate whether you or your company is responsible for the material released",
    )

    yes_are_you_or_your_company_responsible_for_material_released: BooleanLike = Field(
        default="",
        description="Select if you or your company is responsible for the material released",
    )

    no_are_you_or_your_company_responsible_for_material_released: BooleanLike = Field(
        default="",
        description="Select if you or your company is not responsible for the material released",
    )


class SuspectedResponsibleParty(BaseModel):
    """Contact and organization information for the suspected responsible party"""

    suspected_responsible_party_last_name: str = Field(
        default="",
        description=(
            "Last name (surname) of the suspected responsible party .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    suspected_responsible_party_first_name: str = Field(
        default="",
        description=(
            "First (given) name of the suspected responsible party .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    suspected_responsible_party_phone_1: str = Field(
        default="",
        description=(
            "Primary phone number for the suspected responsible party .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    suspected_responsible_party_phone_1_type: str = Field(
        default="",
        description=(
            "Type of primary phone (e.g., mobile, work, home) for the suspected responsible "
            'party .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    suspected_responsible_party_phone_2: str = Field(
        default="",
        description=(
            "Secondary phone number for the suspected responsible party .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    suspected_responsible_party_phone_2_type: str = Field(
        default="",
        description=(
            "Type of secondary phone (e.g., mobile, work, home) for the suspected "
            'responsible party .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    suspected_responsible_party_phone_3: str = Field(
        default="",
        description=(
            "Additional phone number for the suspected responsible party .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    suspected_responsible_party_phone_3_type: str = Field(
        default="",
        description=(
            "Type of additional phone (e.g., mobile, work, home) for the suspected "
            'responsible party .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    suspected_responsible_party_company: str = Field(
        default="",
        description=(
            "Company name of the suspected responsible party, if applicable .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    suspected_responsible_party_org_type: str = Field(
        default="",
        description=(
            "Type of organization for the suspected responsible party (e.g., government, "
            'private, NGO) .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    suspected_responsible_party_address: str = Field(
        default="",
        description=(
            "Street mailing address of the suspected responsible party .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    suspected_responsible_party_city: str = Field(
        default="",
        description=(
            "City of the suspected responsible party's address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    suspected_responsible_party_state: str = Field(
        default="", description="State or territory of the suspected responsible party's address"
    )

    suspected_responsible_party_zip: str = Field(
        default="", description="ZIP or postal code of the suspected responsible party's address"
    )


class IncidentDescription(BaseModel):
    """Details about the incident itself"""

    description_of_incident: str = Field(
        default="",
        description=(
            "Narrative description of what happened, including circumstances and impacts "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    incident_date: str = Field(
        default="", description="Calendar date when the incident occurred"
    )  # YYYY-MM-DD format

    time: str = Field(
        default="",
        description=(
            "Time of the incident, including time zone if available .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    occurred_discovered_planned: str = Field(
        default="",
        description=(
            "Indicate whether the date/time is when the incident occurred, was discovered, "
            'or was planned .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class NationalResponseCenterVesselReport(BaseModel):
    """
        NATIONAL RESPONSE CENTER
    VESSEL REPORT

        The PDF Report should not be submitted to the NRC via fax or mail. They were created for use in Training and/or Response Plans, or as a guide when contacting the NRC.
    """

    report_details: ReportDetails = Field(..., description="Report Details")
    reporting_party: ReportingParty = Field(..., description="Reporting Party")
    suspected_responsible_party: SuspectedResponsibleParty = Field(
        ..., description="Suspected Responsible Party"
    )
    incident_description: IncidentDescription = Field(..., description="Incident Description")
