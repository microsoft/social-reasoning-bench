# Form Filling Data Statistics

Comprehensive statistics for a dataset of 988 forms selected from around 80k forms in common form dataset containing 1,762 open-ended questions across multiple domains.

## Dataset Overview

- **Total Forms**: 988
- **Total Questions**: 1,762
- **Form Domains**: 30 primary categories
- **Question Types**: 29 distinct taxonomies
- **Forms Analyzed for Requirements**: 110

## Question Type Distribution

### Top Question Types
1. **Description** (530) - Describing projects, events, services, conditions
2. **Explanation** (201) - Providing reasons, justifications, rationales
3. **Comment** (143) - Open feedback, suggestions, additional notes
4. **Objective** (67) - Goals, purposes, intended outcomes
5. **Experience** (65) - Past experiences, background, history

### Common Categories
- Description, Explanation, Comment, Additional Information
- Experience/Background, Objective/Goal, Plan/Strategy
- Medical/Health Information, Identification
- Recommendation/Action, Interest/Motivation
- Loss/Incident Details, Exemption/Exception

## Form Domain Distribution

### Top 10 Primary Categories
1. **Healthcare & Medical** (139 forms)
2. **Government Services** (119 forms)
3. **Environmental & Permits** (115 forms)
4. **Education & Academic** (113 forms)
5. **Non-Profit & Charitable Organizations** (76 forms)
6. **Employment & HR** (63 forms)
7. **Insurance** (50 forms)
8. **Real Estate & Housing** (49 forms)
9. **Events & Registration** (46 forms)
10. **Small Business & Licensing** (21 forms)

### Most Common Category Combinations
- **Environmental & Permits + Government Services** (99 forms)
- **Healthcare & Medical + Insurance** (35 forms)
- **Government Services + Real Estate & Housing** (32 forms)
- **Education & Academic + Healthcare & Medical** (28 forms)

## Information Requirements

### Most Requested Domain of Information
*(from 110 forms analyzed)*

1. **Past Experiences** (781 occurrences)
2. **Goals** (529 occurrences)
3. **Preferences** (422 occurrences)
4. **Property Information** (413 occurrences)
5. **Organizational Affiliation** (341 occurrences)
6. **Personal Background** (332 occurrences)
7. **Health Information** (269 occurrences)
8. **Skills & Abilities** (215 occurrences)
9. **Legal History** (215 occurrences)
10. **Financial Status** (179 occurrences)

### Frequently Requested Answer for Fields in Forms
- **Location of project** (71 occurrences)
- **Intended use/purpose of project** (71 occurrences)
- **Scope and scale of project** (62 occurrences)
- **Type of project** (44 occurrences)
- **Timeline and phases** (44 occurrences)
- **Property ownership/control** (44 occurrences)
- **Environmental impacts** (44 occurrences)
- **Current medical conditions** (35 occurrences)
- **Allergies** (26 occurrences)
- **Target audience/participants** (26 occurrences)

## Data Structure

The [data_statistics.json](data_statistics.json) file contains three main sections:

### 1. `question_types`
- Total question count
- Question type taxonomy (29 categories)
- Distribution counts for all types and primary types
- Examples for each question type category

### 2. `form_domains`
- Primary and secondary category distributions
- 247 unique category combinations
- Top 20 most common category pairings

### 3. `data_requirements`
- Information type frequencies across 110 analyzed forms
- Specific data point requirements with occurrence counts
- Breakdown by form category (e.g., Healthcare, Government, Education)
- Category-specific information needs and data points
