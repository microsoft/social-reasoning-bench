from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PermitSummaryTableRow(BaseModel):
    """Single row in PERMIT SUMMARY      * Workload to Date"""

    measure_description: str = Field(default="", description="Measure_Description")
    received_month: str = Field(default="", description="Received_Month")
    pending: str = Field(default="", description="Pending")
    approved: str = Field(default="", description="Approved")


class ExecutiveSummary(BaseModel):
    """High-level monthly summary and interdepartmental activity"""

    executive_summary: str = Field(
        default="",
        description=(
            "Brief narrative summary of key activities, issues, and accomplishments for the "
            'month .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    interdepartmental_activity: str = Field(
        default="",
        description=(
            "Description of coordination, projects, or interactions with other departments "
            'during the month .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class StaffReport(BaseModel):
    """Staffing levels and needs for the reporting period"""

    total_staff: str = Field(
        default="",
        description=(
            "Summary of total staff for the reporting period (counts, classifications, or "
            'explanation as needed) .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    staffing_needs: str = Field(
        default="",
        description=(
            "Description of current or anticipated staffing needs, vacancies, or resource "
            'gaps .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class PermitSummary(BaseModel):
    """Summary of permit workload and status for the month"""

    permit_summary_table: List[PermitSummaryTableRow] = Field(
        default="",
        description=(
            "Monthly permit workload summary including measure description, number "
            "received, pending, and approved"
        ),
    )  # List of table rows


class PublicWorksDepartmentMonthlyReport(BaseModel):
    """
        Public Works Department

    Monthly Report

        ''
    """

    executive_summary: ExecutiveSummary = Field(..., description="Executive Summary")
    staff_report: StaffReport = Field(..., description="Staff Report")
    permit_summary: PermitSummary = Field(..., description="Permit Summary")
