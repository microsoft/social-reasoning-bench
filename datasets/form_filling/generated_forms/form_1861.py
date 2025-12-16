from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EmployeeRequest(BaseModel):
    """Top section completed by the employee, including personal information and reason for leave"""

    employee: str = Field(
        ...,
        description=(
            'Employee\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Employee's primary contact phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    home_mailing_address: str = Field(
        ...,
        description=(
            'Employee\'s full home mailing address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    department: str = Field(
        ...,
        description=(
            "Employee's department within the county .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    title: str = Field(
        ...,
        description=(
            'Employee\'s job title .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    serious_health_condition_of_employee: BooleanLike = Field(
        ..., description="Check if the leave is due to the employee's own serious health condition"
    )

    placement_for_adoption_foster_care: BooleanLike = Field(
        ...,
        description="Check if the leave is for placement of a child for adoption or foster care",
    )

    date_to_begin_care_of_child: str = Field(
        default="", description="Date when care of the child will begin"
    )  # YYYY-MM-DD format

    birth_of_a_child: BooleanLike = Field(
        ..., description="Check if the leave is related to the birth of a child"
    )

    expected_due_date: str = Field(
        default="", description="Expected due date of the child"
    )  # YYYY-MM-DD format

    leave_to_care_for_a_family_member: BooleanLike = Field(
        ..., description="Check if the leave is to care for a qualifying family member"
    )

    name_family_member_care: str = Field(
        default="",
        description=(
            "Name of the family member for whom care will be provided .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    relationship_family_member_care: str = Field(
        default="",
        description=(
            "Relationship of the family member to the employee .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    military_family_exigency_leave: BooleanLike = Field(
        ..., description="Check if the leave is for a qualifying military family exigency"
    )

    name_military_family_exigency: str = Field(
        default="",
        description=(
            "Name of the military family member related to the exigency leave .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    relationship_military_family_exigency: str = Field(
        default="",
        description=(
            "Relationship of the military family member to the employee .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    military_care_giver_leave: BooleanLike = Field(
        ...,
        description=(
            "Check if the leave is to care for a covered servicemember with a serious "
            "injury or illness"
        ),
    )

    name_military_care_giver: str = Field(
        default="",
        description=(
            "Name of the servicemember for whom care will be provided .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    relationship_military_care_giver: str = Field(
        default="",
        description=(
            "Relationship of the servicemember to the employee .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other: str = Field(
        default="",
        description=(
            "Describe any other reason for the leave request .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_expansion_public_health_emergency: BooleanLike = Field(
        ...,
        description=(
            "Check if leave is requested to care for a child due to school or childcare "
            "closure from a public health emergency"
        ),
    )

    requested_start_date: str = Field(
        ..., description="Date the employee is requesting the leave to begin"
    )  # YYYY-MM-DD format

    anticipated_return_to_work_date: str = Field(
        ..., description="Date the employee expects to return to work"
    )  # YYYY-MM-DD format

    intermittent_or_reduced_work_schedule_describe: str = Field(
        default="",
        description=(
            "Describe any requested intermittent or reduced work schedule .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    employee_signature_date: str = Field(
        ...,
        description=(
            "Employee's signature and date of request .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class DesignationofLeave(BaseModel):
    """Bottom section completed by the County Administrator to designate and track leave"""

    leave_provisionally_approved_pending_medical_verification: BooleanLike = Field(
        default="",
        description="Indicate if the leave is provisionally approved pending medical verification",
    )

    leave_approved: BooleanLike = Field(
        default="", description="Indicate if the leave is fully approved"
    )

    leave_denied_reason: str = Field(
        default="",
        description=(
            "If leave is denied, specify the reason(s) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    from_designation_of_leave: str = Field(
        default="", description="Start date of the designated leave period"
    )  # YYYY-MM-DD format

    through_designation_of_leave: str = Field(
        default="", description="End date of the designated leave period"
    )  # YYYY-MM-DD format

    qualifies_as_family_medical_leave: BooleanLike = Field(
        default="",
        description="Indicate whether the leave period qualifies as Family & Medical Leave",
    )

    vacation_hours: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of vacation hours to be applied during the leave period"
    )

    vacation_from: str = Field(
        default="", description="Start date for vacation hours used during leave"
    )  # YYYY-MM-DD format

    vacation_through: str = Field(
        default="", description="End date for vacation hours used during leave"
    )  # YYYY-MM-DD format

    sick_leave_hours: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of sick leave hours to be applied during the leave period"
    )

    sick_leave_from: str = Field(
        default="", description="Start date for sick leave hours used during leave"
    )  # YYYY-MM-DD format

    sick_leave_through: str = Field(
        default="", description="End date for sick leave hours used during leave"
    )  # YYYY-MM-DD format

    comp_time_off_hours: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of compensatory time off hours to be applied during the leave period",
    )

    comp_time_off_from: str = Field(
        default="", description="Start date for compensatory time off hours used during leave"
    )  # YYYY-MM-DD format

    comp_time_off_through: str = Field(
        default="", description="End date for compensatory time off hours used during leave"
    )  # YYYY-MM-DD format

    floating_holiday_hours: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of floating holiday hours to be applied during the leave period",
    )

    floating_holiday_from: str = Field(
        default="", description="Start date for floating holiday hours used during leave"
    )  # YYYY-MM-DD format

    floating_holiday_through: str = Field(
        default="", description="End date for floating holiday hours used during leave"
    )  # YYYY-MM-DD format

    emergency_leave_bank_hours: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of emergency leave bank hours to be applied during the leave period",
    )

    emergency_leave_bank_from: str = Field(
        default="", description="Start date for emergency leave bank hours used during leave"
    )  # YYYY-MM-DD format

    emergency_leave_bank_through: str = Field(
        default="", description="End date for emergency leave bank hours used during leave"
    )  # YYYY-MM-DD format

    workers_comp_hours: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of Worker's Compensation hours to be applied during the leave period",
    )

    workers_comp_from: str = Field(
        default="", description="Start date for Worker's Compensation hours used during leave"
    )  # YYYY-MM-DD format

    workers_comp_through: str = Field(
        default="", description="End date for Worker's Compensation hours used during leave"
    )  # YYYY-MM-DD format

    leave_wo_pay_hours: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of unpaid leave hours to be applied during the leave period"
    )

    leave_wo_pay_from: str = Field(
        default="", description="Start date for unpaid leave hours used during leave"
    )  # YYYY-MM-DD format

    leave_wo_pay_through: str = Field(
        default="", description="End date for unpaid leave hours used during leave"
    )  # YYYY-MM-DD format

    supervisor_signature_date: str = Field(
        ...,
        description=(
            "Supervisor's signature and date confirming designation of leave .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class BayfieldCountyFamilyMedicalLeaveRequest(BaseModel):
    """
        BAYFIELD COUNTY
    FAMILY & MEDICAL LEAVE REQUEST

        ''
    """

    employee_request: EmployeeRequest = Field(..., description="Employee Request")
    designation_of_leave: DesignationofLeave = Field(..., description="Designation of Leave")
