from pydantic import BaseModel, ConfigDict, Field


class NoticeOfExemption(BaseModel):
    """Notice of Exemption

    Purpose: This form is used by public agencies or project applicants to notify state and county authorities that a proposed project is exempt from environmental review under the California Environmental Quality Act (CEQA). It documents the exemption status and the reasons for exemption for official record-keeping and compliance purposes.
    Recipient: The intended recipients are officials at the California Office of Planning and Research and the relevant County Clerk's office, who are responsible for processing, recording, and maintaining public records of CEQA exemption notices.
    """

    model_config = ConfigDict(extra="forbid")
