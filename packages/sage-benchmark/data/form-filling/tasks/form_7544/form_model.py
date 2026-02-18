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
    """Basic project identifiers and lead agency contact details"""

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

    longitude_n_degrees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Latitude degrees (north) in degrees, minutes, seconds format"
    )

    longitude_n_minutes: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Latitude minutes (north) in degrees, minutes, seconds format"
    )

    longitude_n_seconds: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Latitude seconds (north) in degrees, minutes, seconds format"
    )

    longitude_w_degrees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Longitude degrees (west) in degrees, minutes, seconds format"
    )

    longitude_w_minutes: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Longitude minutes (west) in degrees, minutes, seconds format"
    )

    longitude_w_seconds: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Longitude seconds (west) in degrees, minutes, seconds format"
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
    """Type of environmental document being filed"""

    ceqa_nop: BooleanLike = Field(
        default="", description="Check if the document type is Notice of Preparation (NOP)"
    )

    ceqa_draft_eir: BooleanLike = Field(
        default="",
        description="Check if the document type is Draft Environmental Impact Report (Draft EIR)",
    )

    ceqa_supplement_subsequent_eir: BooleanLike = Field(
        default="", description="Check if the document type is a Supplement or Subsequent EIR"
    )

    ceqa_noi: BooleanLike = Field(
        default="", description="Check if the document type is Notice of Intent (NOI)"
    )

    ceqa_ea: BooleanLike = Field(
        default="", description="Check if the document type is Environmental Assessment (EA)"
    )

    ceqa_joint_document: BooleanLike = Field(
        default="",
        description="Check if the document is a joint CEQA/NEPA or similar joint document",
    )

    ceqa_early_cons: BooleanLike = Field(
        default="", description="Check if the document type is Early Consultation"
    )

    ceqa_neg_dec_prior_sch_no: str = Field(
        default="",
        description=(
            "Check if Negative Declaration and provide prior SCH number if applicable .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    ceqa_other_neg_dec_line: str = Field(
        default="",
        description=(
            "Specify other CEQA document type on the Neg Dec line .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ceqa_final_document: BooleanLike = Field(
        default="", description="Check if this is the final CEQA document"
    )

    ceqa_mit_neg_dec: BooleanLike = Field(
        default="", description="Check if the document type is Mitigated Negative Declaration"
    )

    ceqa_other_mit_neg_dec_line: str = Field(
        default="",
        description=(
            "Specify other CEQA document type on the Mit Neg Dec line .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ceqa_draft_eis: BooleanLike = Field(
        default="",
        description="Check if the document type is Draft Environmental Impact Statement (Draft EIS)",
    )

    ceqa_fonsi: BooleanLike = Field(
        default="",
        description="Check if the document type is Finding of No Significant Impact (FONSI)",
    )


class LocalActionType(BaseModel):
    """Local planning or permitting actions associated with the project"""

    local_action_general_plan_update: BooleanLike = Field(
        default="", description="Check if the local action includes a General Plan Update"
    )

    local_action_specific_plan: BooleanLike = Field(
        default="", description="Check if the local action includes a Specific Plan"
    )

    local_action_rezone: BooleanLike = Field(
        default="", description="Check if the local action includes a Rezone"
    )

    local_action_annexation: BooleanLike = Field(
        default="", description="Check if the local action includes an Annexation"
    )

    local_action_general_plan_amendment: BooleanLike = Field(
        default="", description="Check if the local action includes a General Plan Amendment"
    )

    local_action_master_plan: BooleanLike = Field(
        default="", description="Check if the local action includes a Master Plan"
    )

    local_action_prezone: BooleanLike = Field(
        default="", description="Check if the local action includes a Prezone"
    )

    local_action_redevelopment: BooleanLike = Field(
        default="", description="Check if the local action includes Redevelopment"
    )

    local_action_general_plan_element: BooleanLike = Field(
        default="", description="Check if the action involves a specific General Plan Element"
    )

    local_action_planned_unit_development: BooleanLike = Field(
        default="", description="Check if the action includes a Planned Unit Development"
    )

    local_action_use_permit: BooleanLike = Field(
        default="", description="Check if the action includes a Use Permit"
    )

    local_action_coastal_permit: BooleanLike = Field(
        default="", description="Check if the action includes a Coastal Permit"
    )

    local_action_community_plan: BooleanLike = Field(
        default="", description="Check if the action includes a Community Plan"
    )

    local_action_site_plan: BooleanLike = Field(
        default="", description="Check if the action includes a Site Plan"
    )

    local_action_land_division: BooleanLike = Field(
        default="", description="Check if the action includes Land Division such as subdivision"
    )

    local_action_other: str = Field(
        default="",
        description=(
            "Specify any other type of local action .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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
        default="", description="Acreage of residential development"
    )

    development_transportation: BooleanLike = Field(
        default="",
        description="Check if the project includes transportation facilities or improvements",
    )

    transportation_type: str = Field(
        default="",
        description=(
            "Type of transportation project (e.g., road, rail, transit) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    development_office: BooleanLike = Field(
        default="", description="Check if the project includes office development"
    )

    office_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total square footage of office space"
    )

    office_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage devoted to office use"
    )

    office_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of office employees"
    )

    development_mining: BooleanLike = Field(
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

    development_commercial: BooleanLike = Field(
        default="", description="Check if the project includes commercial development"
    )

    commercial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total square footage of commercial space"
    )

    commercial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage devoted to commercial use"
    )

    commercial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of commercial employees"
    )

    development_power: BooleanLike = Field(
        default="", description="Check if the project includes power generation or facilities"
    )

    power_type: str = Field(
        default="",
        description=(
            "Type of power facility (e.g., solar, wind, gas) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    power_mw: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Power generation capacity in megawatts (MW)"
    )

    development_industrial: BooleanLike = Field(
        default="", description="Check if the project includes industrial development"
    )

    industrial_sq_ft: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total square footage of industrial space"
    )

    industrial_acres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Acreage devoted to industrial use"
    )

    industrial_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of industrial employees"
    )

    development_waste_treatment: BooleanLike = Field(
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
        default="", description="Waste treatment capacity in million gallons per day (MGD)"
    )

    development_educational: BooleanLike = Field(
        default="", description="Check if the project includes educational facilities"
    )

    educational: str = Field(
        default="",
        description=(
            "Describe the type of educational development .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    development_hazardous_waste: BooleanLike = Field(
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

    development_recreational: BooleanLike = Field(
        default="", description="Check if the project includes recreational facilities"
    )

    recreational: str = Field(
        default="",
        description=(
            "Describe the type of recreational development .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    development_other: BooleanLike = Field(
        default="",
        description="Check if the project includes other types of development not listed",
    )

    other_development_type: str = Field(
        default="",
        description=(
            "Describe any other type of development .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    development_water_facilities: BooleanLike = Field(
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
        default="", description="Water facility capacity in million gallons per day (MGD)"
    )


class ProjectIssuesDiscussedinDocument(BaseModel):
    """Environmental and planning issues addressed in the document"""

    project_issues_aesthetic_visual: BooleanLike = Field(
        default="", description="Indicate if aesthetic or visual impacts are discussed"
    )

    project_issues_fiscal: BooleanLike = Field(
        default="", description="Indicate if fiscal impacts are discussed"
    )

    project_issues_recreation_parks: BooleanLike = Field(
        default="", description="Indicate if recreation or parks impacts are discussed"
    )

    project_issues_vegetation: BooleanLike = Field(
        default="", description="Indicate if vegetation impacts are discussed"
    )

    project_issues_agricultural_land: BooleanLike = Field(
        default="", description="Indicate if agricultural land impacts are discussed"
    )

    project_issues_flood_plain_flooding: BooleanLike = Field(
        default="", description="Indicate if flood plain or flooding impacts are discussed"
    )

    project_issues_schools_universities: BooleanLike = Field(
        default="", description="Indicate if impacts to schools or universities are discussed"
    )

    project_issues_water_quality: BooleanLike = Field(
        default="", description="Indicate if water quality impacts are discussed"
    )

    project_issues_air_quality: BooleanLike = Field(
        default="", description="Indicate if air quality impacts are discussed"
    )

    project_issues_forest_land_fire_hazard: BooleanLike = Field(
        default="", description="Indicate if forest land or fire hazard impacts are discussed"
    )

    project_issues_septic_systems: BooleanLike = Field(
        default="", description="Indicate if septic system impacts are discussed"
    )

    project_issues_water_supply_groundwater: BooleanLike = Field(
        default="", description="Indicate if water supply or groundwater impacts are discussed"
    )

    project_issues_archeological_historical: BooleanLike = Field(
        default="",
        description="Indicate if archeological or historical resources impacts are discussed",
    )

    project_issues_geologic_seismic: BooleanLike = Field(
        default="", description="Indicate if geologic or seismic impacts are discussed"
    )

    project_issues_sewer_capacity: BooleanLike = Field(
        default="", description="Indicate if sewer capacity impacts are discussed"
    )

    project_issues_wetland_riparian: BooleanLike = Field(
        default="", description="Indicate if wetland or riparian impacts are discussed"
    )

    project_issues_biological_resources: BooleanLike = Field(
        default="", description="Indicate if biological resources impacts are discussed"
    )

    project_issues_minerals: BooleanLike = Field(
        default="", description="Indicate if mineral resources impacts are discussed"
    )

    project_issues_soil_erosion_compaction_grading: BooleanLike = Field(
        default="",
        description="Indicate if soil erosion, compaction, or grading impacts are discussed",
    )

    project_issues_growth_inducement: BooleanLike = Field(
        default="", description="Indicate if growth-inducing impacts are discussed"
    )

    project_issues_coastal_zone: BooleanLike = Field(
        default="", description="Indicate if coastal zone impacts are discussed"
    )

    project_issues_noise: BooleanLike = Field(
        default="", description="Indicate if noise impacts are discussed"
    )

    project_issues_solid_waste: BooleanLike = Field(
        default="", description="Indicate if solid waste impacts are discussed"
    )

    project_issues_land_use: BooleanLike = Field(
        default="", description="Indicate if land use impacts are discussed"
    )

    project_issues_drainage_absorption: BooleanLike = Field(
        default="", description="Indicate if drainage or absorption impacts are discussed"
    )

    project_issues_population_housing_balance: BooleanLike = Field(
        default="", description="Indicate if population or housing balance impacts are discussed"
    )

    project_issues_toxic_hazardous: BooleanLike = Field(
        default="", description="Indicate if toxic or hazardous materials impacts are discussed"
    )

    project_issues_cumulative_effects: BooleanLike = Field(
        default="", description="Indicate if cumulative impacts are discussed"
    )

    project_issues_economic_jobs: BooleanLike = Field(
        default="", description="Indicate if economic or employment impacts are discussed"
    )

    project_issues_public_services_facilities: BooleanLike = Field(
        default="", description="Indicate if public services or facilities impacts are discussed"
    )

    project_issues_traffic_circulation: BooleanLike = Field(
        default="", description="Indicate if traffic or circulation impacts are discussed"
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


class LandUseandProjectDescription(BaseModel):
    """Existing land use designations and narrative project description"""

    present_land_use_zoning_general_plan_designation: str = Field(
        default="",
        description=(
            "Describe current land use, zoning, and General Plan designation of the project "
            'site .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    project_description: str = Field(
        ...,
        description=(
            "Narrative description of the proposed project; attach additional pages if "
            'needed .If you cannot fill this, write "N/A". If this field should not be '
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
    land_use_and_project_description: LandUseandProjectDescription = Field(
        ..., description="Land Use and Project Description"
    )
