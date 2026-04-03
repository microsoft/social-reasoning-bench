from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProjectIdentification(BaseModel):
    """Basic project and lead agency information"""

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

    project_location_zip_code: str = Field(
        default="", description="ZIP code of the project location"
    )

    cross_streets: str = Field(
        default="",
        description=(
            "Major cross streets near the project location .If you cannot fill this, write "
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
            "Section designation for the project location .If you cannot fill this, write "
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
    """Type of environmental document being filed"""

    ceqa_nop: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Notice of Preparation (NOP)"
    )

    ceqa_early_cons: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Early Consultation"
    )

    ceqa_neg_dec: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Negative Declaration"
    )

    ceqa_mit_neg_dec: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Mitigated Negative Declaration"
    )

    ceqa_draft_eir: BooleanLike = Field(
        default="",
        description="Check if the CEQA document type is Draft Environmental Impact Report (EIR)",
    )

    ceqa_supplement_subsequent_eir: BooleanLike = Field(
        default="", description="Check if the CEQA document type is Supplement or Subsequent EIR"
    )

    ceqa_prior_sch_no: str = Field(
        default="",
        description=(
            "Prior State Clearinghouse number, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ceqa_other: str = Field(
        default="",
        description=(
            "Other CEQA document type, if not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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
        description="Check if the NEPA document type is Draft Environmental Impact Statement (EIS)",
    )

    nepa_fonsi: BooleanLike = Field(
        default="",
        description="Check if the NEPA document type is Finding of No Significant Impact (FONSI)",
    )

    other_joint_document: BooleanLike = Field(
        default="", description="Check if this is a joint CEQA/NEPA or other joint document"
    )

    other_final_document: BooleanLike = Field(
        default="", description="Check if this is a final document"
    )

    other_other: str = Field(
        default="",
        description=(
            "Describe other document type, if not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class LocalActionType(BaseModel):
    """Local approvals or planning actions associated with the project"""

    local_action_type_general_plan_update: BooleanLike = Field(
        default="", description="Check if the local action type is General Plan Update"
    )

    local_action_type_specific_plan: BooleanLike = Field(
        default="", description="Check if the local action type is Specific Plan"
    )

    local_action_type_rezone: BooleanLike = Field(
        default="", description="Check if the local action type is Rezone"
    )

    local_action_type_annexation: BooleanLike = Field(
        default="", description="Check if the local action type is Annexation"
    )

    local_action_type_general_plan_amendment: BooleanLike = Field(
        default="", description="Check if the local action type is General Plan Amendment"
    )

    local_action_type_master_plan: BooleanLike = Field(
        default="", description="Check if the local action type is Master Plan"
    )

    local_action_type_prezone: BooleanLike = Field(
        default="", description="Check if the local action type is Prezone"
    )

    local_action_type_redevelopment: BooleanLike = Field(
        default="", description="Check if the local action type is Redevelopment"
    )

    local_action_type_general_plan_element: BooleanLike = Field(
        default="", description="Check if the local action type is General Plan Element"
    )

    local_action_type_planned_unit_development: BooleanLike = Field(
        default="", description="Check if the local action type is Planned Unit Development"
    )

    local_action_type_use_permit: BooleanLike = Field(
        default="", description="Check if the local action type is Use Permit"
    )

    local_action_type_coastal_permit: BooleanLike = Field(
        default="", description="Check if the local action type is Coastal Permit"
    )

    local_action_type_community_plan: BooleanLike = Field(
        default="", description="Check if the local action type is Community Plan"
    )

    local_action_type_site_plan: BooleanLike = Field(
        default="", description="Check if the local action type is Site Plan"
    )

    local_action_type_land_division_subdivision_etc: BooleanLike = Field(
        default="",
        description="Check if the local action type is Land Division (Subdivision, etc.)",
    )

    local_action_type_other: str = Field(
        default="",
        description=(
            "Describe other local action type, if not listed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class DevelopmentType(BaseModel):
    """Type and scale of proposed development"""

    development_type_residential_checkbox: BooleanLike = Field(
        default="", description="Check if the project includes residential development"
    )

    residential_units: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of residential units proposed"
    )

    residential_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage of residential development"
    )

    development_type_office_checkbox: BooleanLike = Field(
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

    development_type_commercial_checkbox: BooleanLike = Field(
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

    development_type_industrial_checkbox: BooleanLike = Field(
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

    development_type_educational: BooleanLike = Field(
        default="", description="Check if the project includes educational facilities"
    )

    development_type_recreational: BooleanLike = Field(
        default="", description="Check if the project includes recreational facilities"
    )

    development_type_water_facilities_checkbox: BooleanLike = Field(
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

    development_type_transportation_checkbox: BooleanLike = Field(
        default="", description="Check if the project includes transportation facilities"
    )

    transportation_type: str = Field(
        default="",
        description=(
            "Type of transportation facilities proposed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    development_type_mining_checkbox: BooleanLike = Field(
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

    development_type_power_checkbox: BooleanLike = Field(
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

    development_type_waste_treatment_checkbox: BooleanLike = Field(
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

    development_type_hazardous_waste_checkbox: BooleanLike = Field(
        default="", description="Check if the project includes hazardous waste facilities"
    )

    hazardous_waste_type: str = Field(
        default="",
        description=(
            "Type of hazardous waste facility or waste handled .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    development_type_other: str = Field(
        default="",
        description=(
            "Describe other types of development not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectIssuesDiscussedinDocument(BaseModel):
    """Environmental issues addressed in the document"""

    project_issues_aesthetic_visual: BooleanLike = Field(
        default="", description="Check if aesthetic/visual impacts are discussed"
    )

    project_issues_agricultural_land: BooleanLike = Field(
        default="", description="Check if agricultural land impacts are discussed"
    )

    project_issues_air_quality: BooleanLike = Field(
        default="", description="Check if air quality impacts are discussed"
    )

    project_issues_archeological_historical: BooleanLike = Field(
        default="", description="Check if archeological/historical resources are discussed"
    )

    project_issues_biological_resources: BooleanLike = Field(
        default="", description="Check if biological resources impacts are discussed"
    )

    project_issues_coastal_zone: BooleanLike = Field(
        default="", description="Check if coastal zone issues are discussed"
    )

    project_issues_drainage_absorption: BooleanLike = Field(
        default="", description="Check if drainage/absorption issues are discussed"
    )

    project_issues_economic_jobs: BooleanLike = Field(
        default="", description="Check if economic or jobs impacts are discussed"
    )

    project_issues_fiscal: BooleanLike = Field(
        default="", description="Check if fiscal impacts are discussed"
    )

    project_issues_flood_plain_flooding: BooleanLike = Field(
        default="", description="Check if flood plain or flooding impacts are discussed"
    )

    project_issues_forest_land_fire_hazard: BooleanLike = Field(
        default="", description="Check if forest land or fire hazard issues are discussed"
    )

    project_issues_geologic_seismic: BooleanLike = Field(
        default="", description="Check if geologic or seismic impacts are discussed"
    )

    project_issues_minerals: BooleanLike = Field(
        default="", description="Check if mineral resources impacts are discussed"
    )

    project_issues_noise: BooleanLike = Field(
        default="", description="Check if noise impacts are discussed"
    )

    project_issues_population_housing_balance: BooleanLike = Field(
        default="", description="Check if population/housing balance issues are discussed"
    )

    project_issues_public_services_facilities: BooleanLike = Field(
        default="", description="Check if public services or facilities impacts are discussed"
    )

    project_issues_recreation_parks: BooleanLike = Field(
        default="", description="Check if recreation or parks impacts are discussed"
    )

    project_issues_schools_universities: BooleanLike = Field(
        default="", description="Check if schools or universities impacts are discussed"
    )

    project_issues_septic_systems: BooleanLike = Field(
        default="", description="Check if septic systems impacts are discussed"
    )

    project_issues_sewer_capacity: BooleanLike = Field(
        default="", description="Check if sewer capacity impacts are discussed"
    )

    project_issues_soil_erosion_compaction_grading: BooleanLike = Field(
        default="",
        description="Check if soil erosion, compaction, or grading impacts are discussed",
    )

    project_issues_solid_waste: BooleanLike = Field(
        default="", description="Check if solid waste impacts are discussed"
    )

    project_issues_toxic_hazardous: BooleanLike = Field(
        default="", description="Check if toxic or hazardous materials impacts are discussed"
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
        default="", description="Check if growth inducement impacts are discussed"
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
            "Describe other project issues discussed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ExistingandProposedUse(BaseModel):
    """Current land use and narrative project description"""

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
            "Detailed description of the project; attach additional pages if necessary .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AppendixCNoticeOfCompletionEnvironmentalDocumentTransmittal(BaseModel):
    """
        Appendix C

    Notice of Completion & Environmental Document Transmittal

        ''
    """

    project_identification: ProjectIdentification = Field(..., description="Project Identification")
    project_location: ProjectLocation = Field(..., description="Project Location")
    document_type: DocumentType = Field(..., description="Document Type")
    local_action_type: LocalActionType = Field(..., description="Local Action Type")
    development_type: DevelopmentType = Field(..., description="Development Type")
    project_issues_discussed_in_document: ProjectIssuesDiscussedinDocument = Field(
        ..., description="Project Issues Discussed in Document"
    )
    existing_and_proposed_use: ExistingandProposedUse = Field(
        ..., description="Existing and Proposed Use"
    )
