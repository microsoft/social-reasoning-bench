from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EquipmentRequestDetails(BaseModel):
    """Information about the requesting agency and the equipment being requested"""

    date: str = Field(
        ..., description="Date the equipment request is submitted"
    )  # YYYY-MM-DD format

    ems_agency: str = Field(
        ...,
        description=(
            "Name of the EMS agency submitting the request .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_requestor: str = Field(
        ...,
        description=(
            "Full name of the person submitting the request .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    new_equipment: BooleanLike = Field(
        ..., description="Check if the request is for entirely new equipment"
    )

    additional_or_replacement_equipment: BooleanLike = Field(
        ..., description="Check if the request is for additional or replacement equipment"
    )

    item_name_description: str = Field(
        ...,
        description=(
            "Name and brief description of the equipment item .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    manufacturer: str = Field(
        ...,
        description=(
            'Manufacturer of the equipment .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    vendor_if_different_from_manufacturer: str = Field(
        default="",
        description=(
            "Vendor or supplier if different from the manufacturer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    item_number_reference_number: str = Field(
        default="",
        description=(
            "Item or reference number used by the manufacturer or vendor .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    als: BooleanLike = Field(
        ...,
        description="Check if Advanced Life Support level of care is required to use this equipment",
    )

    bls: BooleanLike = Field(
        ...,
        description="Check if Basic Life Support level of care is required to use this equipment",
    )

    first_responder: BooleanLike = Field(
        ...,
        description="Check if First Responder level of care is sufficient to use this equipment",
    )

    no_specialized_or_additional_training_required: BooleanLike = Field(
        ...,
        description=(
            "Check if no specialized or additional training is required to use this equipment"
        ),
    )

    yes_specialized_or_additional_training_required: BooleanLike = Field(
        ...,
        description="Check if specialized or additional training is required to use this equipment",
    )

    explain_additional_or_specialized_training_required_if_applicable: str = Field(
        default="",
        description=(
            "Describe any additional or specialized training needed to use the equipment "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    no_current_sop_apply_or_make_provision_for_use: BooleanLike = Field(
        ...,
        description=(
            "Check if current SOPs do not apply or make provision for use of this new equipment"
        ),
    )

    yes_current_sop_apply_or_make_provision_for_use: BooleanLike = Field(
        ...,
        description="Check if current SOPs apply or make provision for use of this new equipment",
    )

    list_current_sop_policy_that_applied_to_equipment_use: str = Field(
        default="",
        description=(
            "Identify the current SOP or policy that applies to the equipment use .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    explain_need_for_sop_policy_addition_or_change: str = Field(
        default="",
        description=(
            "Explain why a new SOP/policy or a change to an existing one is needed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    describe_how_equipment_will_directly_benefit_the_provision_of_patient_care_attach_additional_information_as_needed: str = Field(
        ...,
        description=(
            "Describe how this equipment will improve or directly benefit patient care .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AdministrativeUseOnly(BaseModel):
    """For EMS system review and approval"""

    approved: BooleanLike = Field(
        default="", description="Indicates the request has been approved by the EMS system"
    )

    denied: BooleanLike = Field(
        default="", description="Indicates the request has been denied by the EMS system"
    )

    additional_information_required: BooleanLike = Field(
        default="",
        description="Indicates that more information is needed before a decision can be made",
    )

    comments_notes: str = Field(
        default="",
        description=(
            "Administrative comments or notes regarding the request .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ems_system_coordinator_signature: str = Field(
        ...,
        description=(
            "Signature of the EMS System Coordinator .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_ems_system_coordinator_signature: str = Field(
        ..., description="Date the EMS System Coordinator signed the form"
    )  # YYYY-MM-DD format

    ems_medical_director_signature: str = Field(
        ...,
        description=(
            'Signature of the EMS Medical Director .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_ems_medical_director_signature: str = Field(
        ..., description="Date the EMS Medical Director signed the form"
    )  # YYYY-MM-DD format


class NewOrAdditionalEquipmentRequest(BaseModel):
    """
    NEW OR ADDITIONAL EQUIPMENT REQUEST

    THE ADDITION OF EQUIPMENT USED FOR PATIENT CARE PURPOSES REQUIRES APPROVAL FROM THE CENTRAL DUPAGE EMERGENCY MEDICAL SERVICES SYSTEM AND MEDICAL DIRECTOR. THIS FORM MUST BE COMPLETED IN ITS ENTIRETY AND SUBMITTED TO THE EMS OFFICE PRIOR TO THE USE OF REQUESTED NEW OR ADDITIONAL EQUIPMENT IN THE PROVISION OF PATIENT CARE. SAID EQUIPMENT MAY NOT BE USED FOR PATIENT CARE PURPOSES UNTIL THIS REQUEST IS APPROVED AND RETURNED TO THE REQUESTING AGENCY.
    """

    equipment_request_details: EquipmentRequestDetails = Field(
        ..., description="Equipment Request Details"
    )
    administrative_use_only: AdministrativeUseOnly = Field(
        ..., description="Administrative Use Only"
    )
