from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RecipientInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about the office or clerk to which the notice is being sent."""

    office_of_planning_and_research: BooleanLike = Field(
        ...,
        description="Check if filing with the Office of Planning and Research"
    )

    county_clerk: BooleanLike = Field(
        ...,
        description="Check if filing with the County Clerk"
    )

    county_of: str = Field(
        ...,
        description=(
            "Name of the county for County Clerk filing .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    address_county_clerk: str = Field(
        ...,
        description=(
            "Mailing address for the County Clerk .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class SubmittingAgencyInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Details about the public agency submitting the notice and the lead agency if different."""

    public_agency: str = Field(
        ...,
        description=(
            "Name of the public agency filing the notice .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    address_public_agency: str = Field(
        ...,
        description=(
            "Mailing address of the public agency .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    contact_public_agency: str = Field(
        ...,
        description=(
            "Contact person at the public agency .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    phone_public_agency: str = Field(
        ...,
        description=(
            "Phone number for the public agency contact .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    lead_agency_if_different_from_above: str = Field(
        ...,
        description=(
            "Name of the lead agency if different from public agency .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    address_lead_agency: str = Field(
        ...,
        description=(
            "Mailing address of the lead agency .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    contact_lead_agency: str = Field(
        ...,
        description=(
            "Contact person at the lead agency .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    phone_lead_agency: str = Field(
        ...,
        description=(
            "Phone number for the lead agency contact .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )


class ProjectInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Key details about the project and its location."""

    state_clearinghouse_number_if_submitted_to_state_clearinghouse: str = Field(
        ...,
        description=(
            "State Clearinghouse Number, if applicable .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    project_title: str = Field(
        ...,
        description=(
            "Title of the project .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    project_applicant: str = Field(
        ...,
        description=(
            "Name of the project applicant .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    project_location_include_county: str = Field(
        ...,
        description=(
            "Location of the project, including county .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    project_description: str = Field(
        ...,
        description=(
            "Brief description of the project .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class ProjectApprovalandDeterminations(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about project approval and required CEQA determinations."""

    lead_agency_or_responsible_agency: str = Field(
        ...,
        description=(
            "Name of the lead or responsible agency approving the project .If you cannot "
            "fill this, write \"N/A\". If this field should not be filled by you (for "
            "example, it belongs to another person or office), leave it blank (empty string "
            "\"\")."
        )
    )

    date_project_approval: str = Field(
        ...,
        description="Date the project was approved"
    )  # YYYY-MM-DD format

    the_project_will_have_a_significant_effect_on_the_environment: BooleanLike = Field(
        ...,
        description="Indicate if the project will have a significant effect on the environment"
    )

    the_project_will_not_have_a_significant_effect_on_the_environment: BooleanLike = Field(
        ...,
        description="Indicate if the project will not have a significant effect on the environment"
    )

    an_environmental_impact_report_was_prepared_for_this_project_pursuant_to_the_provisions_of_ceqa: BooleanLike = Field(
        ...,
        description="Check if an Environmental Impact Report was prepared for this project"
    )

    a_negative_declaration_was_prepared_for_this_project_pursuant_to_the_provisions_of_ceqa: BooleanLike = Field(
        ...,
        description="Check if a Negative Declaration was prepared for this project"
    )

    mitigation_measures_were_made_a_condition_of_the_approval_of_the_project: BooleanLike = Field(
        ...,
        description="Indicate if mitigation measures were made a condition of approval"
    )

    mitigation_measures_were_not_made_a_condition_of_the_approval_of_the_project: BooleanLike = Field(
        ...,
        description="Indicate if mitigation measures were not made a condition of approval"
    )

    a_mitigation_reporting_or_monitoring_plan_was_adopted_for_this_project: BooleanLike = Field(
        ...,
        description="Indicate if a mitigation reporting or monitoring plan was adopted"
    )

    a_mitigation_reporting_or_monitoring_plan_was_not_adopted_for_this_project: BooleanLike = Field(
        ...,
        description="Indicate if a mitigation reporting or monitoring plan was not adopted"
    )

    a_statement_of_overriding_considerations_was_adopted_for_this_project: BooleanLike = Field(
        ...,
        description="Indicate if a statement of Overriding Considerations was adopted"
    )

    a_statement_of_overriding_considerations_was_not_adopted_for_this_project: BooleanLike = Field(
        ...,
        description="Indicate if a statement of Overriding Considerations was not adopted"
    )

    findings_were_made_pursuant_to_the_provisions_of_ceqa: BooleanLike = Field(
        ...,
        description="Indicate if findings were made pursuant to CEQA"
    )

    findings_were_not_made_pursuant_to_the_provisions_of_ceqa: BooleanLike = Field(
        ...,
        description="Indicate if findings were not made pursuant to CEQA"
    )


class CertificationandFiling(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Certification of document availability and official signatures."""

    location_where_final_eir_or_negative_declaration_is_available: str = Field(
        ...,
        description=(
            "Location where the final EIR or Negative Declaration is available to the "
            "public .If you cannot fill this, write \"N/A\". If this field should not be "
            "filled by you (for example, it belongs to another person or office), leave it "
            "blank (empty string \"\")."
        )
    )

    signature_public_agency: str = Field(
        ...,
        description=(
            "Signature of authorized public agency representative .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    title: str = Field(
        ...,
        description=(
            "Title of the person signing for the public agency .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    date: str = Field(
        ...,
        description="Date of signature"
    )  # YYYY-MM-DD format

    date_received_for_filing_at_opr: str = Field(
        ...,
        description="Date received for filing at Office of Planning and Research"
    )  # YYYY-MM-DD format


class NoticeOfDeterminationAppendixD(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    Notice of Determination
Appendix D

    SUBJECT: Filing of Notice of Determination in compliance with Section 21108 or 21152 of the Public Resources Code.
    """

    recipient_information: RecipientInformation = Field(
        ...,
        description="Recipient Information"
    )
    submitting_agency_information: SubmittingAgencyInformation = Field(
        ...,
        description="Submitting Agency Information"
    )
    project_information: ProjectInformation = Field(
        ...,
        description="Project Information"
    )
    project_approval_and_determinations: ProjectApprovalandDeterminations = Field(
        ...,
        description="Project Approval and Determinations"
    )
    certification_and_filing: CertificationandFiling = Field(
        ...,
        description="Certification and Filing"
    )