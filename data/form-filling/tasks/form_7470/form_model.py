from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class WeekParticipantInformation(BaseModel):
    """Week start date, employee, and client identifiers"""

    sunday_that_started_your_work_week: str = Field(
        ..., description="Sunday date that begins the work week (MM/DD/YY)"
    )  # YYYY-MM-DD format

    employee_name_please_print: str = Field(
        ...,
        description=(
            'Employee\'s full printed name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    employee_id: str = Field(
        ...,
        description=(
            "10-digit employee identification number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    client_name_please_print: str = Field(
        ...,
        description=(
            'Client\'s full printed name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    client_id: str = Field(
        ...,
        description=(
            '10-digit client identification number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ShiftTimeEntries(BaseModel):
    """Service dates and time in/out for each shift"""

    service_date_month_mm_row_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month (MM) of service date for row 1"
    )

    service_date_day_dd_row_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day (DD) of service date for row 1"
    )

    time_in_hour_hh_row_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Hour (HH) for time in on row 1"
    )

    time_in_min_mm_row_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Minutes (MM) for time in on row 1"
    )

    time_in_am_row_1: BooleanLike = Field(..., description="Check if time in is AM for row 1")

    time_in_pm_row_1: BooleanLike = Field(..., description="Check if time in is PM for row 1")

    time_out_hour_hh_row_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Hour (HH) for time out on row 1"
    )

    time_out_min_mm_row_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Minutes (MM) for time out on row 1"
    )

    time_out_am_row_1: BooleanLike = Field(..., description="Check if time out is AM for row 1")

    time_out_pm_row_1: BooleanLike = Field(..., description="Check if time out is PM for row 1")

    service_date_month_mm_row_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month (MM) of service date for row 2"
    )

    service_date_day_dd_row_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day (DD) of service date for row 2"
    )

    time_in_hour_hh_row_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Hour (HH) for time in on row 2"
    )

    time_in_min_mm_row_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minutes (MM) for time in on row 2"
    )

    time_in_am_row_2: BooleanLike = Field(
        default="", description="Check if time in is AM for row 2"
    )

    time_in_pm_row_2: BooleanLike = Field(
        default="", description="Check if time in is PM for row 2"
    )

    time_out_hour_hh_row_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Hour (HH) for time out on row 2"
    )

    time_out_min_mm_row_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minutes (MM) for time out on row 2"
    )

    time_out_am_row_2: BooleanLike = Field(
        default="", description="Check if time out is AM for row 2"
    )

    time_out_pm_row_2: BooleanLike = Field(
        default="", description="Check if time out is PM for row 2"
    )

    service_date_month_mm_row_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month (MM) of service date for row 3"
    )

    service_date_day_dd_row_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day (DD) of service date for row 3"
    )

    time_in_hour_hh_row_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Hour (HH) for time in on row 3"
    )

    time_in_min_mm_row_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minutes (MM) for time in on row 3"
    )

    time_in_am_row_3: BooleanLike = Field(
        default="", description="Check if time in is AM for row 3"
    )

    time_in_pm_row_3: BooleanLike = Field(
        default="", description="Check if time in is PM for row 3"
    )

    time_out_hour_hh_row_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Hour (HH) for time out on row 3"
    )

    time_out_min_mm_row_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minutes (MM) for time out on row 3"
    )

    time_out_am_row_3: BooleanLike = Field(
        default="", description="Check if time out is AM for row 3"
    )

    time_out_pm_row_3: BooleanLike = Field(
        default="", description="Check if time out is PM for row 3"
    )

    service_date_month_mm_row_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month (MM) of service date for row 4"
    )

    service_date_day_dd_row_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day (DD) of service date for row 4"
    )

    time_in_hour_hh_row_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Hour (HH) for time in on row 4"
    )

    time_in_min_mm_row_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minutes (MM) for time in on row 4"
    )

    time_in_am_row_4: BooleanLike = Field(
        default="", description="Check if time in is AM for row 4"
    )

    time_in_pm_row_4: BooleanLike = Field(
        default="", description="Check if time in is PM for row 4"
    )

    time_out_hour_hh_row_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Hour (HH) for time out on row 4"
    )

    time_out_min_mm_row_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minutes (MM) for time out on row 4"
    )

    time_out_am_row_4: BooleanLike = Field(
        default="", description="Check if time out is AM for row 4"
    )

    time_out_pm_row_4: BooleanLike = Field(
        default="", description="Check if time out is PM for row 4"
    )


class ServiceCodesbyShift(BaseModel):
    """CFC and PCS service selection for each shift"""

    service_cfc_shift_1: BooleanLike = Field(
        default="", description="Check if CFC service code applies to shift 1"
    )

    service_cfc_shift_2: BooleanLike = Field(
        default="", description="Check if CFC service code applies to shift 2"
    )

    service_cfc_shift_3: BooleanLike = Field(
        default="", description="Check if CFC service code applies to shift 3"
    )

    service_cfc_shift_4: BooleanLike = Field(
        default="", description="Check if CFC service code applies to shift 4"
    )

    service_pcs_shift_1: BooleanLike = Field(
        default="", description="Check if PCS service code applies to shift 1"
    )

    service_pcs_shift_2: BooleanLike = Field(
        default="", description="Check if PCS service code applies to shift 2"
    )

    service_pcs_shift_3: BooleanLike = Field(
        default="", description="Check if PCS service code applies to shift 3"
    )

    service_pcs_shift_4: BooleanLike = Field(
        default="", description="Check if PCS service code applies to shift 4"
    )


class TasksPerformedbyShift(BaseModel):
    """Tasks completed for each shift"""

    positioning_shift_1: BooleanLike = Field(
        default="", description="Mark if positioning task was performed during shift 1"
    )

    positioning_shift_2: BooleanLike = Field(
        default="", description="Mark if positioning task was performed during shift 2"
    )

    positioning_shift_3: BooleanLike = Field(
        default="", description="Mark if positioning task was performed during shift 3"
    )

    positioning_shift_4: BooleanLike = Field(
        default="", description="Mark if positioning task was performed during shift 4"
    )

    prom_shift_1: BooleanLike = Field(
        default="", description="Mark if PROM task was performed during shift 1"
    )

    prom_shift_2: BooleanLike = Field(
        default="", description="Mark if PROM task was performed during shift 2"
    )

    prom_shift_3: BooleanLike = Field(
        default="", description="Mark if PROM task was performed during shift 3"
    )

    prom_shift_4: BooleanLike = Field(
        default="", description="Mark if PROM task was performed during shift 4"
    )

    transfer_shift_1: BooleanLike = Field(
        default="", description="Mark if transfer task was performed during shift 1"
    )

    transfer_shift_2: BooleanLike = Field(
        default="", description="Mark if transfer task was performed during shift 2"
    )

    transfer_shift_3: BooleanLike = Field(
        default="", description="Mark if transfer task was performed during shift 3"
    )

    transfer_shift_4: BooleanLike = Field(
        default="", description="Mark if transfer task was performed during shift 4"
    )

    locomote_single_shift_1: BooleanLike = Field(
        default="", description="Mark if single locomotion assistance was provided during shift 1"
    )

    locomote_single_shift_2: BooleanLike = Field(
        default="", description="Mark if single locomotion assistance was provided during shift 2"
    )

    locomote_single_shift_3: BooleanLike = Field(
        default="", description="Mark if single locomotion assistance was provided during shift 3"
    )

    locomote_single_shift_4: BooleanLike = Field(
        default="", description="Mark if single locomotion assistance was provided during shift 4"
    )

    locomote_multi_shift_1: BooleanLike = Field(
        default="", description="Mark if multi locomotion assistance was provided during shift 1"
    )

    locomote_multi_shift_2: BooleanLike = Field(
        default="", description="Mark if multi locomotion assistance was provided during shift 2"
    )

    locomote_multi_shift_3: BooleanLike = Field(
        default="", description="Mark if multi locomotion assistance was provided during shift 3"
    )

    locomote_multi_shift_4: BooleanLike = Field(
        default="", description="Mark if multi locomotion assistance was provided during shift 4"
    )

    locomote_med_shift_1: BooleanLike = Field(
        default="", description="Mark if medium locomotion assistance was provided during shift 1"
    )

    locomote_med_shift_2: BooleanLike = Field(
        default="", description="Mark if medium locomotion assistance was provided during shift 2"
    )

    locomote_med_shift_3: BooleanLike = Field(
        default="", description="Mark if medium locomotion assistance was provided during shift 3"
    )

    locomote_med_shift_4: BooleanLike = Field(
        default="", description="Mark if medium locomotion assistance was provided during shift 4"
    )

    dressing_shift_1: BooleanLike = Field(
        default="", description="Mark if dressing assistance was provided during shift 1"
    )

    dressing_shift_2: BooleanLike = Field(
        default="", description="Mark if dressing assistance was provided during shift 2"
    )

    dressing_shift_3: BooleanLike = Field(
        default="", description="Mark if dressing assistance was provided during shift 3"
    )

    dressing_shift_4: BooleanLike = Field(
        default="", description="Mark if dressing assistance was provided during shift 4"
    )

    eating_shift_1: BooleanLike = Field(
        default="", description="Mark if eating assistance was provided during shift 1"
    )

    eating_shift_2: BooleanLike = Field(
        default="", description="Mark if eating assistance was provided during shift 2"
    )

    eating_shift_3: BooleanLike = Field(
        default="", description="Mark if eating assistance was provided during shift 3"
    )

    eating_shift_4: BooleanLike = Field(
        default="", description="Mark if eating assistance was provided during shift 4"
    )

    toileting_shift_1: BooleanLike = Field(
        default="", description="Mark if toileting assistance was provided during shift 1"
    )

    toileting_shift_2: BooleanLike = Field(
        default="", description="Mark if toileting assistance was provided during shift 2"
    )

    toileting_shift_3: BooleanLike = Field(
        default="", description="Mark if toileting assistance was provided during shift 3"
    )

    toileting_shift_4: BooleanLike = Field(
        default="", description="Mark if toileting assistance was provided during shift 4"
    )

    hygiene_shift_1: BooleanLike = Field(
        default="", description="Mark if hygiene assistance was provided during shift 1"
    )

    hygiene_shift_2: BooleanLike = Field(
        default="", description="Mark if hygiene assistance was provided during shift 2"
    )

    hygiene_shift_3: BooleanLike = Field(
        default="", description="Mark if hygiene assistance was provided during shift 3"
    )

    hygiene_shift_4: BooleanLike = Field(
        default="", description="Mark if hygiene assistance was provided during shift 4"
    )

    bathing_shift_1: BooleanLike = Field(
        default="", description="Mark if bathing assistance was provided during shift 1"
    )

    bathing_shift_2: BooleanLike = Field(
        default="", description="Mark if bathing assistance was provided during shift 2"
    )

    bathing_shift_3: BooleanLike = Field(
        default="", description="Mark if bathing assistance was provided during shift 3"
    )

    bathing_shift_4: BooleanLike = Field(
        default="", description="Mark if bathing assistance was provided during shift 4"
    )

    light_meal_shift_1: BooleanLike = Field(
        default="",
        description="Mark if light meal preparation/assistance was provided during shift 1",
    )

    light_meal_shift_2: BooleanLike = Field(
        default="",
        description="Mark if light meal preparation/assistance was provided during shift 2",
    )

    light_meal_shift_3: BooleanLike = Field(
        default="",
        description="Mark if light meal preparation/assistance was provided during shift 3",
    )

    light_meal_shift_4: BooleanLike = Field(
        default="",
        description="Mark if light meal preparation/assistance was provided during shift 4",
    )

    main_meal_shift_1: BooleanLike = Field(
        default="",
        description="Mark if main meal preparation/assistance was provided during shift 1",
    )

    main_meal_shift_2: BooleanLike = Field(
        default="",
        description="Mark if main meal preparation/assistance was provided during shift 2",
    )

    main_meal_shift_3: BooleanLike = Field(
        default="",
        description="Mark if main meal preparation/assistance was provided during shift 3",
    )

    main_meal_shift_4: BooleanLike = Field(
        default="",
        description="Mark if main meal preparation/assistance was provided during shift 4",
    )

    housework_shift_1: BooleanLike = Field(
        default="", description="Mark if housework assistance was provided during shift 1"
    )

    housework_shift_2: BooleanLike = Field(
        default="", description="Mark if housework assistance was provided during shift 2"
    )

    housework_shift_3: BooleanLike = Field(
        default="", description="Mark if housework assistance was provided during shift 3"
    )

    housework_shift_4: BooleanLike = Field(
        default="", description="Mark if housework assistance was provided during shift 4"
    )

    shopping_shift_1: BooleanLike = Field(
        default="", description="Mark if shopping assistance was provided during shift 1"
    )

    shopping_shift_2: BooleanLike = Field(
        default="", description="Mark if shopping assistance was provided during shift 2"
    )

    shopping_shift_3: BooleanLike = Field(
        default="", description="Mark if shopping assistance was provided during shift 3"
    )

    shopping_shift_4: BooleanLike = Field(
        default="", description="Mark if shopping assistance was provided during shift 4"
    )

    laundry_shift_1: BooleanLike = Field(
        default="", description="Mark if laundry assistance was provided during shift 1"
    )

    laundry_shift_2: BooleanLike = Field(
        default="", description="Mark if laundry assistance was provided during shift 2"
    )

    laundry_shift_3: BooleanLike = Field(
        default="", description="Mark if laundry assistance was provided during shift 3"
    )

    laundry_shift_4: BooleanLike = Field(
        default="", description="Mark if laundry assistance was provided during shift 4"
    )

    wound_care_shift_1: BooleanLike = Field(
        default="", description="Mark if wound care was provided during shift 1"
    )

    wound_care_shift_2: BooleanLike = Field(
        default="", description="Mark if wound care was provided during shift 2"
    )

    wound_care_shift_3: BooleanLike = Field(
        default="", description="Mark if wound care was provided during shift 3"
    )

    wound_care_shift_4: BooleanLike = Field(
        default="", description="Mark if wound care was provided during shift 4"
    )

    oxygen_maint_shift_1: BooleanLike = Field(
        default="", description="Mark if oxygen maintenance was provided during shift 1"
    )

    oxygen_maint_shift_2: BooleanLike = Field(
        default="", description="Mark if oxygen maintenance was provided during shift 2"
    )

    oxygen_maint_shift_3: BooleanLike = Field(
        default="", description="Mark if oxygen maintenance was provided during shift 3"
    )

    oxygen_maint_shift_4: BooleanLike = Field(
        default="", description="Mark if oxygen maintenance was provided during shift 4"
    )

    escort_shift_1: BooleanLike = Field(
        default="", description="Mark if escort services were provided during shift 1"
    )

    escort_shift_2: BooleanLike = Field(
        default="", description="Mark if escort services were provided during shift 2"
    )

    escort_shift_3: BooleanLike = Field(
        default="", description="Mark if escort services were provided during shift 3"
    )

    escort_shift_4: BooleanLike = Field(
        default="", description="Mark if escort services were provided during shift 4"
    )

    medication_shift_1: BooleanLike = Field(
        default="", description="Mark if medication assistance was provided during shift 1"
    )

    medication_shift_2: BooleanLike = Field(
        default="", description="Mark if medication assistance was provided during shift 2"
    )

    medication_shift_3: BooleanLike = Field(
        default="", description="Mark if medication assistance was provided during shift 3"
    )

    medication_shift_4: BooleanLike = Field(
        default="", description="Mark if medication assistance was provided during shift 4"
    )


class CaseNotesbyShift(BaseModel):
    """Client response (G/A/P) and narrative notes for each shift"""

    case_notes_shift_1_g: BooleanLike = Field(
        default="", description="Select if client's response for shift 1 was Good (G)"
    )

    case_notes_shift_1_a: BooleanLike = Field(
        default="", description="Select if client's response for shift 1 was Average (A)"
    )

    case_notes_shift_1_p: BooleanLike = Field(
        default="", description="Select if client's response for shift 1 was Poor (P)"
    )

    case_notes_description_shift_1: str = Field(
        default="",
        description=(
            "Brief description of client's response and services for shift 1 .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    case_notes_shift_2_g: BooleanLike = Field(
        default="", description="Select if client's response for shift 2 was Good (G)"
    )

    case_notes_shift_2_a: BooleanLike = Field(
        default="", description="Select if client's response for shift 2 was Average (A)"
    )

    case_notes_shift_2_p: BooleanLike = Field(
        default="", description="Select if client's response for shift 2 was Poor (P)"
    )

    case_notes_description_shift_2: str = Field(
        default="",
        description=(
            "Brief description of client's response and services for shift 2 .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    case_notes_shift_3_g: BooleanLike = Field(
        default="", description="Select if client's response for shift 3 was Good (G)"
    )

    case_notes_shift_3_a: BooleanLike = Field(
        default="", description="Select if client's response for shift 3 was Average (A)"
    )

    case_notes_shift_3_p: BooleanLike = Field(
        default="", description="Select if client's response for shift 3 was Poor (P)"
    )

    case_notes_description_shift_3: str = Field(
        default="",
        description=(
            "Brief description of client's response and services for shift 3 .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    case_notes_shift_4_g: BooleanLike = Field(
        default="", description="Select if client's response for shift 4 was Good (G)"
    )

    case_notes_shift_4_a: BooleanLike = Field(
        default="", description="Select if client's response for shift 4 was Average (A)"
    )

    case_notes_shift_4_p: BooleanLike = Field(
        default="", description="Select if client's response for shift 4 was Poor (P)"
    )

    case_notes_description_shift_4: str = Field(
        default="",
        description=(
            "Brief description of client's response and services for shift 4 .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class FVVCodes(BaseModel):
    """FVV in/out codes for each shift"""

    fvv_code_in_shift_1_digit_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="First digit of FVV In code for shift 1"
    )

    fvv_code_in_shift_1_digit_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Second digit of FVV In code for shift 1"
    )

    fvv_code_in_shift_1_digit_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Third digit of FVV In code for shift 1"
    )

    fvv_code_in_shift_1_digit_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Fourth digit of FVV In code for shift 1"
    )

    fvv_code_in_shift_1_digit_5: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Fifth digit of FVV In code for shift 1"
    )

    fvv_code_in_shift_1_digit_6: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Sixth digit of FVV In code for shift 1"
    )

    fvv_code_in_shift_1_digit_7: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Seventh digit of FVV In code for shift 1"
    )

    fvv_code_in_shift_1_digit_8: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Eighth digit of FVV In code for shift 1"
    )

    fvv_code_out_shift_1_digit_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="First digit of FVV Out code for shift 1"
    )

    fvv_code_out_shift_1_digit_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Second digit of FVV Out code for shift 1"
    )

    fvv_code_out_shift_1_digit_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Third digit of FVV Out code for shift 1"
    )

    fvv_code_out_shift_1_digit_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Fourth digit of FVV Out code for shift 1"
    )

    fvv_code_out_shift_1_digit_5: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Fifth digit of FVV Out code for shift 1"
    )

    fvv_code_out_shift_1_digit_6: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Sixth digit of FVV Out code for shift 1"
    )

    fvv_code_out_shift_1_digit_7: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Seventh digit of FVV Out code for shift 1"
    )

    fvv_code_out_shift_1_digit_8: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Eighth digit of FVV Out code for shift 1"
    )

    fvv_code_in_shift_2_digit_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="First digit of FVV In code for shift 2"
    )

    fvv_code_in_shift_2_digit_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Second digit of FVV In code for shift 2"
    )

    fvv_code_in_shift_2_digit_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Third digit of FVV In code for shift 2"
    )

    fvv_code_in_shift_2_digit_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Fourth digit of FVV In code for shift 2"
    )

    fvv_code_in_shift_2_digit_5: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Fifth digit of FVV In code for shift 2"
    )

    fvv_code_in_shift_2_digit_6: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Sixth digit of FVV In code for shift 2"
    )

    fvv_code_in_shift_2_digit_7: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Seventh digit of FVV In code for shift 2"
    )

    fvv_code_in_shift_2_digit_8: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Eighth digit of FVV In code for shift 2"
    )

    fvv_code_out_shift_2_digit_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="First digit of FVV Out code for shift 2"
    )

    fvv_code_out_shift_2_digit_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Second digit of FVV Out code for shift 2"
    )

    fvv_code_out_shift_2_digit_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Third digit of FVV Out code for shift 2"
    )

    fvv_code_out_shift_2_digit_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Fourth digit of FVV Out code for shift 2"
    )

    fvv_code_out_shift_2_digit_5: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Fifth digit of FVV Out code for shift 2"
    )

    fvv_code_out_shift_2_digit_6: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Sixth digit of FVV Out code for shift 2"
    )

    fvv_code_out_shift_2_digit_7: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Seventh digit of FVV Out code for shift 2"
    )

    fvv_code_out_shift_2_digit_8: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Eighth digit of FVV Out code for shift 2"
    )

    fvv_code_in_shift_3_digit_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="First digit of FVV In code for shift 3"
    )

    fvv_code_in_shift_3_digit_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Second digit of FVV In code for shift 3"
    )

    fvv_code_in_shift_3_digit_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Third digit of FVV In code for shift 3"
    )

    fvv_code_in_shift_3_digit_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Fourth digit of FVV In code for shift 3"
    )

    fvv_code_in_shift_3_digit_5: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Fifth digit of FVV In code for shift 3"
    )

    fvv_code_in_shift_3_digit_6: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Sixth digit of FVV In code for shift 3"
    )

    fvv_code_in_shift_3_digit_7: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Seventh digit of FVV In code for shift 3"
    )

    fvv_code_in_shift_3_digit_8: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Eighth digit of FVV In code for shift 3"
    )

    fvv_code_out_shift_3_digit_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="First digit of FVV Out code for shift 3"
    )

    fvv_code_out_shift_3_digit_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Second digit of FVV Out code for shift 3"
    )

    fvv_code_out_shift_3_digit_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Third digit of FVV Out code for shift 3"
    )

    fvv_code_out_shift_3_digit_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Fourth digit of FVV Out code for shift 3"
    )

    fvv_code_out_shift_3_digit_5: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Fifth digit of FVV Out code for shift 3"
    )

    fvv_code_out_shift_3_digit_6: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Sixth digit of FVV Out code for shift 3"
    )

    fvv_code_out_shift_3_digit_7: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Seventh digit of FVV Out code for shift 3"
    )

    fvv_code_out_shift_3_digit_8: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Eighth digit of FVV Out code for shift 3"
    )

    fvv_code_in_shift_4_digit_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="First digit of FVV In code for shift 4"
    )

    fvv_code_in_shift_4_digit_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Second digit of FVV In code for shift 4"
    )

    fvv_code_in_shift_4_digit_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Third digit of FVV In code for shift 4"
    )

    fvv_code_in_shift_4_digit_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Fourth digit of FVV In code for shift 4"
    )

    fvv_code_in_shift_4_digit_5: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Fifth digit of FVV In code for shift 4"
    )

    fvv_code_in_shift_4_digit_6: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Sixth digit of FVV In code for shift 4"
    )

    fvv_code_in_shift_4_digit_7: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Seventh digit of FVV In code for shift 4"
    )

    fvv_code_in_shift_4_digit_8: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Eighth digit of FVV In code for shift 4"
    )

    fvv_code_out_shift_4_digit_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="First digit of FVV Out code for shift 4"
    )

    fvv_code_out_shift_4_digit_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Second digit of FVV Out code for shift 4"
    )

    fvv_code_out_shift_4_digit_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Third digit of FVV Out code for shift 4"
    )

    fvv_code_out_shift_4_digit_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Fourth digit of FVV Out code for shift 4"
    )

    fvv_code_out_shift_4_digit_5: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Fifth digit of FVV Out code for shift 4"
    )

    fvv_code_out_shift_4_digit_6: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Sixth digit of FVV Out code for shift 4"
    )

    fvv_code_out_shift_4_digit_7: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Seventh digit of FVV Out code for shift 4"
    )

    fvv_code_out_shift_4_digit_8: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Eighth digit of FVV Out code for shift 4"
    )


class EVVComments(BaseModel):
    """Explanation when unable to electronically check in/out"""

    evv_comments_line_1: str = Field(
        default="",
        description=(
            "First line of explanation if unable to electronically check in/out .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    evv_comments_line_2: str = Field(
        default="",
        description=(
            "Second line of explanation if unable to electronically check in/out .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    evv_comments_line_3: str = Field(
        default="",
        description=(
            "Third line of explanation if unable to electronically check in/out .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    evv_comments_line_4: str = Field(
        default="",
        description=(
            "Fourth line of explanation if unable to electronically check in/out .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ClientConditionChanges(BaseModel):
    """Narrative description of any change in client's condition"""

    describe_any_change_in_clients_condition_line_1: str = Field(
        default="",
        description=(
            "First line describing any change, improvement, or decline in client's "
            'condition .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    describe_any_change_in_clients_condition_line_2: str = Field(
        default="",
        description=(
            "Second line describing any change, improvement, or decline in client's "
            'condition .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    describe_any_change_in_clients_condition_line_3: str = Field(
        default="",
        description=(
            "Third line describing any change, improvement, or decline in client's "
            'condition .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    describe_any_change_in_clients_condition_line_4: str = Field(
        default="",
        description=(
            "Fourth line describing any change, improvement, or decline in client's "
            'condition .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    describe_any_change_in_clients_condition_line_5: str = Field(
        default="",
        description=(
            "Fifth line describing any change, improvement, or decline in client's "
            'condition .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    describe_any_change_in_clients_condition_line_6: str = Field(
        default="",
        description=(
            "Sixth line describing any change, improvement, or decline in client's "
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
            "Signature of employee certifying hours and services .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    employee_signature_date_month_mm: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month (MM) of employee signature date"
    )

    employee_signature_date_day_dd: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day (DD) of employee signature date"
    )

    employee_signature_date_year_yy: Union[float, Literal["N/A", ""]] = Field(
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

    client_representative_signature_date_month_mm: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month (MM) of client/representative signature date"
    )

    client_representative_signature_date_day_dd: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day (DD) of client/representative signature date"
    )

    client_representative_signature_date_year_yy: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year (YY) of client/representative signature date"
    )


class ConsumerDirectCareNetworkAlaskaCfcAndPcsTimesheet(BaseModel):
    """
        CONSUMER DIRECT
    CARE NETWORK

    Alaska
    CFC and PCS Timesheet

        For the week of service, timesheets are due the following Monday by 5:00pm if faxed or dropped off, and postmarked by Monday if mailed. Timesheets are due every week. Due to the timing of the payroll cycle, late timesheets will result in late pay. Timesheets must be signed AFTER all work is completed. Advance timesheets will not be accepted.
    """

    week__participant_information: WeekParticipantInformation = Field(
        ..., description="Week & Participant Information"
    )
    shift_time_entries: ShiftTimeEntries = Field(..., description="Shift Time Entries")
    service_codes_by_shift: ServiceCodesbyShift = Field(..., description="Service Codes by Shift")
    tasks_performed_by_shift: TasksPerformedbyShift = Field(
        ..., description="Tasks Performed by Shift"
    )
    case_notes_by_shift: CaseNotesbyShift = Field(..., description="Case Notes by Shift")
    fvv_codes: FVVCodes = Field(..., description="FVV Codes")
    evv_comments: EVVComments = Field(..., description="EVV Comments")
    client_condition_changes: ClientConditionChanges = Field(
        ..., description="Client Condition Changes"
    )
    signatures: Signatures = Field(..., description="Signatures")
