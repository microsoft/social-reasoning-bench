from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class SampleTableRow(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Single row in SAMPLE ID"""

    sample_id: str = Field(
        ...,
        description="Sample_Id"
    )
    sample_description_serial_number: str = Field(
        ...,
        description="Sample_Description_Serial_Number"
    )
    sample_location: str = Field(
        ...,
        description="Sample_Location"
    )
    area_volume_material: str = Field(
        ...,
        description="Area_Volume_Material"
    )
    asbestos_bulk_plm: str = Field(
        ...,
        description="Asbestos_Bulk_Plm"
    )
    asbestos_point_count: str = Field(
        ...,
        description="Asbestos_Point_Count"
    )
    fungal_spore_trap_analysis_air: str = Field(
        ...,
        description="Fungal_Spore_Trap_Analysis_Air"
    )
    fungal_bulk_examination_tape: str = Field(
        ...,
        description="Fungal_Bulk_Examination_Tape"
    )
    lead_in_paint_cpl: str = Field(
        ...,
        description="Lead_In_Paint_Cpl"
    )
    lead_in_paint_xrf_confirmation: str = Field(
        ...,
        description="Lead_In_Paint_Xrf_Confirmation"
    )
    other_please_specify: str = Field(
        ...,
        description="Other_Please_Specify"
    )


class ClientContactSiteInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about the client, contact person, and site location."""

    contact: str = Field(
        ...,
        description=(
            "Name of the primary contact person .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    client_company_name_address: str = Field(
        ...,
        description=(
            "Full name and address of the client or company .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    phone: str = Field(
        ...,
        description=(
            "Contact phone number .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    e_mail: str = Field(
        ...,
        description=(
            "Contact email address .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    reference_number: str = Field(
        ...,
        description=(
            "Reference number for this request (if applicable) .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    sampled_by: str = Field(
        ...,
        description=(
            "Name of the person who collected the sample(s) .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    date_sampled: str = Field(
        ...,
        description="Date when the sample(s) were collected"
    )  # YYYY-MM-DD format

    client_site_address_same: BooleanLike = Field(
        ...,
        description="Check if the client and site address are the same"
    )

    site_address: str = Field(
        ...,
        description=(
            "Address where the sample(s) were collected .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )


class LaboratoryUseOnly(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Fields to be completed by laboratory staff."""

    samples_received_proper_condition: BooleanLike = Field(
        ...,
        description="Indicate if samples were received in proper condition (lab use only)"
    )

    laboratory_project_id: str = Field(
        ...,
        description=(
            "Laboratory project identification number (lab use only) .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )


class TurnAroundTime(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Requested time frame for analysis completion."""

    turn_around_time: Literal["RUSH", "24 Hours", "2 - 3 Days", "4+ Days", "N/A", ""] = Field(
        ...,
        description="Select the required analysis turn around time"
    )

    rush: BooleanLike = Field(
        ...,
        description="Check if rush (under 24 hours) is requested"
    )

    field_24_hours: BooleanLike = Field(
        ...,
        description="Check if 24 hour turn around is requested"
    )

    field_2_3_days: BooleanLike = Field(
        ...,
        description="Check if 2-3 day turn around is requested"
    )

    field_4_days: BooleanLike = Field(
        ...,
        description="Check if 4 or more day turn around is requested"
    )


class Comments(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Additional comments or notes."""

    comments: str = Field(
        ...,
        description=(
            "Additional comments or instructions .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class RequestedAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Types of analysis requested and project number."""

    requested_analysis: Literal["Asbestos Bulk (PLM)", "Asbestos Point Count", "Fungal Spore Trap Analysis (Air)", "Fungal Bulk Examination (Tape)", "Lead in Paint (CPL)", "Lead in Paint (XRF Confirmation)", "Other Please Specify", "N/A", ""] = Field(
        ...,
        description="Select the type(s) of analysis requested"
    )

    acm_project_number: str = Field(
        ...,
        description=(
            "Project number assigned by ACM .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class SampleTable(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Details for each sample submitted."""

    sample_table: List[SampleTableRow] = Field(
        ...,
        description="Table to record sample details and requested analyses"
    )  # List of table rows


class ChainofCustody(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Tracking of sample handling and processing."""

    submitted_relinquished_by: str = Field(
        ...,
        description=(
            "Name of person submitting or relinquishing samples .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    date_time_submitted_relinquished: str = Field(
        ...,
        description=(
            "Date and time when samples were submitted or relinquished .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    received_accepted_by: str = Field(
        ...,
        description=(
            "Name of person receiving or accepting samples .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    date_time_received_accepted: str = Field(
        ...,
        description=(
            "Date and time when samples were received or accepted .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    samples_processed_by: str = Field(
        ...,
        description=(
            "Name of person who processed the samples .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    date_time_samples_processed: str = Field(
        ...,
        description=(
            "Date and time when samples were processed .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )


class ChainofcustodyAnalysisRequestForm(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    Chain-of-Custody / Analysis Request Form

    Chain-of-Custody / Analysis Request Form for submitting environmental samples to ACM Engineering & Environmental Services, Inc. Includes client, contact, and site information, requested analyses (such as asbestos, fungal, and lead testing), sample details, and documentation of sample handling and processing for laboratory analysis. Used to ensure proper tracking and analysis of samples from collection through laboratory processing.
    """

    client__contact__site_information: ClientContactSiteInformation = Field(
        ...,
        description="Client / Contact / Site Information"
    )
    laboratory_use_only: LaboratoryUseOnly = Field(
        ...,
        description="Laboratory Use Only"
    )
    turn_around_time: TurnAroundTime = Field(
        ...,
        description="Turn Around Time"
    )
    comments: Comments = Field(
        ...,
        description="Comments"
    )
    requested_analysis: RequestedAnalysis = Field(
        ...,
        description="Requested Analysis"
    )
    sample_table: SampleTable = Field(
        ...,
        description="Sample Table"
    )
    chain_of_custody: ChainofCustody = Field(
        ...,
        description="Chain of Custody"
    )