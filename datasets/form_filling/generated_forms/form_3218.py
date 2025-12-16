from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProjectandAgencyInformation(BaseModel):
    """Basic project identification and lead agency contact details"""

    sch_number: str = Field(
        default="",
        description=(
            "State Clearinghouse identification number, if already assigned .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
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
            "Primary contact person for the lead agency regarding this project .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
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
    """Location details and nearby features"""

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
            "Major cross streets near the project location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    project_location_zip_code: str = Field(
        default="", description="ZIP code for the project location"
    )

    latitude_degrees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Degrees portion of the project latitude (N)"
    )

    latitude_minutes: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minutes portion of the project latitude (N)"
    )

    latitude_seconds: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Seconds portion of the project latitude (N)"
    )

    longitude_degrees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Degrees portion of the project longitude (W)"
    )

    longitude_minutes: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minutes portion of the project longitude (W)"
    )

    longitude_seconds: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Seconds portion of the project longitude (W)"
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
            "Section number for the project location (public land survey) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
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
            "Base meridian for the project location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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
    """Type of environmental document under CEQA/NEPA and related classifications"""

    ceqa_nop: BooleanLike = Field(
        default="", description="Check if a CEQA Notice of Preparation (NOP) is the document type"
    )

    ceqa_draft_eir: BooleanLike = Field(
        default="",
        description=(
            "Check if a CEQA Draft Environmental Impact Report (Draft EIR) is the document type"
        ),
    )

    ceqa_early_cons: BooleanLike = Field(
        default="", description="Check if a CEQA Early Consultation document is included"
    )

    ceqa_supplement_subsequent_eir: BooleanLike = Field(
        default="", description="Check if a CEQA Supplement or Subsequent EIR is the document type"
    )

    ceqa_prior_sch_no: str = Field(
        default="",
        description=(
            "Prior State Clearinghouse number for related CEQA documents .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    ceqa_neg_dec: BooleanLike = Field(
        default="", description="Check if a CEQA Negative Declaration is the document type"
    )

    ceqa_mit_neg_dec: BooleanLike = Field(
        default="",
        description="Check if a CEQA Mitigated Negative Declaration is the document type",
    )

    ceqa_other: str = Field(
        default="",
        description=(
            'Describe any other CEQA document type .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    nepa_noi: BooleanLike = Field(
        default="", description="Check if a NEPA Notice of Intent (NOI) is the document type"
    )

    nepa_ea: BooleanLike = Field(
        default="", description="Check if a NEPA Environmental Assessment (EA) is the document type"
    )

    nepa_draft_eis: BooleanLike = Field(
        default="",
        description=(
            "Check if a NEPA Draft Environmental Impact Statement (Draft EIS) is the document type"
        ),
    )

    nepa_fonsi: BooleanLike = Field(
        default="",
        description="Check if a NEPA Finding of No Significant Impact (FONSI) is the document type",
    )

    other_joint_document: BooleanLike = Field(
        default="",
        description="Check if the document is a joint CEQA/NEPA or multi-agency document",
    )

    other_final_document: BooleanLike = Field(
        default="", description="Check if the document is a final version"
    )

    other_other_document_type: str = Field(
        default="",
        description=(
            "Describe any other document type not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class LocalActionType(BaseModel):
    """Local planning and permitting actions associated with the project"""

    local_action_general_plan_update: BooleanLike = Field(
        default="", description="Check if the project involves a General Plan Update"
    )

    local_action_general_plan_amendment: BooleanLike = Field(
        default="", description="Check if the project involves a General Plan Amendment"
    )

    local_action_general_plan_element: BooleanLike = Field(
        default="", description="Check if the project involves a specific General Plan Element"
    )

    local_action_community_plan: BooleanLike = Field(
        default="", description="Check if the project involves a Community Plan"
    )

    local_action_specific_plan: BooleanLike = Field(
        default="", description="Check if the project involves a Specific Plan"
    )

    local_action_master_plan: BooleanLike = Field(
        default="", description="Check if the project involves a Master Plan"
    )

    local_action_planned_unit_development: BooleanLike = Field(
        default="", description="Check if the project involves a Planned Unit Development"
    )

    local_action_site_plan: BooleanLike = Field(
        default="", description="Check if the project involves a Site Plan"
    )

    local_action_rezone: BooleanLike = Field(
        default="", description="Check if the project involves a Rezone"
    )

    local_action_prezoning: BooleanLike = Field(
        default="", description="Check if the project involves Prezoning"
    )

    local_action_use_permit: BooleanLike = Field(
        default="", description="Check if the project involves a Use Permit"
    )

    local_action_land_division: BooleanLike = Field(
        default="",
        description="Check if the project involves a land division such as a subdivision",
    )

    local_action_annexation: BooleanLike = Field(
        default="", description="Check if the project involves Annexation"
    )

    local_action_redevelopment: BooleanLike = Field(
        default="", description="Check if the project involves Redevelopment"
    )

    local_action_coastal_permit: BooleanLike = Field(
        default="", description="Check if the project requires a Coastal Permit"
    )

    local_action_other: str = Field(
        default="",
        description=(
            'Describe any other local action type .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class DevelopmentType(BaseModel):
    """Type and scale of proposed development"""

    development_residential: BooleanLike = Field(
        default="", description="Check if the project includes residential development"
    )

    residential_units: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of residential units proposed"
    )

    residential_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage devoted to residential use"
    )

    development_office: BooleanLike = Field(
        default="", description="Check if the project includes office development"
    )

    office_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of office space"
    )

    office_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage devoted to office use"
    )

    office_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with office uses"
    )

    development_commercial: BooleanLike = Field(
        default="", description="Check if the project includes commercial development"
    )

    commercial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of commercial space"
    )

    commercial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage devoted to commercial use"
    )

    commercial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with commercial uses"
    )

    development_industrial: BooleanLike = Field(
        default="", description="Check if the project includes industrial development"
    )

    industrial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of industrial space"
    )

    industrial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage devoted to industrial use"
    )

    industrial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with industrial uses"
    )

    development_educational: str = Field(
        default="",
        description=(
            "Describe any educational facilities included in the project .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    development_recreational: str = Field(
        default="",
        description=(
            "Describe any recreational facilities included in the project .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    development_water_facilities_type: str = Field(
        default="",
        description=(
            "Type of water facilities included in the project .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    development_water_facilities_mgd: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Capacity of water facilities in million gallons per day (MGD)"
    )

    development_transportation_type: str = Field(
        default="",
        description=(
            "Type of transportation facilities or improvements included .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    development_mining_mineral: str = Field(
        default="",
        description=(
            "Type of mineral to be extracted in mining operations .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    development_power_type: str = Field(
        default="",
        description=(
            "Type of power generation facility (e.g., solar, wind, gas) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    development_power_mw: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Power generation capacity in megawatts (MW)"
    )

    development_waste_treatment_type: str = Field(
        default="",
        description=(
            'Type of waste treatment facility .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    development_waste_treatment_mgd: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Capacity of waste treatment facilities in million gallons per day (MGD)",
    )

    development_hazardous_waste_type: str = Field(
        default="",
        description=(
            "Type of hazardous waste facility or activity .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    development_other: str = Field(
        default="",
        description=(
            "Describe any other type of development not listed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectIssuesDiscussedinDocument(BaseModel):
    """Environmental topics and issues addressed in the document"""

    project_issues_aesthetic_visual: BooleanLike = Field(
        default="", description="Check if aesthetic or visual impacts are discussed"
    )

    project_issues_agricultural_land: BooleanLike = Field(
        default="", description="Check if agricultural land impacts are discussed"
    )

    project_issues_air_quality: BooleanLike = Field(
        default="", description="Check if air quality impacts are discussed"
    )

    project_issues_archeological_historical: BooleanLike = Field(
        default="", description="Check if archeological or historical resources are discussed"
    )

    project_issues_biological_resources: BooleanLike = Field(
        default="", description="Check if biological resources are discussed"
    )

    project_issues_coastal_zone: BooleanLike = Field(
        default="", description="Check if coastal zone issues are discussed"
    )

    project_issues_drainage_absorption: BooleanLike = Field(
        default="", description="Check if drainage or absorption issues are discussed"
    )

    project_issues_economic_jobs: BooleanLike = Field(
        default="", description="Check if economic or employment impacts are discussed"
    )

    project_issues_fiscal: BooleanLike = Field(
        default="", description="Check if fiscal impacts are discussed"
    )

    project_issues_flood_plain_flooding: BooleanLike = Field(
        default="", description="Check if flood plain or flooding issues are discussed"
    )

    project_issues_forest_land_fire_hazard: BooleanLike = Field(
        default="", description="Check if forest land or fire hazard issues are discussed"
    )

    project_issues_geologic_seismic: BooleanLike = Field(
        default="", description="Check if geologic or seismic issues are discussed"
    )

    project_issues_minerals: BooleanLike = Field(
        default="", description="Check if mineral resources are discussed"
    )

    project_issues_noise: BooleanLike = Field(
        default="", description="Check if noise impacts are discussed"
    )

    project_issues_population_housing_balance: BooleanLike = Field(
        default="", description="Check if population or housing balance issues are discussed"
    )

    project_issues_public_services_facilities: BooleanLike = Field(
        default="", description="Check if public services or facilities impacts are discussed"
    )

    project_issues_recreation_parks: BooleanLike = Field(
        default="", description="Check if recreation or parks impacts are discussed"
    )

    project_issues_schools_universities: BooleanLike = Field(
        default="", description="Check if impacts to schools or universities are discussed"
    )

    project_issues_septic_systems: BooleanLike = Field(
        default="", description="Check if septic system issues are discussed"
    )

    project_issues_sewer_capacity: BooleanLike = Field(
        default="", description="Check if sewer capacity issues are discussed"
    )

    project_issues_soil_erosion_compaction_grading: BooleanLike = Field(
        default="", description="Check if soil erosion, compaction, or grading issues are discussed"
    )

    project_issues_solid_waste: BooleanLike = Field(
        default="", description="Check if solid waste issues are discussed"
    )

    project_issues_toxic_hazardous: BooleanLike = Field(
        default="", description="Check if toxic or hazardous materials issues are discussed"
    )

    project_issues_traffic_circulation: BooleanLike = Field(
        default="", description="Check if traffic or circulation impacts are discussed"
    )

    project_issues_vegetation: BooleanLike = Field(
        default="", description="Check if vegetation impacts are discussed"
    )

    project_issues_water_quality: BooleanLike = Field(
        default="", description="Check if water quality impacts are discussed"
    )

    project_issues_water_supply_groundwater: BooleanLike = Field(
        default="", description="Check if water supply or groundwater impacts are discussed"
    )

    project_issues_wetland_riparian: BooleanLike = Field(
        default="", description="Check if wetland or riparian impacts are discussed"
    )

    project_issues_growth_inducement: BooleanLike = Field(
        default="", description="Check if growth-inducing impacts are discussed"
    )

    project_issues_land_use: BooleanLike = Field(
        default="", description="Check if land use impacts are discussed"
    )

    project_issues_cumulative_effects: BooleanLike = Field(
        default="", description="Check if cumulative effects are discussed"
    )

    project_issues_other: str = Field(
        default="",
        description=(
            "Describe any other project issues discussed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PresentLandUseandProjectDescription(BaseModel):
    """Existing land use designations and narrative description of the project"""

    present_land_use_zoning_gp_designation: str = Field(
        default="",
        description=(
            "Describe the current land use, zoning, and General Plan designation of the "
            'project site .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    project_description: str = Field(
        ...,
        description=(
            "Detailed description of the proposed project; attach additional pages if "
            'necessary .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class NoticeOfCompletionEnvironmentalDocumentTransmittal(BaseModel):
    """
    Notice of Completion & Environmental Document Transmittal

    Note: The State Clearinghouse will assign identification numbers for all new projects. If a SCH number already exists for a project (e.g. Notice of Preparation or previous draft document) please fill it in.
    """

    project_and_agency_information: ProjectandAgencyInformation = Field(
        ..., description="Project and Agency Information"
    )
    project_location: ProjectLocation = Field(..., description="Project Location")
    document_type: DocumentType = Field(..., description="Document Type")
    local_action_type: LocalActionType = Field(..., description="Local Action Type")
    development_type: DevelopmentType = Field(..., description="Development Type")
    project_issues_discussed_in_document: ProjectIssuesDiscussedinDocument = Field(
        ..., description="Project Issues Discussed in Document"
    )
    present_land_use_and_project_description: PresentLandUseandProjectDescription = Field(
        ..., description="Present Land Use and Project Description"
    )
