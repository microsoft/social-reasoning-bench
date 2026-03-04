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
            "Phone number for the contact person or lead agency .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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

    zip: str = Field(..., description="ZIP code of the lead agency mailing address")

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

    project_location_zip_code: str = Field(
        default="", description="ZIP code of the project location"
    )

    cross_streets: str = Field(
        default="",
        description=(
            "Major cross streets near the project site .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    longitude_n_degrees_minutes_seconds: str = Field(
        default="",
        description=(
            "Latitude in degrees, minutes, and seconds (North) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    longitude_w_degrees_minutes_seconds: str = Field(
        default="",
        description=(
            "Longitude in degrees, minutes, and seconds (West) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
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
    """Type of CEQA/NEPA/environmental document being filed"""

    nop: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Notice of Preparation (NOP)"
    )

    early_cons: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Early Consultation"
    )

    neg_dec: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Negative Declaration"
    )

    mit_neg_dec: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Mitigated Negative Declaration"
    )

    draft_eir: BooleanLike = Field(
        default="",
        description="Check if the CEQA document type is Draft Environmental Impact Report (EIR)",
    )

    supplement_subsequent_eir: BooleanLike = Field(
        default="", description="Check if the CEQA document type is a Supplement or Subsequent EIR"
    )

    prior_sch_no: str = Field(
        default="",
        description=(
            "Prior State Clearinghouse number, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_ceqa_document_type: str = Field(
        default="",
        description=(
            "Description of other CEQA document type, if not listed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    noi: BooleanLike = Field(
        default="", description="Check if the NEPA document type is Notice of Intent (NOI)"
    )

    ea: BooleanLike = Field(
        default="", description="Check if the NEPA document type is Environmental Assessment (EA)"
    )

    draft_eis: BooleanLike = Field(
        default="",
        description="Check if the NEPA document type is Draft Environmental Impact Statement (EIS)",
    )

    fonsi: BooleanLike = Field(
        default="",
        description="Check if the NEPA document type is Finding of No Significant Impact (FONSI)",
    )

    joint_document: BooleanLike = Field(
        default="",
        description="Check if the document is a joint CEQA/NEPA or multi-agency document",
    )

    final_document: BooleanLike = Field(
        default="", description="Check if the document is a final version"
    )

    other_nepa_other_document_type: str = Field(
        default="",
        description=(
            "Description of other NEPA or document type, if not listed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class LocalActionType(BaseModel):
    """Local planning and permitting actions associated with the project"""

    general_plan_update: BooleanLike = Field(
        default="", description="Check if the local action type includes a General Plan Update"
    )

    specific_plan: BooleanLike = Field(
        default="", description="Check if the local action type includes a Specific Plan"
    )

    rezone: BooleanLike = Field(
        default="", description="Check if the local action type includes a Rezone"
    )

    annexation: BooleanLike = Field(
        default="", description="Check if the local action type includes an Annexation"
    )

    general_plan_amendment: BooleanLike = Field(
        default="", description="Check if the local action type includes a General Plan Amendment"
    )

    master_plan: BooleanLike = Field(
        default="", description="Check if the local action type includes a Master Plan"
    )

    prezone: BooleanLike = Field(
        default="", description="Check if the local action type includes a Prezone"
    )

    redevelopment: BooleanLike = Field(
        default="", description="Check if the local action type includes Redevelopment"
    )

    general_plan_element: BooleanLike = Field(
        default="", description="Check if the local action type includes a General Plan Element"
    )

    planned_unit_development: BooleanLike = Field(
        default="", description="Check if the local action type includes a Planned Unit Development"
    )

    use_permit: BooleanLike = Field(
        default="", description="Check if the local action type includes a Use Permit"
    )

    coastal_permit: BooleanLike = Field(
        default="", description="Check if the local action type includes a Coastal Permit"
    )

    community_plan: BooleanLike = Field(
        default="", description="Check if the local action type includes a Community Plan"
    )

    site_plan: BooleanLike = Field(
        default="", description="Check if the local action type includes a Site Plan"
    )

    land_division_subdivision_etc: BooleanLike = Field(
        default="",
        description="Check if the local action type includes Land Division (Subdivision, etc.)",
    )

    other_local_action_type: str = Field(
        default="",
        description=(
            "Description of other local action type, if not listed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class DevelopmentType(BaseModel):
    """Nature and scale of proposed development"""

    residential_units: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of residential units proposed"
    )

    residential_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of residential development"
    )

    office_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of office development"
    )

    office_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of office development"
    )

    office_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with office development"
    )

    commercial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of commercial development"
    )

    commercial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of commercial development"
    )

    commercial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with commercial development"
    )

    industrial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Square footage of industrial development"
    )

    industrial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of industrial development"
    )

    industrial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees associated with industrial development"
    )

    educational: str = Field(
        default="",
        description=(
            "Description of educational development .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    recreational: str = Field(
        default="",
        description=(
            "Description of recreational development .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
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

    transportation_type: str = Field(
        default="",
        description=(
            "Type of transportation facilities or improvements .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mining_mineral: str = Field(
        default="",
        description=(
            'Type of mineral to be mined .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    power_type: str = Field(
        default="",
        description=(
            'Type of power generation facility .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    power_mw: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Power generation capacity in megawatts (MW)"
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

    hazardous_waste_type: str = Field(
        default="",
        description=(
            "Type of hazardous waste facility or materials .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    other_development_type: str = Field(
        default="",
        description=(
            "Description of other development type not listed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectIssuesDiscussedinDocument(BaseModel):
    """Environmental topics and issues addressed in the document"""

    aesthetic_visual: BooleanLike = Field(
        default="", description="Check if aesthetic/visual impacts are discussed in the document"
    )

    fiscal: BooleanLike = Field(
        default="", description="Check if fiscal impacts are discussed in the document"
    )

    recreation_parks: BooleanLike = Field(
        default="", description="Check if recreation/parks impacts are discussed in the document"
    )

    vegetation: BooleanLike = Field(
        default="", description="Check if vegetation impacts are discussed in the document"
    )

    agricultural_land: BooleanLike = Field(
        default="", description="Check if agricultural land impacts are discussed in the document"
    )

    flood_plain_flooding: BooleanLike = Field(
        default="",
        description="Check if flood plain/flooding impacts are discussed in the document",
    )

    schools_universities: BooleanLike = Field(
        default="",
        description="Check if schools/universities impacts are discussed in the document",
    )

    water_quality: BooleanLike = Field(
        default="", description="Check if water quality impacts are discussed in the document"
    )

    air_quality: BooleanLike = Field(
        default="", description="Check if air quality impacts are discussed in the document"
    )

    forest_land_fire_hazard: BooleanLike = Field(
        default="",
        description="Check if forest land or fire hazard impacts are discussed in the document",
    )

    septic_systems: BooleanLike = Field(
        default="", description="Check if septic systems impacts are discussed in the document"
    )

    water_supply_groundwater: BooleanLike = Field(
        default="",
        description="Check if water supply/groundwater impacts are discussed in the document",
    )

    archeological_historical: BooleanLike = Field(
        default="",
        description="Check if archeological/historical impacts are discussed in the document",
    )

    geologic_seismic: BooleanLike = Field(
        default="", description="Check if geologic/seismic impacts are discussed in the document"
    )

    sewer_capacity: BooleanLike = Field(
        default="", description="Check if sewer capacity impacts are discussed in the document"
    )

    wetland_riparian: BooleanLike = Field(
        default="", description="Check if wetland/riparian impacts are discussed in the document"
    )

    biological_resources: BooleanLike = Field(
        default="",
        description="Check if biological resources impacts are discussed in the document",
    )

    minerals: BooleanLike = Field(
        default="", description="Check if mineral resources impacts are discussed in the document"
    )

    soil_erosion_compaction_grading: BooleanLike = Field(
        default="",
        description="Check if soil erosion/compaction/grading impacts are discussed in the document",
    )

    growth_inducement: BooleanLike = Field(
        default="", description="Check if growth inducement impacts are discussed in the document"
    )

    coastal_zone: BooleanLike = Field(
        default="", description="Check if coastal zone impacts are discussed in the document"
    )

    noise: BooleanLike = Field(
        default="", description="Check if noise impacts are discussed in the document"
    )

    solid_waste: BooleanLike = Field(
        default="", description="Check if solid waste impacts are discussed in the document"
    )

    land_use: BooleanLike = Field(
        default="", description="Check if land use impacts are discussed in the document"
    )

    drainage_absorption: BooleanLike = Field(
        default="", description="Check if drainage/absorption impacts are discussed in the document"
    )

    population_housing_balance: BooleanLike = Field(
        default="",
        description="Check if population/housing balance impacts are discussed in the document",
    )

    toxic_hazardous: BooleanLike = Field(
        default="",
        description="Check if toxic/hazardous materials impacts are discussed in the document",
    )

    cumulative_effects: BooleanLike = Field(
        default="", description="Check if cumulative effects are discussed in the document"
    )

    economic_jobs: BooleanLike = Field(
        default="", description="Check if economic/jobs impacts are discussed in the document"
    )

    public_services_facilities: BooleanLike = Field(
        default="",
        description="Check if public services/facilities impacts are discussed in the document",
    )

    traffic_circulation: BooleanLike = Field(
        default="", description="Check if traffic/circulation impacts are discussed in the document"
    )

    other_project_issues: str = Field(
        default="",
        description=(
            "Description of other project issues discussed in the document .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ExistingLandUseProjectDescription(BaseModel):
    """Current land use designations and narrative description of the project"""

    present_land_use_zoning_general_plan_designation: str = Field(
        default="",
        description=(
            "Current land use, zoning, and general plan designation of the project site .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
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


class AppendixCNoticeOfCompletionEnvironmentalDocumentTransmittal(BaseModel):
    """
        Appendix C

    Notice of Completion & Environmental Document Transmittal

        ''
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
    existing_land_use__project_description: ExistingLandUseProjectDescription = Field(
        ..., description="Existing Land Use & Project Description"
    )
