from typing import List, Literal, Optional, Union

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
    asbestos_bulk_plm: str = Field(default="", description="Asbestos_Bulk_Plm")
    asbestos_point_count: str = Field(default="", description="Asbestos_Point_Count")
    fungi_spore_trap_analysis_air: str = Field(
        default="", description="Fungi_Spore_Trap_Analysis_Air"
    )
    fungi_direct_examination_tape: str = Field(
        default="", description="Fungi_Direct_Examination_Tape"
    )
    lead_paint_chip_analysis: str = Field(default="", description="Lead_Paint_Chip_Analysis")
    c_of_c_with_pcb_caulk_sediment: str = Field(
        default="", description="C_Of_C_With_Pcb_Caulk_Sediment"
    )
    other_please_specify: str = Field(default="", description="Other_Please_Specify")


class ClientContactSiteInformation(BaseModel):
    """Client contact details and sampling/site information"""

    contact: str = Field(
        ...,
        description=(
            'Primary contact person\'s full name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    client_company_name_address: str = Field(
        ...,
        description=(
            "Client or company name and full mailing address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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

    e_mail: str = Field(
        ...,
        description=(
            'Email address for the contact .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    reference_number: str = Field(
        default="",
        description=(
            "Client or project reference number, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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

    date_sampled: str = Field(
        ..., description="Date on which the samples were collected"
    )  # YYYY-MM-DD format

    client_site_same: BooleanLike = Field(
        default="", description="Indicate if the client address and site address are identical"
    )

    site_address: str = Field(
        ...,
        description=(
            'Physical address of the sampling site .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class LaboratoryUseOnly(BaseModel):
    """Fields completed by the laboratory upon receipt"""

    samples_received_proper_condition: BooleanLike = Field(
        default="",
        description="Lab confirmation that samples were received in acceptable condition",
    )

    laboratory_project_id: str = Field(
        default="",
        description=(
            "Identifier assigned by the laboratory for this project .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class TurnAroundTime(BaseModel):
    """Requested analysis turnaround time"""

    rush: BooleanLike = Field(default="", description="Select if rush turnaround is requested")

    under_24_hours_special_request: BooleanLike = Field(
        default="", description="Select if turnaround under 24 hours is specially requested"
    )

    twenty_four_hours: BooleanLike = Field(
        default="", description="Select if 24-hour turnaround is requested"
    )

    two_three_days: BooleanLike = Field(
        default="", description="Select if 2–3 day turnaround is requested"
    )

    four_plus_days: BooleanLike = Field(
        default="", description="Select if 4 or more day turnaround is acceptable"
    )


class ProjectComments(BaseModel):
    """Project identification and general comments"""

    acm_project_number: str = Field(
        default="",
        description=(
            "Internal ACM project number, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    comments: str = Field(
        default="",
        description=(
            "Additional notes or special instructions .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class RequestedAnalysisSummary(BaseModel):
    """Overall requested analysis types (checkbox list)"""

    asbestos_bulk_plm: BooleanLike = Field(
        default="", description="Request asbestos bulk analysis by PLM"
    )

    asbestos_point_count: BooleanLike = Field(
        default="", description="Request asbestos point count analysis"
    )

    fungi_spore_trap_analysis_air: BooleanLike = Field(
        default="", description="Request fungi spore trap analysis for air samples"
    )

    fungi_direct_examination_tape: BooleanLike = Field(
        default="", description="Request fungi direct examination of tape samples"
    )

    lead_paint_chip_analysis: BooleanLike = Field(
        default="", description="Request lead paint chip analysis"
    )

    c_of_c_with_pcb_caulk_sediment: BooleanLike = Field(
        default="", description="Request chain-of-custody with PCB analysis for caulk or sediment"
    )

    other_please_specify: str = Field(
        default="",
        description=(
            "Specify any other requested analysis not listed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SampleTable(BaseModel):
    """Per-sample information and analysis selections"""

    sample_table: List[SampleTableRow] = Field(
        ...,
        description=(
            "Table to record sample identifiers, descriptions, locations, materials, and "
            "requested analyses for each sample"
        ),
    )  # List of table rows

    sample_description_serial_number: str = Field(
        default="",
        description=(
            "Description of the sample and any serial or identification number .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    sample_location: str = Field(
        default="",
        description=(
            "Location where the sample was collected .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    area_volume_material: str = Field(
        default="",
        description=(
            "Area, volume, or material description associated with the sample .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    asbestos_bulk_plm_table_column: BooleanLike = Field(
        default="",
        description="Indicate for each sample if asbestos bulk (PLM) analysis is requested",
    )

    asbestos_point_count_table_column: BooleanLike = Field(
        default="",
        description="Indicate for each sample if asbestos point count analysis is requested",
    )

    fungi_spore_trap_analysis_air_table_column: BooleanLike = Field(
        default="",
        description="Indicate for each sample if fungi spore trap analysis (air) is requested",
    )

    fungi_direct_examination_tape_table_column: BooleanLike = Field(
        default="",
        description="Indicate for each sample if fungi direct examination (tape) is requested",
    )

    lead_paint_chip_analysis_table_column: BooleanLike = Field(
        default="", description="Indicate for each sample if lead paint chip analysis is requested"
    )

    c_of_c_with_pcb_caulk_sediment_table_column: BooleanLike = Field(
        default="",
        description=(
            "Indicate for each sample if C of C with PCB (caulk, sediment) analysis is requested"
        ),
    )

    other_please_specify_table_column: str = Field(
        default="",
        description=(
            "For each sample, specify any other requested analysis not listed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ChainofCustody(BaseModel):
    """Sample custody and processing information"""

    submitted_relinquished_by: str = Field(
        ...,
        description=(
            "Name of the person submitting or relinquishing the samples .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    submitted_relinquished_date_time: str = Field(
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
            "Name of the person receiving or accepting the samples .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    received_accepted_date_time: str = Field(
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
            "Name of the person who processed the samples in the lab .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    samples_processed_date_time: str = Field(
        default="",
        description=(
            "Date and time when samples were processed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AcmEnvServicesChainOfCustodyRequestForm(BaseModel):
    """
        ACM Engineering & Environmental Services, Inc.
    Chain-of-Custody / Analysis Request Form

        ''
    """

    client__contact__site_information: ClientContactSiteInformation = Field(
        ..., description="Client / Contact / Site Information"
    )
    laboratory_use_only: LaboratoryUseOnly = Field(..., description="Laboratory Use Only")
    turn_around_time: TurnAroundTime = Field(..., description="Turn Around Time")
    project__comments: ProjectComments = Field(..., description="Project & Comments")
    requested_analysis_summary: RequestedAnalysisSummary = Field(
        ..., description="Requested Analysis (Summary)"
    )
    sample_table: SampleTable = Field(..., description="Sample Table")
    chain_of_custody: ChainofCustody = Field(..., description="Chain of Custody")
