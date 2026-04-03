from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class TimesheetHeader(BaseModel):
    """Week and participant/employee identifiers"""

    sunday_that_started_your_work_week: str = Field(
        ..., description="Sunday date that begins the work week for this timesheet"
    )  # YYYY-MM-DD format

    employee_name: str = Field(
        ...,
        description=(
            'Employee\'s full name (print clearly) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    employee_id: str = Field(
        ...,
        description=(
            "Unique ID number assigned to the employee .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    client_name: str = Field(
        ...,
        description=(
            'Client\'s full name (print clearly) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    client_id: str = Field(
        ...,
        description=(
            "Unique ID number assigned to the client .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ServiceDatesandTimes(BaseModel):
    """Daily service dates and time in/out for each shift"""

    service_date_1_month_mm: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month (two digits) for service date 1"
    )

    service_date_1_day_dd: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day (two digits) for service date 1"
    )

    service_date_1_time_in_hour_hh: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Hour (two digits) for time in on service date 1"
    )

    service_date_1_time_in_min_mm: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Minutes (two digits) for time in on service date 1"
    )

    service_date_1_time_in_am: BooleanLike = Field(
        ..., description="Check if time in on service date 1 is AM"
    )

    service_date_1_time_in_pm: BooleanLike = Field(
        ..., description="Check if time in on service date 1 is PM"
    )

    service_date_1_time_out_hour_hh: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Hour (two digits) for time out on service date 1"
    )

    service_date_1_time_out_min_mm: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Minutes (two digits) for time out on service date 1"
    )

    service_date_1_time_out_am: BooleanLike = Field(
        ..., description="Check if time out on service date 1 is AM"
    )

    service_date_1_time_out_pm: BooleanLike = Field(
        ..., description="Check if time out on service date 1 is PM"
    )

    service_date_2_month_mm: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month (two digits) for service date 2"
    )

    service_date_2_day_dd: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day (two digits) for service date 2"
    )

    service_date_2_time_in_hour_hh: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Hour (two digits) for time in on service date 2"
    )

    service_date_2_time_in_min_mm: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minutes (two digits) for time in on service date 2"
    )

    service_date_2_time_in_am: BooleanLike = Field(
        default="", description="Check if time in on service date 2 is AM"
    )

    service_date_2_time_in_pm: BooleanLike = Field(
        default="", description="Check if time in on service date 2 is PM"
    )

    service_date_2_time_out_hour_hh: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Hour (two digits) for time out on service date 2"
    )

    service_date_2_time_out_min_mm: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minutes (two digits) for time out on service date 2"
    )

    service_date_2_time_out_am: BooleanLike = Field(
        default="", description="Check if time out on service date 2 is AM"
    )

    service_date_2_time_out_pm: BooleanLike = Field(
        default="", description="Check if time out on service date 2 is PM"
    )

    service_date_3_month_mm: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month (two digits) for service date 3"
    )

    service_date_3_day_dd: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day (two digits) for service date 3"
    )

    service_date_3_time_in_hour_hh: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Hour (two digits) for time in on service date 3"
    )

    service_date_3_time_in_min_mm: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minutes (two digits) for time in on service date 3"
    )

    service_date_3_time_in_am: BooleanLike = Field(
        default="", description="Check if time in on service date 3 is AM"
    )

    service_date_3_time_in_pm: BooleanLike = Field(
        default="", description="Check if time in on service date 3 is PM"
    )

    service_date_3_time_out_hour_hh: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Hour (two digits) for time out on service date 3"
    )

    service_date_3_time_out_min_mm: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minutes (two digits) for time out on service date 3"
    )

    service_date_3_time_out_am: BooleanLike = Field(
        default="", description="Check if time out on service date 3 is AM"
    )

    service_date_3_time_out_pm: BooleanLike = Field(
        default="", description="Check if time out on service date 3 is PM"
    )

    service_date_4_month_mm: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month (two digits) for service date 4"
    )

    service_date_4_day_dd: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day (two digits) for service date 4"
    )

    service_date_4_time_in_hour_hh: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Hour (two digits) for time in on service date 4"
    )

    service_date_4_time_in_min_mm: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minutes (two digits) for time in on service date 4"
    )

    service_date_4_time_in_am: BooleanLike = Field(
        default="", description="Check if time in on service date 4 is AM"
    )

    service_date_4_time_in_pm: BooleanLike = Field(
        default="", description="Check if time in on service date 4 is PM"
    )

    service_date_4_time_out_hour_hh: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Hour (two digits) for time out on service date 4"
    )

    service_date_4_time_out_min_mm: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minutes (two digits) for time out on service date 4"
    )

    service_date_4_time_out_am: BooleanLike = Field(
        default="", description="Check if time out on service date 4 is AM"
    )

    service_date_4_time_out_pm: BooleanLike = Field(
        default="", description="Check if time out on service date 4 is PM"
    )


class CaseNotes(BaseModel):
    """Client response notes for each shift"""

    case_notes_shift_1_client_response: str = Field(
        ...,
        description=(
            "Brief note describing client response to care for shift 1 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    case_notes_shift_2_client_response: str = Field(
        ...,
        description=(
            "Brief note describing client response to care for shift 2 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    case_notes_shift_3_client_response: str = Field(
        ...,
        description=(
            "Brief note describing client response to care for shift 3 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    case_notes_shift_4_client_response: str = Field(
        ...,
        description=(
            "Brief note describing client response to care for shift 4 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    case_notes_shift_1_g: BooleanLike = Field(
        ..., description="Mark if client response for shift 1 was Good (G)"
    )

    case_notes_shift_1_a: BooleanLike = Field(
        ..., description="Mark if client response for shift 1 was Average (A)"
    )

    case_notes_shift_1_p: BooleanLike = Field(
        ..., description="Mark if client response for shift 1 was Poor (P)"
    )

    case_notes_shift_2_g: BooleanLike = Field(
        ..., description="Mark if client response for shift 2 was Good (G)"
    )

    case_notes_shift_2_a: BooleanLike = Field(
        ..., description="Mark if client response for shift 2 was Average (A)"
    )

    case_notes_shift_2_p: BooleanLike = Field(
        ..., description="Mark if client response for shift 2 was Poor (P)"
    )

    case_notes_shift_3_g: BooleanLike = Field(
        ..., description="Mark if client response for shift 3 was Good (G)"
    )

    case_notes_shift_3_a: BooleanLike = Field(
        ..., description="Mark if client response for shift 3 was Average (A)"
    )

    case_notes_shift_3_p: BooleanLike = Field(
        ..., description="Mark if client response for shift 3 was Poor (P)"
    )

    case_notes_shift_4_g: BooleanLike = Field(
        ..., description="Mark if client response for shift 4 was Good (G)"
    )

    case_notes_shift_4_a: BooleanLike = Field(
        ..., description="Mark if client response for shift 4 was Average (A)"
    )

    case_notes_shift_4_p: BooleanLike = Field(
        ..., description="Mark if client response for shift 4 was Poor (P)"
    )


class EVVCodesandComments(BaseModel):
    """Electronic visit verification codes and related comments"""

    shift_1_evv_in_code: str = Field(
        default="",
        description=(
            "Eight-digit EVV code for check-in on shift 1 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    shift_1_evv_out_code: str = Field(
        default="",
        description=(
            "Eight-digit EVV code for check-out on shift 1 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    shift_2_evv_in_code: str = Field(
        default="",
        description=(
            "Eight-digit EVV code for check-in on shift 2 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    shift_2_evv_out_code: str = Field(
        default="",
        description=(
            "Eight-digit EVV code for check-out on shift 2 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    shift_3_evv_in_code: str = Field(
        default="",
        description=(
            "Eight-digit EVV code for check-in on shift 3 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    shift_3_evv_out_code: str = Field(
        default="",
        description=(
            "Eight-digit EVV code for check-out on shift 3 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    shift_4_evv_in_code: str = Field(
        default="",
        description=(
            "Eight-digit EVV code for check-in on shift 4 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    shift_4_evv_out_code: str = Field(
        default="",
        description=(
            "Eight-digit EVV code for check-out on shift 4 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    evv_comments_line_1: str = Field(
        default="",
        description=(
            "First line explaining why EVV check in/out could not be completed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    evv_comments_line_2: str = Field(
        default="",
        description=(
            "Second line explaining why EVV check in/out could not be completed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    evv_comments_line_3: str = Field(
        default="",
        description=(
            "Third line explaining why EVV check in/out could not be completed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    evv_comments_line_4: str = Field(
        default="",
        description=(
            "Fourth line explaining why EVV check in/out could not be completed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ServiceSelection(BaseModel):
    """CFC/PCS service type selection by shift"""

    service_cfc_shift_1: BooleanLike = Field(
        default="", description="Check if CFC services were provided during shift 1"
    )

    service_cfc_shift_2: BooleanLike = Field(
        default="", description="Check if CFC services were provided during shift 2"
    )

    service_cfc_shift_3: BooleanLike = Field(
        default="", description="Check if CFC services were provided during shift 3"
    )

    service_cfc_shift_4: BooleanLike = Field(
        default="", description="Check if CFC services were provided during shift 4"
    )

    service_pcs_shift_1: BooleanLike = Field(
        default="", description="Check if PCS services were provided during shift 1"
    )

    service_pcs_shift_2: BooleanLike = Field(
        default="", description="Check if PCS services were provided during shift 2"
    )

    service_pcs_shift_3: BooleanLike = Field(
        default="", description="Check if PCS services were provided during shift 3"
    )

    service_pcs_shift_4: BooleanLike = Field(
        default="", description="Check if PCS services were provided during shift 4"
    )


class TasksPerformed(BaseModel):
    """Tasks completed during the week"""

    tasks_positioning: BooleanLike = Field(
        default="", description="Check if positioning task was performed"
    )

    tasks_prom: BooleanLike = Field(
        default="",
        description="Indicate if PROM (passive range of motion) task applies (marked with — on form)",
    )

    tasks_transfer: BooleanLike = Field(
        default="", description="Check if transfer task was performed"
    )

    tasks_locomote_single: BooleanLike = Field(
        default="", description="Check if single-person locomotion assistance was provided"
    )

    tasks_locomote_multi: BooleanLike = Field(
        default="", description="Check if multi-person locomotion assistance was provided"
    )

    tasks_locomote_med: BooleanLike = Field(
        default="", description="Check if locomotion with medical equipment assistance was provided"
    )

    tasks_dressing: BooleanLike = Field(
        default="", description="Check if dressing assistance was provided"
    )

    tasks_eating: BooleanLike = Field(
        default="", description="Check if eating assistance was provided"
    )

    tasks_toileting: BooleanLike = Field(
        default="", description="Check if toileting assistance was provided"
    )

    tasks_hygiene: BooleanLike = Field(
        default="", description="Check if personal hygiene assistance was provided"
    )

    tasks_bathing: BooleanLike = Field(
        default="", description="Check if bathing assistance was provided"
    )

    tasks_light_meal: BooleanLike = Field(
        default="", description="Check if light meal preparation was provided"
    )

    tasks_main_meal: BooleanLike = Field(
        default="", description="Check if main meal preparation was provided"
    )

    tasks_housework: BooleanLike = Field(
        default="", description="Check if housework tasks were performed"
    )

    tasks_shopping: BooleanLike = Field(
        default="", description="Check if shopping assistance was provided"
    )

    tasks_laundry: BooleanLike = Field(
        default="", description="Check if laundry tasks were performed"
    )

    tasks_wound_care: BooleanLike = Field(
        default="", description="Indicate if wound care task applies (marked with — on form)"
    )

    tasks_oxygen_maint: BooleanLike = Field(
        default="",
        description="Indicate if oxygen maintenance task applies (marked with — on form)",
    )

    tasks_escort: BooleanLike = Field(
        default="", description="Indicate if escort task applies (marked with — on form)"
    )

    tasks_medication: BooleanLike = Field(
        default="", description="Indicate if medication task applies (marked with — on form)"
    )


class ClientConditionChanges(BaseModel):
    """Narrative description of changes in client condition"""

    describe_change_in_clients_condition_line_1: str = Field(
        default="",
        description=(
            "First line describing any change, improvement, or decline in client's "
            'condition .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    describe_change_in_clients_condition_line_2: str = Field(
        default="",
        description=(
            "Second line describing any change, improvement, or decline in client's "
            'condition .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    describe_change_in_clients_condition_line_3: str = Field(
        default="",
        description=(
            "Third line describing any change, improvement, or decline in client's "
            'condition .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    describe_change_in_clients_condition_line_4: str = Field(
        default="",
        description=(
            "Fourth line describing any change, improvement, or decline in client's "
            'condition .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class Signatures(BaseModel):
    """Employee and client/representative signatures and dates"""

    employee_signature: str = Field(
        ...,
        description=(
            "Employee's handwritten or electronic signature certifying the timesheet .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    employee_signature_date_month_mm: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month (two digits) of employee signature date"
    )

    employee_signature_date_day_dd: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day (two digits) of employee signature date"
    )

    employee_signature_date_year_yy: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year (two digits) of employee signature date"
    )

    client_representative_signature: str = Field(
        ...,
        description=(
            "Signature of client or authorized representative .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    client_representative_signature_date_month_mm: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month (two digits) of client/representative signature date"
    )

    client_representative_signature_date_day_dd: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day (two digits) of client/representative signature date"
    )

    client_representative_signature_date_year_yy: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year (two digits) of client/representative signature date"
    )


class ConsumerDirectCareNetworkAlaskaCfcAndPcsTimesheet(BaseModel):
    """
        CONSUMER DIRECT
    CARE NETWORK

    Alaska
    CFC and PCS Timesheet

        For the week of service, timesheets are due the following Monday by 5:00pm if faxed or dropped off, and postmarked by Monday if mailed. Timesheets are due every week. Due to the timing of the payroll cycle, late timesheets will result in late pay. Timesheets must be signed AFTER all work is completed. Advance timesheets will not be accepted.
    """

    timesheet_header: TimesheetHeader = Field(..., description="Timesheet Header")
    service_dates_and_times: ServiceDatesandTimes = Field(
        ..., description="Service Dates and Times"
    )
    case_notes: CaseNotes = Field(..., description="Case Notes")
    evv_codes_and_comments: EVVCodesandComments = Field(..., description="EVV Codes and Comments")
    service_selection: ServiceSelection = Field(..., description="Service Selection")
    tasks_performed: TasksPerformed = Field(..., description="Tasks Performed")
    client_condition_changes: ClientConditionChanges = Field(
        ..., description="Client Condition Changes"
    )
    signatures: Signatures = Field(..., description="Signatures")
