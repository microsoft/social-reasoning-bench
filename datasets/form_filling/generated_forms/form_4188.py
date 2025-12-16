from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProjectandLeadAgencyInformation(BaseModel):
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
            "Name of the lead agency responsible for the environmental document .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
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
    """Geographic location and nearby features of the project"""

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
            "City or nearest community to the project site .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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

    zip_code: str = Field(default="", description="ZIP code for the project location")

    longitude_degrees_n: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Degrees portion of the project longitude (north coordinate)"
    )

    longitude_minutes_n: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minutes portion of the project longitude (north coordinate)"
    )

    longitude_seconds_n: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Seconds portion of the project longitude (north coordinate)"
    )

    latitude_degrees_w: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Degrees portion of the project latitude (west coordinate)"
    )

    latitude_minutes_w: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minutes portion of the project latitude (west coordinate)"
    )

    latitude_seconds_w: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Seconds portion of the project latitude (west coordinate)"
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
            "Section number for the project location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    twp: str = Field(
        default="",
        description=(
            "Township (TWP.) designation for the project location .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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
            "State highway numbers within 2 miles of the project site .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_waterways: str = Field(
        default="",
        description=(
            "Waterways within 2 miles of the project site .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_airports: str = Field(
        default="",
        description=(
            "Airports within 2 miles of the project site .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_railways: str = Field(
        default="",
        description=(
            "Railways within 2 miles of the project site .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    within_2_miles_schools: str = Field(
        default="",
        description=(
            "Schools within 2 miles of the project site .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class DocumentType(BaseModel):
    """Type of environmental document under CEQA and/or NEPA"""

    ceqa_nop: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Notice of Preparation (NOP)"
    )

    ceqa_draft_eir: BooleanLike = Field(
        default="",
        description=(
            "Check if the CEQA document type is Draft Environmental Impact Report (Draft EIR)"
        ),
    )

    ceqa_early_cons: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Early Consultation"
    )

    ceqa_supplement_subsequent_eir: BooleanLike = Field(
        default="", description="Check if the CEQA document type is a Supplement or Subsequent EIR"
    )

    ceqa_neg_dec: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Negative Declaration (Neg Dec)"
    )

    ceqa_mit_neg_dec: BooleanLike = Field(
        default="",
        description="Check if the CEQA document type is Mitigated Negative Declaration (Mit Neg Dec)",
    )

    ceqa_other: str = Field(
        default="",
        description=(
            "Specify other CEQA document type, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    nepa_noi: BooleanLike = Field(
        default="", description="Check if the NEPA document type is Notice of Intent (NOI)"
    )

    nepa_ea: BooleanLike = Field(
        default="", description="Check if the NEPA document type is Environmental Assessment (EA)"
    )

    nepa_draft_eis: BooleanLike = Field(
        default="",
        description=(
            "Check if the NEPA document type is Draft Environmental Impact Statement (Draft EIS)"
        ),
    )

    nepa_fonsi: BooleanLike = Field(
        default="",
        description="Check if the NEPA document type is Finding of No Significant Impact (FONSI)",
    )

    nepa_other: str = Field(
        default="",
        description=(
            "Specify other NEPA document type, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    joint_document: BooleanLike = Field(
        default="", description="Check if the CEQA and NEPA documents are joint"
    )

    final_document: BooleanLike = Field(
        default="", description="Check if this is a final environmental document"
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
        default="", description="Check if the project involves a General Plan Element"
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
        default="", description="Check if the project involves a Coastal Permit"
    )

    local_action_other: str = Field(
        default="",
        description=(
            "Describe any other local action type not listed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class DevelopmentType(BaseModel):
    """Characteristics and scale of proposed development"""

    development_residential_units: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of residential units proposed"
    )

    development_residential_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of residential development"
    )

    development_office_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of office development"
    )

    development_office_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of office development"
    )

    development_office_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with office development"
    )

    development_commercial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of commercial development"
    )

    development_commercial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of commercial development"
    )

    development_commercial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with commercial development"
    )

    development_industrial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of industrial development"
    )

    development_industrial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of industrial development"
    )

    development_industrial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with industrial development"
    )

    development_educational: str = Field(
        default="",
        description=(
            "Description or size of educational development .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    development_recreational: str = Field(
        default="",
        description=(
            "Description or size of recreational development .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    development_water_facilities_type: str = Field(
        default="",
        description=(
            'Type of water facilities proposed .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    development_water_facilities_mgd: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Capacity of water facilities in million gallons per day (MGD)"
    )

    development_transportation_type: str = Field(
        default="",
        description=(
            "Type of transportation facilities proposed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    development_mining_mineral: str = Field(
        default="",
        description=(
            'Type of mineral to be mined .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    development_power_type: str = Field(
        default="",
        description=(
            'Type of power facility proposed .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    development_power_mw: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Power generation capacity in megawatts (MW)"
    )

    development_waste_treatment_type: str = Field(
        default="",
        description=(
            "Type of waste treatment facility proposed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    development_waste_treatment_mgd: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Capacity of waste treatment facility in million gallons per day (MGD)",
    )

    development_hazardous_waste_type: str = Field(
        default="",
        description=(
            "Type of hazardous waste facility or materials involved .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    development_other: str = Field(
        default="",
        description=(
            "Description of any other type of development not listed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectIssuesDiscussedinDocument(BaseModel):
    """Environmental topics and issues addressed in the document"""

    project_issues_aesthetic_visual: BooleanLike = Field(
        default="",
        description="Indicate if aesthetic or visual impacts are discussed in the document",
    )

    project_issues_agricultural_land: BooleanLike = Field(
        default="", description="Indicate if agricultural land impacts are discussed"
    )

    project_issues_air_quality: BooleanLike = Field(
        default="", description="Indicate if air quality impacts are discussed"
    )

    project_issues_archeological_historical: BooleanLike = Field(
        default="", description="Indicate if archeological or historical resources are discussed"
    )

    project_issues_biological_resources: BooleanLike = Field(
        default="", description="Indicate if biological resources are discussed"
    )

    project_issues_coastal_zone: BooleanLike = Field(
        default="", description="Indicate if coastal zone issues are discussed"
    )

    project_issues_drainage_absorption: BooleanLike = Field(
        default="", description="Indicate if drainage or absorption issues are discussed"
    )

    project_issues_economic_jobs: BooleanLike = Field(
        default="", description="Indicate if economic or jobs impacts are discussed"
    )

    project_issues_fiscal: BooleanLike = Field(
        default="", description="Indicate if fiscal impacts are discussed"
    )

    project_issues_flood_plain_flooding: BooleanLike = Field(
        default="", description="Indicate if flood plain or flooding issues are discussed"
    )

    project_issues_forest_land_fire_hazard: BooleanLike = Field(
        default="", description="Indicate if forest land or fire hazard issues are discussed"
    )

    project_issues_geologic_seismic: BooleanLike = Field(
        default="", description="Indicate if geologic or seismic issues are discussed"
    )

    project_issues_minerals: BooleanLike = Field(
        default="", description="Indicate if mineral resources are discussed"
    )

    project_issues_noise: BooleanLike = Field(
        default="", description="Indicate if noise impacts are discussed"
    )

    project_issues_population_housing_balance: BooleanLike = Field(
        default="", description="Indicate if population or housing balance issues are discussed"
    )

    project_issues_public_services_facilities: BooleanLike = Field(
        default="", description="Indicate if public services or facilities impacts are discussed"
    )

    project_issues_recreation_parks: BooleanLike = Field(
        default="", description="Indicate if recreation or parks impacts are discussed"
    )

    project_issues_schools_universities: BooleanLike = Field(
        default="", description="Indicate if schools or universities impacts are discussed"
    )

    project_issues_septic_systems: BooleanLike = Field(
        default="", description="Indicate if septic system issues are discussed"
    )

    project_issues_sewer_capacity: BooleanLike = Field(
        default="", description="Indicate if sewer capacity issues are discussed"
    )

    project_issues_soil_erosion_compaction_grading: BooleanLike = Field(
        default="",
        description="Indicate if soil erosion, compaction, or grading issues are discussed",
    )

    project_issues_solid_waste: BooleanLike = Field(
        default="", description="Indicate if solid waste issues are discussed"
    )

    project_issues_toxic_hazardous: BooleanLike = Field(
        default="", description="Indicate if toxic or hazardous materials issues are discussed"
    )

    project_issues_traffic_circulation: BooleanLike = Field(
        default="", description="Indicate if traffic or circulation impacts are discussed"
    )

    project_issues_vegetation: BooleanLike = Field(
        default="", description="Indicate if vegetation impacts are discussed"
    )

    project_issues_water_quality: BooleanLike = Field(
        default="", description="Indicate if water quality impacts are discussed"
    )

    project_issues_water_supply_groundwater: BooleanLike = Field(
        default="", description="Indicate if water supply or groundwater impacts are discussed"
    )

    project_issues_wetland_riparian: BooleanLike = Field(
        default="", description="Indicate if wetland or riparian impacts are discussed"
    )

    project_issues_growth_inducement: BooleanLike = Field(
        default="", description="Indicate if growth-inducing impacts are discussed"
    )

    project_issues_land_use: BooleanLike = Field(
        default="", description="Indicate if land use impacts are discussed"
    )

    project_issues_cumulative_effects: BooleanLike = Field(
        default="", description="Indicate if cumulative effects are discussed"
    )

    project_issues_other: str = Field(
        default="",
        description=(
            "Describe any other project issues discussed in the document .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ExistingLandUseandProjectDescription(BaseModel):
    """Current land use designations and narrative description of the project"""

    present_land_use_zoning_general_plan_designation: str = Field(
        default="",
        description=(
            "Describe the current land use, zoning, and general plan designation of the "
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

    ''
    """

    project_and_lead_agency_information: ProjectandLeadAgencyInformation = Field(
        ..., description="Project and Lead Agency Information"
    )
    project_location: ProjectLocation = Field(..., description="Project Location")
    document_type: DocumentType = Field(..., description="Document Type")
    local_action_type: LocalActionType = Field(..., description="Local Action Type")
    development_type: DevelopmentType = Field(..., description="Development Type")
    project_issues_discussed_in_document: ProjectIssuesDiscussedinDocument = Field(
        ..., description="Project Issues Discussed in Document"
    )
    existing_land_use_and_project_description: ExistingLandUseandProjectDescription = Field(
        ..., description="Existing Land Use and Project Description"
    )
