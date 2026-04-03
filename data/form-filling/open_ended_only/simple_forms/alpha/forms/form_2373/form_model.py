from pydantic import BaseModel, ConfigDict, Field


class BachelorsMastersThesisSouthTyrolApp(BaseModel):
    """CALL FOR PROPOSALS "BACHELOR'S AND MASTER'S THESES ON THE SOUTH TYROLEAN ECONOMY" APPLICATION FORM

    Purpose: Application for a call for proposals to support bachelor's and master's theses focused on the South Tyrolean economy. The form collects student and supervisor information, thesis details, and a research exposé.
    Recipient: Staff and evaluators at the Institute for Economic Research of the Chamber of Commerce, Industry, Crafts and Agriculture of Bolzano, who will assess the suitability and relevance of the proposed thesis for the call.
    """

    model_config = ConfigDict(extra="forbid")

