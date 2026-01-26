from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProjectIdentificationLeadAgency(BaseModel):
    """Basic project identifiers and lead agency contact information"""

    sch_number: str = Field(
        default="",
        description=(
            "Existing State Clearinghouse (SCH) number, if previously assigned .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    project_title: str = Field(
        ...,
        description=(
            'Official title of the project .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    lead_agency: str = Field(
        ...,
        description=(
            "Name of the lead agency responsible for the project .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_person: str = Field(
        ...,
        description=(
            "Primary contact person at the lead agency .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            'Mailing address of the lead agency .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Telephone number for the contact person or lead agency .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            "City of the lead agency mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    zip: str = Field(..., description="ZIP code for the lead agency mailing address")

    county: str = Field(
        ...,
        description=(
            "County of the lead agency mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectLocation(BaseModel):
    """Geographic location and nearby features"""

    project_location_county: str = Field(
        ...,
        description=(
            'County where the project is located .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    project_location_city_nearest_community: str = Field(
        ...,
        description=(
            "City or nearest community to the project location .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    cross_streets: str = Field(
        default="",
        description=(
            "Major cross streets near the project site .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    zip_code: str = Field(default="", description="ZIP code for the project location")

    longitude_degrees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Longitude degrees of the project location"
    )

    longitude_minutes: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Longitude minutes of the project location"
    )

    longitude_seconds: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Longitude seconds of the project location"
    )

    latitude_degrees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Latitude degrees of the project location"
    )

    latitude_minutes: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Latitude minutes of the project location"
    )

    latitude_seconds: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Latitude seconds of the project location"
    )

    total_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total acreage of the project site"
    )

    assessors_parcel_no: str = Field(
        default="",
        description=(
            "Assessor’s parcel number(s) for the project site .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    section: str = Field(
        default="",
        description=(
            "Survey section for the project location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    twp: str = Field(
        default="",
        description=(
            "Township designation for the project location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    range: str = Field(
        default="",
        description=(
            "Range designation for the project location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    base: str = Field(
        default="",
        description=(
            "Base meridian reference for the project location .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_state_hwy_number: str = Field(
        default="",
        description=(
            "State highway numbers within 2 miles of the project .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_waterways: str = Field(
        default="",
        description=(
            "Waterways within 2 miles of the project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_airports: str = Field(
        default="",
        description=(
            "Airports within 2 miles of the project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_railways: str = Field(
        default="",
        description=(
            "Railways within 2 miles of the project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_schools: str = Field(
        default="",
        description=(
            'Schools within 2 miles of the project .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class DocumentType(BaseModel):
    """Type of CEQA/NEPA environmental document being filed"""

    ceqa_nop: BooleanLike = Field(
        default="", description="Check if the document type is a CEQA Notice of Preparation (NOP)"
    )

    ceqa_draft_eir: BooleanLike = Field(
        default="",
        description=(
            "Check if the document type is a CEQA Draft Environmental Impact Report (Draft EIR)"
        ),
    )

    nepa_noi: BooleanLike = Field(
        default="", description="Check if the document type is a NEPA Notice of Intent (NOI)"
    )

    other_joint_document: BooleanLike = Field(
        default="",
        description="Check if the document is a joint CEQA/NEPA or similar joint document",
    )

    ceqa_early_cons: BooleanLike = Field(
        default="", description="Check if the document type is a CEQA Early Consultation"
    )

    ceqa_supplement_subsequent_eir: BooleanLike = Field(
        default="", description="Check if the document type is a CEQA Supplement or Subsequent EIR"
    )

    nepa_ea: BooleanLike = Field(
        default="", description="Check if the document type is a NEPA Environmental Assessment (EA)"
    )

    nepa_final_document: BooleanLike = Field(
        default="", description="Check if the document is a NEPA final document"
    )

    ceqa_neg_dec_prior_sch_no: str = Field(
        default="",
        description=(
            "Check if CEQA Negative Declaration and provide prior SCH number if applicable "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    nepa_draft_eis: BooleanLike = Field(
        default="",
        description=(
            "Check if the document type is a NEPA Draft Environmental Impact Statement (Draft EIS)"
        ),
    )

    nepa_other: str = Field(
        default="",
        description=(
            "Specify other NEPA document type, if checked .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ceqa_mit_neg_dec: BooleanLike = Field(
        default="",
        description="Check if the document type is a CEQA Mitigated Negative Declaration",
    )

    ceqa_other: str = Field(
        default="",
        description=(
            "Specify other CEQA document type, if checked .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    nepa_fonsi: str = Field(
        default="",
        description=(
            "Check if NEPA Finding of No Significant Impact (FONSI) and provide any "
            'identifier if applicable .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class LocalActionType(BaseModel):
    """Local planning and permitting actions associated with the project"""

    general_plan_update: BooleanLike = Field(
        default="", description="Indicate if the local action type includes a General Plan Update"
    )

    specific_plan: BooleanLike = Field(
        default="", description="Indicate if the local action type includes a Specific Plan"
    )

    rezone: BooleanLike = Field(
        default="", description="Indicate if the local action type includes a Rezone"
    )

    annexation: BooleanLike = Field(
        default="", description="Indicate if the local action type includes an Annexation"
    )

    general_plan_amendment: BooleanLike = Field(
        default="",
        description="Indicate if the local action type includes a General Plan Amendment",
    )

    master_plan: BooleanLike = Field(
        default="", description="Indicate if the local action type includes a Master Plan"
    )

    prezone: BooleanLike = Field(
        default="", description="Indicate if the local action type includes a Prezone"
    )

    redevelopment: BooleanLike = Field(
        default="", description="Indicate if the local action type includes Redevelopment"
    )

    general_plan_element: BooleanLike = Field(
        default="", description="Indicate if the local action type includes a General Plan Element"
    )

    planned_unit_development: BooleanLike = Field(
        default="",
        description="Indicate if the local action type includes a Planned Unit Development",
    )

    use_permit: BooleanLike = Field(
        default="", description="Indicate if the local action type includes a Use Permit"
    )

    coastal_permit: BooleanLike = Field(
        default="", description="Indicate if the local action type includes a Coastal Permit"
    )

    community_plan: BooleanLike = Field(
        default="", description="Indicate if the local action type includes a Community Plan"
    )

    site_plan: BooleanLike = Field(
        default="", description="Indicate if the local action type includes a Site Plan"
    )

    land_division_subdivision_etc: BooleanLike = Field(
        default="",
        description="Indicate if the local action type includes Land Division (Subdivision, etc.)",
    )

    local_action_type_other: str = Field(
        default="",
        description=(
            "Specify other local action type, if checked .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class DevelopmentType(BaseModel):
    """Nature and scale of proposed development"""

    residential: BooleanLike = Field(
        default="", description="Check if the project includes residential development"
    )

    residential_units: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of residential units proposed"
    )

    residential_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of residential development"
    )

    transportation: BooleanLike = Field(
        default="", description="Check if the project includes transportation facilities"
    )

    transportation_type: str = Field(
        default="",
        description=(
            "Type of transportation project (e.g., road, rail, transit) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    office: BooleanLike = Field(
        default="", description="Check if the project includes office development"
    )

    office_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of office space"
    )

    office_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of office development"
    )

    office_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with office development"
    )

    mining: BooleanLike = Field(
        default="", description="Check if the project includes mining activities"
    )

    mining_mineral: str = Field(
        default="",
        description=(
            'Type of mineral to be extracted .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    commercial: BooleanLike = Field(
        default="", description="Check if the project includes commercial development"
    )

    commercial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of commercial space"
    )

    commercial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of commercial development"
    )

    commercial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with commercial development"
    )

    power: BooleanLike = Field(
        default="", description="Check if the project includes power generation facilities"
    )

    power_type: str = Field(
        default="",
        description=(
            "Type of power generation (e.g., solar, wind, gas) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    power_mw: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Megawatt capacity of the power facility"
    )

    industrial: BooleanLike = Field(
        default="", description="Check if the project includes industrial development"
    )

    industrial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of industrial space"
    )

    industrial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of industrial development"
    )

    industrial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with industrial development"
    )

    waste_treatment: BooleanLike = Field(
        default="", description="Check if the project includes waste treatment facilities"
    )

    waste_treatment_type: str = Field(
        default="",
        description=(
            'Type of waste treatment facility .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    waste_treatment_mgd: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Capacity of waste treatment facility in million gallons per day (MGD)",
    )

    educational: BooleanLike = Field(
        default="", description="Check if the project includes educational facilities"
    )

    recreational: BooleanLike = Field(
        default="", description="Check if the project includes recreational facilities"
    )

    hazardous_waste: BooleanLike = Field(
        default="",
        description="Check if the project includes hazardous waste facilities or activities",
    )

    hazardous_waste_type: str = Field(
        default="",
        description=(
            'Type of hazardous waste involved .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    other_development_type: str = Field(
        default="",
        description=(
            "Specify any other type of development not listed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    water_facilities: BooleanLike = Field(
        default="", description="Check if the project includes water facilities"
    )

    water_facilities_type: str = Field(
        default="",
        description=(
            "Type of water facilities (e.g., treatment plant, pipeline) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    water_facilities_mgd: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Capacity of water facilities in million gallons per day (MGD)"
    )


class ProjectIssuesDiscussedinDocument(BaseModel):
    """Environmental topics and issues addressed in the document"""

    aesthetic_visual: BooleanLike = Field(
        default="", description="Indicate if aesthetic/visual issues are discussed in the document"
    )

    fiscal: BooleanLike = Field(
        default="", description="Indicate if fiscal issues are discussed in the document"
    )

    recreation_parks: BooleanLike = Field(
        default="", description="Indicate if recreation/parks issues are discussed in the document"
    )

    vegetation: BooleanLike = Field(
        default="", description="Indicate if vegetation issues are discussed in the document"
    )

    agricultural_land: BooleanLike = Field(
        default="", description="Indicate if agricultural land issues are discussed in the document"
    )

    flood_plain_flooding: BooleanLike = Field(
        default="",
        description="Indicate if flood plain/flooding issues are discussed in the document",
    )

    schools_universities: BooleanLike = Field(
        default="",
        description="Indicate if schools/universities issues are discussed in the document",
    )

    water_quality: BooleanLike = Field(
        default="", description="Indicate if water quality issues are discussed in the document"
    )

    air_quality: BooleanLike = Field(
        default="", description="Indicate if air quality issues are discussed in the document"
    )

    forest_land_fire_hazard: BooleanLike = Field(
        default="",
        description="Indicate if forest land or fire hazard issues are discussed in the document",
    )

    septic_systems: BooleanLike = Field(
        default="", description="Indicate if septic systems issues are discussed in the document"
    )

    water_supply_groundwater: BooleanLike = Field(
        default="",
        description="Indicate if water supply/groundwater issues are discussed in the document",
    )

    archeological_historical: BooleanLike = Field(
        default="",
        description="Indicate if archeological/historical issues are discussed in the document",
    )

    geologic_seismic: BooleanLike = Field(
        default="", description="Indicate if geologic/seismic issues are discussed in the document"
    )

    sewer_capacity: BooleanLike = Field(
        default="", description="Indicate if sewer capacity issues are discussed in the document"
    )

    wetland_riparian: BooleanLike = Field(
        default="", description="Indicate if wetland/riparian issues are discussed in the document"
    )

    biological_resources: BooleanLike = Field(
        default="",
        description="Indicate if biological resources issues are discussed in the document",
    )

    minerals: BooleanLike = Field(
        default="", description="Indicate if minerals issues are discussed in the document"
    )

    soil_erosion_compaction_grading: BooleanLike = Field(
        default="",
        description=(
            "Indicate if soil erosion/compaction/grading issues are discussed in the document"
        ),
    )

    growth_inducement: BooleanLike = Field(
        default="", description="Indicate if growth inducement issues are discussed in the document"
    )

    coastal_zone: BooleanLike = Field(
        default="", description="Indicate if coastal zone issues are discussed in the document"
    )

    noise: BooleanLike = Field(
        default="", description="Indicate if noise issues are discussed in the document"
    )

    solid_waste: BooleanLike = Field(
        default="", description="Indicate if solid waste issues are discussed in the document"
    )

    land_use: BooleanLike = Field(
        default="", description="Indicate if land use issues are discussed in the document"
    )

    drainage_absorption: BooleanLike = Field(
        default="",
        description="Indicate if drainage/absorption issues are discussed in the document",
    )

    population_housing_balance: BooleanLike = Field(
        default="",
        description="Indicate if population/housing balance issues are discussed in the document",
    )

    toxic_hazardous: BooleanLike = Field(
        default="", description="Indicate if toxic/hazardous issues are discussed in the document"
    )

    cumulative_effects: BooleanLike = Field(
        default="", description="Indicate if cumulative effects are discussed in the document"
    )

    economic_jobs: BooleanLike = Field(
        default="", description="Indicate if economic/jobs issues are discussed in the document"
    )

    public_services_facilities: BooleanLike = Field(
        default="",
        description="Indicate if public services/facilities issues are discussed in the document",
    )

    traffic_circulation: BooleanLike = Field(
        default="",
        description="Indicate if traffic/circulation issues are discussed in the document",
    )

    other_project_issues: str = Field(
        default="",
        description=(
            "Specify any other project issues discussed in the document .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class LandUseProjectDescription(BaseModel):
    """Existing land use designations and narrative project description"""

    present_land_use_zoning_general_plan_designation: str = Field(
        default="",
        description=(
            "Current land use, zoning, and general plan designation for the project site "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    project_description: str = Field(
        ...,
        description=(
            "Detailed description of the proposed project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class NoticeOfCompletionEnvironmentalDocumentTransmittal(BaseModel):
    """
    Notice of Completion & Environmental Document Transmittal

    Note: The State Clearinghouse will assign identification numbers for all new projects. If a SCH number already exists for a project (e.g. Notice of Preparation or previous draft document) please fill in.
    """

    project_identification__lead_agency: ProjectIdentificationLeadAgency = Field(
        ..., description="Project Identification & Lead Agency"
    )
    project_location: ProjectLocation = Field(..., description="Project Location")
    document_type: DocumentType = Field(..., description="Document Type")
    local_action_type: LocalActionType = Field(..., description="Local Action Type")
    development_type: DevelopmentType = Field(..., description="Development Type")
    project_issues_discussed_in_document: ProjectIssuesDiscussedinDocument = Field(
        ..., description="Project Issues Discussed in Document"
    )
    land_use__project_description: LandUseProjectDescription = Field(
        ..., description="Land Use & Project Description"
    )
