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


class ClientContactSiteInformation(BaseModel):
    """Client, contact, and sampling site details"""

    contact: str = Field(
        ...,
        description=(
            "Primary contact person's name for this project or submission .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    client_company_name_address: str = Field(
        ...,
        description=(
            "Client or company name along with full mailing address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Primary phone number for the contact or client .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            'Email address for the primary contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reference_number: str = Field(
        default="",
        description=(
            "Client or project reference number associated with this submission .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    sampled_by: str = Field(
        ...,
        description=(
            "Name of the person or organization that collected the samples .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    client_site_address_same: BooleanLike = Field(
        default="", description="Indicate if the client address and the site address are identical"
    )

    date_sampled: str = Field(
        ..., description="Calendar date on which the samples were collected"
    )  # YYYY-MM-DD format

    site_address: str = Field(
        ...,
        description=(
            'Physical address of the sampling site .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class LaboratoryUseOnly(BaseModel):
    """Laboratory receipt and project identifiers"""

    samples_received_proper_condition: BooleanLike = Field(
        default="",
        description="Laboratory confirmation that samples were received in acceptable condition",
    )

    laboratory_project_id: str = Field(
        default="",
        description=(
            "Identifier assigned by the laboratory for this project .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    acm_project_number: str = Field(
        default="",
        description=(
            "Internal ACM project number associated with this work .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class TurnaroundTime(BaseModel):
    """Requested analysis turnaround time"""

    rush: BooleanLike = Field(default="", description="Select if rush turnaround is requested")

    under_24_hours_special_request: BooleanLike = Field(
        default="", description="Indicate if a special turnaround of under 24 hours is requested"
    )

    turnaround_24_hours: BooleanLike = Field(
        default="", description="Select if a 24-hour turnaround time is requested"
    )

    turnaround_2_3_days: BooleanLike = Field(
        default="", description="Select if a 2–3 day turnaround time is requested"
    )

    turnaround_4_plus_days: BooleanLike = Field(
        default="", description="Select if a 4 or more day turnaround time is acceptable"
    )


class Comments(BaseModel):
    """Additional notes or instructions"""

    comments: str = Field(
        default="",
        description=(
            "Additional notes or special instructions related to the samples or analysis "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class RequestedAnalysis(BaseModel):
    """Types of analyses requested for samples"""

    asbestos_bulk_plm: BooleanLike = Field(
        default="", description="Request analysis for asbestos bulk samples using PLM"
    )

    asbestos_point_count: BooleanLike = Field(
        default="", description="Request asbestos point count analysis"
    )

    fungal_spore_trap_analysis: BooleanLike = Field(
        default="", description="Request fungal spore trap analysis"
    )

    fungal_direct_examination_tape: BooleanLike = Field(
        default="", description="Request fungal direct examination using tape lift samples"
    )

    lead_pb_tclp: BooleanLike = Field(default="", description="Request TCLP analysis for lead (Pb)")

    cyanide_tclp: BooleanLike = Field(default="", description="Request TCLP analysis for cyanide")

    ph_corrosivity: BooleanLike = Field(default="", description="Request pH corrosivity analysis")

    other_please_specify: str = Field(
        default="",
        description=(
            "Specify any other requested analyses not listed above .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SampleInformationChainofCustody(BaseModel):
    """Sample identifiers and chain-of-custody details"""

    sample_table: List[SampleTableRow] = Field(
        ...,
        description=(
            "Table for listing each sample, its description/serial number, location, and "
            "area/volume/material"
        ),
    )  # List of table rows

    submitted_relinquished_by: str = Field(
        ...,
        description=(
            "Name of the person submitting or relinquishing custody of the samples .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
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
            "Name of the person receiving or accepting the samples at the laboratory .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    received_accepted_date_time: str = Field(
        ...,
        description=(
            "Date and time when samples were received or accepted by the laboratory .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    samples_processed_by: str = Field(
        default="",
        description=(
            "Name of the laboratory staff member who processed the samples .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    samples_processed_date_time: str = Field(
        default="",
        description=(
            "Date and time when the samples were processed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AcmEngEnvServicesChainOfCustodyAnalysisRequestForm(BaseModel):
    """
        ACM Engineering & Environmental Services, Inc.
    Chain-of-Custody / Analysis Request Form

        ''
    """

    client__contact__site_information: ClientContactSiteInformation = Field(
        ..., description="Client / Contact / Site Information"
    )
    laboratory_use_only: LaboratoryUseOnly = Field(..., description="Laboratory Use Only")
    turnaround_time: TurnaroundTime = Field(..., description="Turnaround Time")
    comments: Comments = Field(..., description="Comments")
    requested_analysis: RequestedAnalysis = Field(..., description="Requested Analysis")
    sample_information__chain_of_custody: SampleInformationChainofCustody = Field(
        ..., description="Sample Information & Chain of Custody"
    )
