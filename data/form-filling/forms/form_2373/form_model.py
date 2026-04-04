from pydantic import BaseModel, ConfigDict, Field


class BachelorsAndMastersThesesSouthTyroleanEconomyApp(BaseModel):
    """CALL FOR PROPOSALS "BACHELOR'S AND MASTER'S THESES ON THE SOUTH TYROLEAN ECONOMY" APPLICATION FORM

    Students submit this application to the Bolzano Chamber of Commerce (IER) to apply for support/awards for bachelor’s
    or master’s theses relevant to the South Tyrolean economy. IER staff and the evaluation/selection committee review
    the student and supervisor details and the thesis exposé to assess eligibility and decide on selection and funding.
    """

    model_config = ConfigDict(extra="forbid")

    student_data_telephone: str = Field(
        ...,
        description='Student telephone.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    supervisor_data_subject_area: str = Field(
        ...,
        description='Supervisor subject area.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )


    expose_text: str = Field(
        ...,
        description='Thesis exposé text (max 3500 keystrokes).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )