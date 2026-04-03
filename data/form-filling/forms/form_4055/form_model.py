from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class SampleTableRow(BaseModel):
    """Single row in SAMPLE ID"""

    sample_id: str = Field(default="", description="Sample_Id")
    sample_description_serial_number: str = Field(
        default="", description="Sample_Description_Serial_Number"
    )
    sample_location: str = Field(default="", description="Sample_Location")
    area_volume_material: str = Field(default="", description="Area_Volume_Material")
    requested_analysis: str = Field(default="", description="Requested_Analysis")


class ClientContactSiteInformation(BaseModel):
    """Client, contact, and sampling site details"""

    contact: str = Field(
        ...,
        description=(
            'Primary contact person\'s name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    client_company_name_address: str = Field(
        ...,
        description=(
            "Client or company name and first line of mailing address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Primary phone number for the contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    client_company_name_address_line_2: str = Field(
        default="",
        description=(
            "Second line of client/company address (e.g., suite, building) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            'Email address for the contact .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    client_company_name_address_line_3: str = Field(
        default="",
        description=(
            'Third line of client/company address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reference_number: str = Field(
        default="",
        description=(
            'Project or internal reference number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    client_company_name_address_line_4: str = Field(
        default="",
        description=(
            "Fourth line of client/company address (e.g., city, state, ZIP) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    sampled_by: str = Field(
        ...,
        description=(
            "Name of the person who collected the samples .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    client_site_address_same: BooleanLike = Field(
        default="", description="Indicate if the client address and site address are identical"
    )

    date_sampled: str = Field(
        ..., description="Date on which the samples were collected"
    )  # YYYY-MM-DD format

    site_address: str = Field(
        ...,
        description=(
            "Site address where samples were collected (first line) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    site_address_line_2: str = Field(
        default="",
        description=(
            "Additional line for site address (e.g., city, state, ZIP) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class LaboratoryUseOnly(BaseModel):
    """Laboratory receipt and project identification"""

    samples_received_in_proper_condition: BooleanLike = Field(
        default="",
        description="For laboratory use: confirm samples were received in acceptable condition",
    )

    laboratory_project_id: str = Field(
        default="",
        description=(
            "Identifier assigned by the laboratory to this project .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class TurnAroundTime(BaseModel):
    """Requested analysis turnaround time"""

    rush: BooleanLike = Field(
        default="",
        description="Select if rush turnaround (under 24 hours, special request) is required",
    )

    turnaround_24_hours: BooleanLike = Field(
        default="", description="Select if 24-hour turnaround is requested"
    )

    turnaround_2_3_days: BooleanLike = Field(
        default="", description="Select if 2–3 day turnaround is requested"
    )

    turnaround_4_plus_days: BooleanLike = Field(
        default="", description="Select if 4 or more day turnaround is acceptable"
    )


class ProjectInformation(BaseModel):
    """Internal project number and general comments"""

    acm_project_number: str = Field(
        default="",
        description=(
            'ACM internal project number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    comments_line_1: str = Field(
        default="",
        description=(
            "First line of comments or special instructions .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    comments_line_2: str = Field(
        default="",
        description=(
            "Second line of comments or special instructions .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    comments_line_3: str = Field(
        default="",
        description=(
            "Third line of comments or special instructions .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    comments_line_4: str = Field(
        default="",
        description=(
            "Fourth line of comments or special instructions .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    comments_line_5: str = Field(
        default="",
        description=(
            "Fifth line of comments or special instructions .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    comments_line_6: str = Field(
        default="",
        description=(
            "Sixth line of comments or special instructions .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    comments_line_7: str = Field(
        default="",
        description=(
            "Seventh line of comments or special instructions .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    comments_line_8: str = Field(
        default="",
        description=(
            "Eighth line of comments or special instructions .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class RequestedAnalysis(BaseModel):
    """Types of analyses requested for samples"""

    asbestos_bulk_plm: BooleanLike = Field(
        default="", description="Request asbestos bulk analysis by PLM"
    )

    asbestos_point_count: BooleanLike = Field(
        default="", description="Request asbestos point count analysis"
    )

    fungi_spore_trap_analysis_air: BooleanLike = Field(
        default="", description="Request fungi spore trap analysis of air samples"
    )

    fungi_direct_examination_tape: BooleanLike = Field(
        default="", description="Request fungi direct examination of tape samples"
    )

    clear_tape_for_pollen_coliform_bacteria: BooleanLike = Field(
        default="", description="Request clear tape analysis for pollen or coliform bacteria"
    )

    other_please_specify: str = Field(
        default="",
        description=(
            "Specify any other requested analysis not listed above .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SampleTable(BaseModel):
    """Per-sample identifiers, locations, and requested analyses"""

    sample_table: List[SampleTableRow] = Field(
        ...,
        description=(
            "Table to record sample identifiers, descriptions, locations, "
            "areas/volumes/materials, and requested analyses"
        ),
    )  # List of table rows

    sample_description_serial_number: str = Field(
        default="",
        description=(
            "Description or serial number of the sample (captured per row in the table) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    sample_location: str = Field(
        default="",
        description=(
            "Location where the sample was collected (captured per row in the table) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    area_volume_material: str = Field(
        default="",
        description=(
            "Area, volume, or material description for the sample (captured per row in the "
            'table) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    requested_analysis: str = Field(
        default="",
        description=(
            "Requested analysis for each sample (corresponding to columns at right of the "
            'table) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class ChainofCustody(BaseModel):
    """Sample custody and processing sign-off"""

    submitted_relinquished_by: str = Field(
        ...,
        description=(
            "Name of person submitting or relinquishing the samples .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    submitted_relinquished_by_date_time: str = Field(
        ...,
        description=(
            "Date and time when samples were submitted or relinquished .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    received_accepted_by: str = Field(
        ...,
        description=(
            "Name of person who received or accepted the samples .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    received_accepted_by_date_time: str = Field(
        ...,
        description=(
            "Date and time when samples were received or accepted .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    samples_processed_by: str = Field(
        default="",
        description=(
            "Name of person who processed the samples .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    samples_processed_by_date_time: str = Field(
        default="",
        description=(
            "Date and time when samples were processed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ChainofcustodyAnalysisRequestForm(BaseModel):
    """
    Chain-of-Custody / Analysis Request Form

    ''
    """

    client__contact__site_information: ClientContactSiteInformation = Field(
        ..., description="Client / Contact / Site Information"
    )
    laboratory_use_only: LaboratoryUseOnly = Field(..., description="Laboratory Use Only")
    turn_around_time: TurnAroundTime = Field(..., description="Turn Around Time")
    project_information: ProjectInformation = Field(..., description="Project Information")
    requested_analysis: RequestedAnalysis = Field(..., description="Requested Analysis")
    sample_table: SampleTable = Field(..., description="Sample Table")
    chain_of_custody: ChainofCustody = Field(..., description="Chain of Custody")
