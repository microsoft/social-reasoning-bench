from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProjectLeadAgencyInformation(BaseModel):
    """Basic project identification and lead agency contact details"""

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
            "Mailing address of the lead agency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Telephone number for the contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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
            "City or nearest community to the project site .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    zip_code: str = Field(default="", description="ZIP code for the project location")

    cross_streets: str = Field(
        default="",
        description=(
            "Major cross streets near the project site .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    longitude_n_degrees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Degrees component of the north latitude coordinate"
    )

    longitude_n_minutes: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minutes component of the north latitude coordinate"
    )

    longitude_n_seconds: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Seconds component of the north latitude coordinate"
    )

    longitude_w_degrees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Degrees component of the west longitude coordinate"
    )

    longitude_w_minutes: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minutes component of the west longitude coordinate"
    )

    longitude_w_seconds: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Seconds component of the west longitude coordinate"
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
            "Section number for the project’s legal description .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    twp: str = Field(
        default="",
        description=(
            "Township designation for the project’s legal description .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    range: str = Field(
        default="",
        description=(
            "Range designation for the project’s legal description .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    base: str = Field(
        default="",
        description=(
            "Base meridian for the project’s legal description .If you cannot fill this, "
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
    """Type of CEQA/NEPA environmental document and related identifiers"""

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
        default="", description="Check if the document type is a NEPA final document"
    )

    ceqa_neg_dec: BooleanLike = Field(
        default="",
        description="Check if the document type is a CEQA Negative Declaration (Neg Dec)",
    )

    prior_sch_no: str = Field(
        default="",
        description=(
            "Prior State Clearinghouse number associated with this project, if any .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
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
            "Specify other NEPA document type, if 'Other' is selected .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ceqa_mit_neg_dec: BooleanLike = Field(
        default="",
        description=(
            "Check if the document type is a CEQA Mitigated Negative Declaration (Mit Neg Dec)"
        ),
    )

    ceqa_other_document_type: str = Field(
        default="",
        description=(
            "Specify other CEQA document type, if 'Other' is selected .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    nepa_fonsi: BooleanLike = Field(
        default="",
        description="Check if the document type is a NEPA Finding of No Significant Impact (FONSI)",
    )


class LocalActionType(BaseModel):
    """Local planning and permitting actions associated with the project"""

    local_action_type_general_plan_update: BooleanLike = Field(
        default="", description="Indicate if the project involves a General Plan Update"
    )

    local_action_type_specific_plan: BooleanLike = Field(
        default="", description="Indicate if the project involves a Specific Plan"
    )

    local_action_type_rezone: BooleanLike = Field(
        default="", description="Indicate if the project involves a Rezone"
    )

    local_action_type_annexation: BooleanLike = Field(
        default="", description="Indicate if the project involves an Annexation"
    )

    local_action_type_general_plan_amendment: BooleanLike = Field(
        default="", description="Indicate if the project involves a General Plan Amendment"
    )

    local_action_type_master_plan: BooleanLike = Field(
        default="", description="Indicate if the project involves a Master Plan"
    )

    local_action_type_prezoning: BooleanLike = Field(
        default="", description="Indicate if the project involves Prezoning"
    )

    local_action_type_redevelopment: BooleanLike = Field(
        default="", description="Indicate if the project involves Redevelopment"
    )

    local_action_type_general_plan_element: BooleanLike = Field(
        default="", description="Indicate if the project involves a General Plan Element"
    )

    local_action_type_planned_unit_development: BooleanLike = Field(
        default="", description="Indicate if the project involves a Planned Unit Development"
    )

    local_action_type_use_permit: BooleanLike = Field(
        default="", description="Indicate if the project involves a Use Permit"
    )

    local_action_type_coastal_permit: BooleanLike = Field(
        default="", description="Indicate if the project involves a Coastal Permit"
    )

    local_action_type_community_plan: BooleanLike = Field(
        default="", description="Indicate if the project involves a Community Plan"
    )

    local_action_type_site_plan: BooleanLike = Field(
        default="", description="Indicate if the project involves a Site Plan"
    )

    local_action_type_land_division_subdivision_etc: BooleanLike = Field(
        default="",
        description="Indicate if the project involves a Land Division, such as a subdivision",
    )

    local_action_type_other: str = Field(
        default="",
        description=(
            "Describe other local action types not listed above .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class DevelopmentType(BaseModel):
    """Type and scale of proposed development"""

    development_type_residential: BooleanLike = Field(
        default="", description="Check if the project includes residential development"
    )

    residential_units: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of residential units proposed"
    )

    residential_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of residential development"
    )

    development_type_office: BooleanLike = Field(
        default="", description="Check if the project includes office development"
    )

    office_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total square footage of office space"
    )

    office_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of office development"
    )

    office_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with office development"
    )

    development_type_commercial: BooleanLike = Field(
        default="", description="Check if the project includes commercial development"
    )

    commercial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total square footage of commercial space"
    )

    commercial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of commercial development"
    )

    commercial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with commercial development"
    )

    development_type_industrial: BooleanLike = Field(
        default="", description="Check if the project includes industrial development"
    )

    industrial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total square footage of industrial space"
    )

    industrial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of industrial development"
    )

    industrial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with industrial development"
    )

    development_type_educational: BooleanLike = Field(
        default="", description="Check if the project includes educational facilities"
    )

    development_type_recreational: BooleanLike = Field(
        default="", description="Check if the project includes recreational facilities"
    )

    development_type_water_facilities: BooleanLike = Field(
        default="", description="Check if the project includes water facilities"
    )

    water_facilities_type: str = Field(
        default="",
        description=(
            'Type of water facilities proposed .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    water_facilities_mgd: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Capacity of water facilities in million gallons per day (MGD)"
    )

    development_type_transportation: BooleanLike = Field(
        default="",
        description="Check if the project includes transportation facilities or improvements",
    )

    transportation_type: str = Field(
        default="",
        description=(
            "Type of transportation facilities or improvements .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    development_type_mining: BooleanLike = Field(
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

    development_type_power: BooleanLike = Field(
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
        default="", description="Power generation capacity in megawatts (MW)"
    )

    development_type_waste_treatment: BooleanLike = Field(
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

    development_type_hazardous_waste: BooleanLike = Field(
        default="",
        description="Check if the project includes hazardous waste facilities or activities",
    )

    hazardous_waste_type: str = Field(
        default="",
        description=(
            "Type of hazardous waste facility or activity .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    development_type_other: str = Field(
        default="",
        description=(
            "Describe other types of development not listed above .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectIssuesDiscussedinDocument(BaseModel):
    """Environmental topics and issues addressed in the document"""

    project_issues_aesthetic_visual: BooleanLike = Field(
        default="",
        description="Indicate if aesthetic or visual impacts are discussed in the document",
    )

    project_issues_fiscal: BooleanLike = Field(
        default="", description="Indicate if fiscal impacts are discussed in the document"
    )

    project_issues_recreation_parks: BooleanLike = Field(
        default="",
        description="Indicate if recreation or parks impacts are discussed in the document",
    )

    project_issues_vegetation: BooleanLike = Field(
        default="", description="Indicate if vegetation impacts are discussed in the document"
    )

    project_issues_agricultural_land: BooleanLike = Field(
        default="",
        description="Indicate if agricultural land impacts are discussed in the document",
    )

    project_issues_flood_plain_flooding: BooleanLike = Field(
        default="",
        description="Indicate if flood plain or flooding impacts are discussed in the document",
    )

    project_issues_schools_universities: BooleanLike = Field(
        default="",
        description="Indicate if impacts to schools or universities are discussed in the document",
    )

    project_issues_water_quality: BooleanLike = Field(
        default="", description="Indicate if water quality impacts are discussed in the document"
    )

    project_issues_air_quality: BooleanLike = Field(
        default="", description="Indicate if air quality impacts are discussed in the document"
    )

    project_issues_forest_land_fire_hazard: BooleanLike = Field(
        default="",
        description="Indicate if forest land or fire hazard impacts are discussed in the document",
    )

    project_issues_septic_systems: BooleanLike = Field(
        default="", description="Indicate if septic system impacts are discussed in the document"
    )

    project_issues_water_supply_groundwater: BooleanLike = Field(
        default="",
        description="Indicate if water supply or groundwater impacts are discussed in the document",
    )

    project_issues_archeological_historical: BooleanLike = Field(
        default="",
        description=(
            "Indicate if archeological or historical resource impacts are discussed in the document"
        ),
    )

    project_issues_geologic_seismic: BooleanLike = Field(
        default="",
        description="Indicate if geologic or seismic impacts are discussed in the document",
    )

    project_issues_sewer_capacity: BooleanLike = Field(
        default="", description="Indicate if sewer capacity impacts are discussed in the document"
    )

    project_issues_wetland_riparian: BooleanLike = Field(
        default="",
        description="Indicate if wetland or riparian impacts are discussed in the document",
    )

    project_issues_biological_resources: BooleanLike = Field(
        default="",
        description="Indicate if biological resource impacts are discussed in the document",
    )

    project_issues_minerals: BooleanLike = Field(
        default="", description="Indicate if mineral resource impacts are discussed in the document"
    )

    project_issues_soil_erosion_compaction_grading: BooleanLike = Field(
        default="",
        description=(
            "Indicate if soil erosion, compaction, or grading impacts are discussed in the document"
        ),
    )

    project_issues_growth_inducement: BooleanLike = Field(
        default="", description="Indicate if growth-inducing impacts are discussed in the document"
    )

    project_issues_coastal_zone: BooleanLike = Field(
        default="", description="Indicate if coastal zone impacts are discussed in the document"
    )

    project_issues_noise: BooleanLike = Field(
        default="", description="Indicate if noise impacts are discussed in the document"
    )

    project_issues_solid_waste: BooleanLike = Field(
        default="", description="Indicate if solid waste impacts are discussed in the document"
    )

    project_issues_land_use: BooleanLike = Field(
        default="", description="Indicate if land use impacts are discussed in the document"
    )

    project_issues_drainage_absorption: BooleanLike = Field(
        default="",
        description="Indicate if drainage or absorption impacts are discussed in the document",
    )

    project_issues_population_housing_balance: BooleanLike = Field(
        default="",
        description="Indicate if population or housing balance impacts are discussed in the document",
    )

    project_issues_toxic_hazardous: BooleanLike = Field(
        default="",
        description="Indicate if toxic or hazardous materials impacts are discussed in the document",
    )

    project_issues_cumulative_effects: BooleanLike = Field(
        default="", description="Indicate if cumulative impacts are discussed in the document"
    )

    project_issues_economic_jobs: BooleanLike = Field(
        default="",
        description="Indicate if economic or jobs-related impacts are discussed in the document",
    )

    project_issues_public_services_facilities: BooleanLike = Field(
        default="",
        description="Indicate if public services or facilities impacts are discussed in the document",
    )

    project_issues_traffic_circulation: BooleanLike = Field(
        default="",
        description="Indicate if traffic or circulation impacts are discussed in the document",
    )

    project_issues_other: str = Field(
        default="",
        description=(
            "Describe other project issues discussed in the document .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class LandUseProjectDescription(BaseModel):
    """Existing land use designations and narrative project description"""

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

    project__lead_agency_information: ProjectLeadAgencyInformation = Field(
        ..., description="Project & Lead Agency Information"
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
