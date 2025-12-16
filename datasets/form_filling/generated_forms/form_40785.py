from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ExecutiveOrderNo21McGreevey2002(BaseModel):
    """OPRA exemptions based on Executive Order 21"""

    records_sabotage_terrorism_risk: BooleanLike = Field(
        default="",
        description=(
            "Check if this exemption is being claimed because disclosure would interfere "
            "with protection against or increase the risk of sabotage or terrorism."
        ),
    )

    records_exempted_by_state_agency_proposed_rules: BooleanLike = Field(
        default="",
        description=(
            "Check if this exemption is being claimed because the records are exempted from "
            "disclosure by a State agency’s proposed rules."
        ),
    )


class ExecutiveOrderNo26McGreevey2002(BaseModel):
    """OPRA exemptions based on Executive Order 26"""

    certain_records_maintained_by_governor_office: BooleanLike = Field(
        default="",
        description=(
            "Check if this exemption is being claimed for records maintained by the Office "
            "of the Governor that are exempt under Executive Order No. 26."
        ),
    )

    employment_applicant_records_during_search: BooleanLike = Field(
        default="",
        description=(
            "Check if this exemption is being claimed for resumes, employment applications, "
            "or other job applicant information while a recruitment search is still in "
            "progress."
        ),
    )

    complaint_investigation_records_model_procedures: BooleanLike = Field(
        default="",
        description=(
            "Check if this exemption is being claimed for complaint and investigation "
            "records under the Model Procedures for Internal Complaints Alleging "
            "Discrimination, Harassment or Hostile Environments."
        ),
    )

    medical_psychiatric_psychological_information: BooleanLike = Field(
        default="",
        description=(
            "Check if this exemption is being claimed for records containing medical, "
            "psychiatric, or psychological history, diagnosis, treatment, or evaluation "
            "information."
        ),
    )

    personal_income_tax_return_information: BooleanLike = Field(
        default="",
        description=(
            "Check if this exemption is being claimed for information contained in a "
            "personal income tax return or other tax return."
        ),
    )

    personal_financial_information: BooleanLike = Field(
        default="",
        description=(
            "Check if this exemption is being claimed for detailed personal financial "
            "information such as income, assets, liabilities, net worth, bank balances, "
            "financial history, activities, or creditworthiness."
        ),
    )

    test_questions_and_exam_data: BooleanLike = Field(
        default="",
        description=(
            "Check if this exemption is being claimed for test questions, scoring keys, or "
            "other examination data used for public employment or licensing exams."
        ),
    )

    records_possession_other_department_confidential: BooleanLike = Field(
        default="",
        description=(
            "Check if this exemption is being claimed for records held by another "
            "department that are confidential by regulation or Executive Order 9."
        ),
    )


class OtherStatutoryorLegalExemptions(BaseModel):
    """Other exemptions from disclosure under statute, regulation, or order"""

    other_exemptions_under_statute_or_order: BooleanLike = Field(
        default="",
        description=(
            "Check if you are relying on any other exemption under State statute, "
            "legislative resolution, regulation, Executive Order, Rules of Court, or "
            "federal law, regulation, or order pursuant to N.J.S.A. 47:1A-9.a."
        ),
    )

    detailed_exemption_information: str = Field(
        default="",
        description=(
            "Provide detailed explanation of the specific exemption(s) relied upon to deny "
            "access to the requested government records. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    specific_exemptions_applying_to_each_record: str = Field(
        default="",
        description=(
            "Identify which exemption(s) apply to each individual record requested, if "
            'multiple records are involved. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class RequestforRecordsUndertheCommonLaw(BaseModel):
    """Common law records request and requester’s interest"""

    request_under_common_law: BooleanLike = Field(
        default="",
        description=(
            "Check if you are also requesting the same records under the common law right "
            "of access, in addition to OPRA."
        ),
    )

    interest_in_subject_matter: str = Field(
        default="",
        description=(
            "Describe your legally recognized interest in the subject matter of the "
            "requested records for purposes of a common law records request. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class RequestForRecordsUnderTheCommonLaw(BaseModel):
    """
    REQUEST FOR RECORDS UNDER THE COMMON LAW

    A public record under the common law is one required by law to be kept, or necessary to be kept in the discharge of a duty imposed by law, or directed by law to serve as a memorial and evidence of something written, said, or done, or a written memorial made by a public officer authorized to perform that function, or a writing filed in a public office. The elements essential to constitute a public record are that it be a written memorial, that it be made by a public officer, and that the officer be authorized by law to make it.
    If the information requested is a "public record" under common law and the requestor has a legally recognized interest in the subject matter contained in the material, then the material must be disclosed if the individual's right of access outweighs the State's interest in preventing disclosure.
    Note that any challenge to a denial of a request for records under the common law cannot be made to the Government Records Council, as the Government Records Council only has jurisdiction to adjudicate challenges to denials of OPRA requests. A challenge to the denial of access under the common law can be made by filing an action in Superior Court.
    """

    executive_order_no_21_mcgreevey_2002: ExecutiveOrderNo21McGreevey2002 = Field(
        ..., description="Executive Order No. 21 (McGreevey 2002)"
    )
    executive_order_no_26_mcgreevey_2002: ExecutiveOrderNo26McGreevey2002 = Field(
        ..., description="Executive Order No. 26 (McGreevey 2002)"
    )
    other_statutory_or_legal_exemptions: OtherStatutoryorLegalExemptions = Field(
        ..., description="Other Statutory or Legal Exemptions"
    )
    request_for_records_under_the_common_law: RequestforRecordsUndertheCommonLaw = Field(
        ..., description="Request for Records Under the Common Law"
    )
