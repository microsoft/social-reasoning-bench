from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EmployeeandClientInformation(BaseModel):
    """Basic identifying information and week of service"""

    employee_name_please_print: str = Field(
        ...,
        description=(
            'Employee\'s full name, printed clearly .If you cannot fill this, write "N/A". '
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

    client_name_please_print: str = Field(
        ...,
        description=(
            'Client\'s full name, printed clearly .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
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

    sunday_start_week_mm: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month (MM) of the Sunday that started the work week"
    )

    sunday_start_week_dd: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day (DD) of the Sunday that started the work week"
    )

    sunday_start_week_yy: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year (YY) of the Sunday that started the work week"
    )


class ShiftTimeandServiceDetails(BaseModel):
    """Service dates, times, and shift numbers for each shift"""

    service_date_month_mm_shift_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Service date month (MM) for shift 1"
    )

    service_date_day_dd_shift_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Service date day (DD) for shift 1"
    )

    time_in_hour_hh_shift_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Time in hour (HH) for shift 1"
    )

    time_in_min_mm_shift_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Time in minutes (MM) for shift 1"
    )

    time_out_hour_hh_shift_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Time out hour (HH) for shift 1"
    )

    time_out_min_mm_shift_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Time out minutes (MM) for shift 1"
    )

    service_shift_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Service shift number for row 1 (usually 1)"
    )

    service_date_month_mm_shift_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Service date month (MM) for shift 2"
    )

    service_date_day_dd_shift_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Service date day (DD) for shift 2"
    )

    time_in_hour_hh_shift_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Time in hour (HH) for shift 2"
    )

    time_in_min_mm_shift_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Time in minutes (MM) for shift 2"
    )

    time_out_hour_hh_shift_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Time out hour (HH) for shift 2"
    )

    time_out_min_mm_shift_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Time out minutes (MM) for shift 2"
    )

    service_shift_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Service shift number for row 2 (usually 2)"
    )

    service_date_month_mm_shift_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Service date month (MM) for shift 3"
    )

    service_date_day_dd_shift_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Service date day (DD) for shift 3"
    )

    time_in_hour_hh_shift_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Time in hour (HH) for shift 3"
    )

    time_in_min_mm_shift_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Time in minutes (MM) for shift 3"
    )

    time_out_hour_hh_shift_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Time out hour (HH) for shift 3"
    )

    time_out_min_mm_shift_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Time out minutes (MM) for shift 3"
    )

    service_shift_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Service shift number for row 3 (usually 3)"
    )

    service_date_month_mm_shift_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Service date month (MM) for shift 4"
    )

    service_date_day_dd_shift_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Service date day (DD) for shift 4"
    )

    time_in_hour_hh_shift_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Time in hour (HH) for shift 4"
    )

    time_in_min_mm_shift_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Time in minutes (MM) for shift 4"
    )

    time_out_hour_hh_shift_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Time out hour (HH) for shift 4"
    )

    time_out_min_mm_shift_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Time out minutes (MM) for shift 4"
    )

    service_shift_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Service shift number for row 4 (usually 4)"
    )


class CaseNotes(BaseModel):
    """Client response to care for each shift"""

    case_notes_shift_1_client_response_g: BooleanLike = Field(
        default="", description="Mark if client response for shift 1 was Good (G)"
    )

    case_notes_shift_1_client_response_a: BooleanLike = Field(
        default="", description="Mark if client response for shift 1 was Average (A)"
    )

    case_notes_shift_1_client_response_p: BooleanLike = Field(
        default="", description="Mark if client response for shift 1 was Poor (P)"
    )

    case_notes_shift_2_client_response_g: BooleanLike = Field(
        default="", description="Mark if client response for shift 2 was Good (G)"
    )

    case_notes_shift_2_client_response_a: BooleanLike = Field(
        default="", description="Mark if client response for shift 2 was Average (A)"
    )

    case_notes_shift_2_client_response_p: BooleanLike = Field(
        default="", description="Mark if client response for shift 2 was Poor (P)"
    )

    case_notes_shift_3_client_response_g: BooleanLike = Field(
        default="", description="Mark if client response for shift 3 was Good (G)"
    )

    case_notes_shift_3_client_response_a: BooleanLike = Field(
        default="", description="Mark if client response for shift 3 was Average (A)"
    )

    case_notes_shift_3_client_response_p: BooleanLike = Field(
        default="", description="Mark if client response for shift 3 was Poor (P)"
    )

    case_notes_shift_4_client_response_g: BooleanLike = Field(
        default="", description="Mark if client response for shift 4 was Good (G)"
    )

    case_notes_shift_4_client_response_a: BooleanLike = Field(
        default="", description="Mark if client response for shift 4 was Average (A)"
    )

    case_notes_shift_4_client_response_p: BooleanLike = Field(
        default="", description="Mark if client response for shift 4 was Poor (P)"
    )


class EVVFVVCodes(BaseModel):
    """Electronic visit verification codes and related comments"""

    evv_fvv_code_shift_1_in: str = Field(
        default="",
        description=(
            "Eight-digit FVV code for electronic check-in for shift 1 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    evv_fvv_code_shift_1_out: str = Field(
        default="",
        description=(
            "Eight-digit FVV code for electronic check-out for shift 1 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    evv_fvv_code_shift_2_in: str = Field(
        default="",
        description=(
            "Eight-digit FVV code for electronic check-in for shift 2 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    evv_fvv_code_shift_2_out: str = Field(
        default="",
        description=(
            "Eight-digit FVV code for electronic check-out for shift 2 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    evv_fvv_code_shift_3_in: str = Field(
        default="",
        description=(
            "Eight-digit FVV code for electronic check-in for shift 3 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    evv_fvv_code_shift_3_out: str = Field(
        default="",
        description=(
            "Eight-digit FVV code for electronic check-out for shift 3 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    evv_fvv_code_shift_4_in: str = Field(
        default="",
        description=(
            "Eight-digit FVV code for electronic check-in for shift 4 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    evv_fvv_code_shift_4_out: str = Field(
        default="",
        description=(
            "Eight-digit FVV code for electronic check-out for shift 4 .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    evv_comments: str = Field(
        default="",
        description=(
            "Explanation if you were unable to electronically check in/out of a shift .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ServiceTypeandTasksbyShift(BaseModel):
    """CFC/PCS service selection and tasks performed for each shift"""

    cfc_shift_1: BooleanLike = Field(
        default="", description="Check if CFC service was provided during shift 1"
    )

    cfc_shift_2: BooleanLike = Field(
        default="", description="Check if CFC service was provided during shift 2"
    )

    cfc_shift_3: BooleanLike = Field(
        default="", description="Check if CFC service was provided during shift 3"
    )

    cfc_shift_4: BooleanLike = Field(
        default="", description="Check if CFC service was provided during shift 4"
    )

    pcs_shift_1: BooleanLike = Field(
        default="", description="Check if PCS service was provided during shift 1"
    )

    pcs_shift_2: BooleanLike = Field(
        default="", description="Check if PCS service was provided during shift 2"
    )

    pcs_shift_3: BooleanLike = Field(
        default="", description="Check if PCS service was provided during shift 3"
    )

    pcs_shift_4: BooleanLike = Field(
        default="", description="Check if PCS service was provided during shift 4"
    )

    positioning_shift_1: BooleanLike = Field(
        default="", description="Check if positioning task was performed during shift 1"
    )

    positioning_shift_2: BooleanLike = Field(
        default="", description="Check if positioning task was performed during shift 2"
    )

    positioning_shift_3: BooleanLike = Field(
        default="", description="Check if positioning task was performed during shift 3"
    )

    positioning_shift_4: BooleanLike = Field(
        default="", description="Check if positioning task was performed during shift 4"
    )

    prom_shift_1: BooleanLike = Field(
        default="", description="Check if PROM task was performed during shift 1"
    )

    prom_shift_2: BooleanLike = Field(
        default="", description="Check if PROM task was performed during shift 2"
    )

    prom_shift_3: BooleanLike = Field(
        default="", description="Check if PROM task was performed during shift 3"
    )

    prom_shift_4: BooleanLike = Field(
        default="", description="Check if PROM task was performed during shift 4"
    )

    transfer_shift_1: BooleanLike = Field(
        default="", description="Check if transfer task was performed during shift 1"
    )

    transfer_shift_2: BooleanLike = Field(
        default="", description="Check if transfer task was performed during shift 2"
    )

    transfer_shift_3: BooleanLike = Field(
        default="", description="Check if transfer task was performed during shift 3"
    )

    transfer_shift_4: BooleanLike = Field(
        default="", description="Check if transfer task was performed during shift 4"
    )

    locomote_single_shift_1: BooleanLike = Field(
        default="",
        description="Check if single-person locomotion assistance was provided during shift 1",
    )

    locomote_single_shift_2: BooleanLike = Field(
        default="",
        description="Check if single-person locomotion assistance was provided during shift 2",
    )

    locomote_single_shift_3: BooleanLike = Field(
        default="",
        description="Check if single-person locomotion assistance was provided during shift 3",
    )

    locomote_single_shift_4: BooleanLike = Field(
        default="",
        description="Check if single-person locomotion assistance was provided during shift 4",
    )

    locomote_multi_shift_1: BooleanLike = Field(
        default="",
        description="Check if multi-person locomotion assistance was provided during shift 1",
    )

    locomote_multi_shift_2: BooleanLike = Field(
        default="",
        description="Check if multi-person locomotion assistance was provided during shift 2",
    )

    locomote_multi_shift_3: BooleanLike = Field(
        default="",
        description="Check if multi-person locomotion assistance was provided during shift 3",
    )

    locomote_multi_shift_4: BooleanLike = Field(
        default="",
        description="Check if multi-person locomotion assistance was provided during shift 4",
    )

    locomote_med_shift_1: BooleanLike = Field(
        default="",
        description="Check if locomotion with medical equipment was provided during shift 1",
    )

    locomote_med_shift_2: BooleanLike = Field(
        default="",
        description="Check if locomotion with medical equipment was provided during shift 2",
    )

    locomote_med_shift_3: BooleanLike = Field(
        default="",
        description="Check if locomotion with medical equipment was provided during shift 3",
    )

    locomote_med_shift_4: BooleanLike = Field(
        default="",
        description="Check if locomotion with medical equipment was provided during shift 4",
    )

    dressing_shift_1: BooleanLike = Field(
        default="", description="Check if dressing assistance was provided during shift 1"
    )

    dressing_shift_2: BooleanLike = Field(
        default="", description="Check if dressing assistance was provided during shift 2"
    )

    dressing_shift_3: BooleanLike = Field(
        default="", description="Check if dressing assistance was provided during shift 3"
    )

    dressing_shift_4: BooleanLike = Field(
        default="", description="Check if dressing assistance was provided during shift 4"
    )

    eating_shift_1: BooleanLike = Field(
        default="", description="Check if eating assistance was provided during shift 1"
    )

    eating_shift_2: BooleanLike = Field(
        default="", description="Check if eating assistance was provided during shift 2"
    )

    eating_shift_3: BooleanLike = Field(
        default="", description="Check if eating assistance was provided during shift 3"
    )

    eating_shift_4: BooleanLike = Field(
        default="", description="Check if eating assistance was provided during shift 4"
    )

    toileting_shift_1: BooleanLike = Field(
        default="", description="Check if toileting assistance was provided during shift 1"
    )

    toileting_shift_2: BooleanLike = Field(
        default="", description="Check if toileting assistance was provided during shift 2"
    )

    toileting_shift_3: BooleanLike = Field(
        default="", description="Check if toileting assistance was provided during shift 3"
    )

    toileting_shift_4: BooleanLike = Field(
        default="", description="Check if toileting assistance was provided during shift 4"
    )

    hygiene_shift_1: BooleanLike = Field(
        default="", description="Check if hygiene assistance was provided during shift 1"
    )

    hygiene_shift_2: BooleanLike = Field(
        default="", description="Check if hygiene assistance was provided during shift 2"
    )

    hygiene_shift_3: BooleanLike = Field(
        default="", description="Check if hygiene assistance was provided during shift 3"
    )

    hygiene_shift_4: BooleanLike = Field(
        default="", description="Check if hygiene assistance was provided during shift 4"
    )

    bathing_shift_1: BooleanLike = Field(
        default="", description="Check if bathing assistance was provided during shift 1"
    )

    bathing_shift_2: BooleanLike = Field(
        default="", description="Check if bathing assistance was provided during shift 2"
    )

    bathing_shift_3: BooleanLike = Field(
        default="", description="Check if bathing assistance was provided during shift 3"
    )

    bathing_shift_4: BooleanLike = Field(
        default="", description="Check if bathing assistance was provided during shift 4"
    )

    light_meal_shift_1: BooleanLike = Field(
        default="",
        description="Check if light meal preparation/assistance was provided during shift 1",
    )

    light_meal_shift_2: BooleanLike = Field(
        default="",
        description="Check if light meal preparation/assistance was provided during shift 2",
    )

    light_meal_shift_3: BooleanLike = Field(
        default="",
        description="Check if light meal preparation/assistance was provided during shift 3",
    )

    light_meal_shift_4: BooleanLike = Field(
        default="",
        description="Check if light meal preparation/assistance was provided during shift 4",
    )

    main_meal_shift_1: BooleanLike = Field(
        default="",
        description="Check if main meal preparation/assistance was provided during shift 1",
    )

    main_meal_shift_2: BooleanLike = Field(
        default="",
        description="Check if main meal preparation/assistance was provided during shift 2",
    )

    main_meal_shift_3: BooleanLike = Field(
        default="",
        description="Check if main meal preparation/assistance was provided during shift 3",
    )

    main_meal_shift_4: BooleanLike = Field(
        default="",
        description="Check if main meal preparation/assistance was provided during shift 4",
    )

    housework_shift_1: BooleanLike = Field(
        default="", description="Check if housework assistance was provided during shift 1"
    )

    housework_shift_2: BooleanLike = Field(
        default="", description="Check if housework assistance was provided during shift 2"
    )

    housework_shift_3: BooleanLike = Field(
        default="", description="Check if housework assistance was provided during shift 3"
    )

    housework_shift_4: BooleanLike = Field(
        default="", description="Check if housework assistance was provided during shift 4"
    )

    shopping_shift_1: BooleanLike = Field(
        default="", description="Check if shopping assistance was provided during shift 1"
    )

    shopping_shift_2: BooleanLike = Field(
        default="", description="Check if shopping assistance was provided during shift 2"
    )

    shopping_shift_3: BooleanLike = Field(
        default="", description="Check if shopping assistance was provided during shift 3"
    )

    shopping_shift_4: BooleanLike = Field(
        default="", description="Check if shopping assistance was provided during shift 4"
    )

    laundry_shift_1: BooleanLike = Field(
        default="", description="Check if laundry assistance was provided during shift 1"
    )

    laundry_shift_2: BooleanLike = Field(
        default="", description="Check if laundry assistance was provided during shift 2"
    )

    laundry_shift_3: BooleanLike = Field(
        default="", description="Check if laundry assistance was provided during shift 3"
    )

    laundry_shift_4: BooleanLike = Field(
        default="", description="Check if laundry assistance was provided during shift 4"
    )

    wound_care_shift_1: BooleanLike = Field(
        default="", description="Check if wound care was provided during shift 1"
    )

    wound_care_shift_2: BooleanLike = Field(
        default="", description="Check if wound care was provided during shift 2"
    )

    wound_care_shift_3: BooleanLike = Field(
        default="", description="Check if wound care was provided during shift 3"
    )

    wound_care_shift_4: BooleanLike = Field(
        default="", description="Check if wound care was provided during shift 4"
    )

    oxygen_maint_shift_1: BooleanLike = Field(
        default="", description="Check if oxygen maintenance was provided during shift 1"
    )

    oxygen_maint_shift_2: BooleanLike = Field(
        default="", description="Check if oxygen maintenance was provided during shift 2"
    )

    oxygen_maint_shift_3: BooleanLike = Field(
        default="", description="Check if oxygen maintenance was provided during shift 3"
    )

    oxygen_maint_shift_4: BooleanLike = Field(
        default="", description="Check if oxygen maintenance was provided during shift 4"
    )

    escort_shift_1: BooleanLike = Field(
        default="", description="Check if escort services were provided during shift 1"
    )

    escort_shift_2: BooleanLike = Field(
        default="", description="Check if escort services were provided during shift 2"
    )

    escort_shift_3: BooleanLike = Field(
        default="", description="Check if escort services were provided during shift 3"
    )

    escort_shift_4: BooleanLike = Field(
        default="", description="Check if escort services were provided during shift 4"
    )

    medication_shift_1: BooleanLike = Field(
        default="", description="Check if medication assistance was provided during shift 1"
    )

    medication_shift_2: BooleanLike = Field(
        default="", description="Check if medication assistance was provided during shift 2"
    )

    medication_shift_3: BooleanLike = Field(
        default="", description="Check if medication assistance was provided during shift 3"
    )

    medication_shift_4: BooleanLike = Field(
        default="", description="Check if medication assistance was provided during shift 4"
    )


class ClientConditionNotes(BaseModel):
    """Narrative description of changes in client condition"""

    describe_any_change_improvement_or_decline: str = Field(
        default="",
        description=(
            "Narrative description of any changes in the client's health, safety, welfare, "
            'or physical/mental condition .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class SignaturesandDates(BaseModel):
    """Certification signatures and dates for employee and client/representative"""

    employee_signature: str = Field(
        ...,
        description=(
            "Employee's signature certifying the accuracy of the timesheet .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    employee_signature_date_mm: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month (MM) of employee signature date"
    )

    employee_signature_date_dd: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day (DD) of employee signature date"
    )

    employee_signature_date_yy: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year (YY) of employee signature date"
    )

    client_representative_signature: str = Field(
        ...,
        description=(
            "Signature of client or authorized representative .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    client_representative_signature_date_mm: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month (MM) of client/representative signature date"
    )

    client_representative_signature_date_dd: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day (DD) of client/representative signature date"
    )

    client_representative_signature_date_yy: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year (YY) of client/representative signature date"
    )


class ConsumerDirectCareNetworkAlaskaCfcAndPcsTimesheet(BaseModel):
    """
        CONSUMER DIRECT CARE NETWORK

    Alaska
    CFC and PCS Timesheet

        For the week of service, timesheets are due the following Monday by 5:00pm if faxed or dropped off, and postmarked by Monday if mailed. Timesheets are due every week. Due to the timing of the payroll cycle, late timesheets will result in late pay. Timesheets must be signed AFTER all work is completed. Advance timesheets will not be accepted.
    """

    employee_and_client_information: EmployeeandClientInformation = Field(
        ..., description="Employee and Client Information"
    )
    shift_time_and_service_details: ShiftTimeandServiceDetails = Field(
        ..., description="Shift Time and Service Details"
    )
    case_notes: CaseNotes = Field(..., description="Case Notes")
    evv__fvv_codes: EVVFVVCodes = Field(..., description="EVV / FVV Codes")
    service_type_and_tasks_by_shift: ServiceTypeandTasksbyShift = Field(
        ..., description="Service Type and Tasks by Shift"
    )
    client_condition_notes: ClientConditionNotes = Field(..., description="Client Condition Notes")
    signatures_and_dates: SignaturesandDates = Field(..., description="Signatures and Dates")
