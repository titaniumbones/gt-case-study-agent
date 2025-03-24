"""Data schemas for the GivingTuesday Campaign Advisor."""

from typing import List, Optional

from pydantic import BaseModel, Field


class CaseStudy(BaseModel):
    """Schema for a GivingTuesday campaign case study."""

    case_study_entry: str = Field(
        ..., description="Name or identifier of the case study"
    )
    country: str = Field(..., description="Country where the campaign took place")
    full_story: Optional[str] = Field(
        "", description="Full description of the case study"
    )
    region: Optional[str] = Field(
        "", description="Region where the campaign took place"
    )
    local_region: Optional[str] = Field(
        "", description="Local region, area or institution name"
    )
    focus_area: Optional[str] = Field("", description="Focus area, cause or category")
    lead_name: Optional[str] = Field("", description="Lead person or institution name")
    date: Optional[str] = Field("", description="Date when the activity happened")
    links: Optional[str] = Field("", description="Links to relevant materials")
    goals: Optional[str] = Field("", description="Campaign goals and objectives")
    key_activities: Optional[str] = Field(
        "", description="Key activities of the campaign"
    )
    outcomes: Optional[str] = Field(
        "", description="Outcomes or results of the campaign"
    )
    contact: Optional[str] = Field("", description="Contact information")
    main_theme: Optional[str] = Field("", description="Main theme of the campaign")
    subtheme: Optional[str] = Field("", description="Subthemes of the campaign")
    gt_themes: Optional[str] = Field("", description="GivingTuesday related themes")
    notes: Optional[str] = Field("", description="Additional notes")

    # Special model config to handle empty strings
    class Config:
        # Allow arbitrary string conversion (needed for data cleaning)
        str_strip_whitespace = True

        # These model settings will help with serialization and validation
        validate_assignment = True
        extra = "ignore"

    def get_content_for_embedding(self) -> str:
        """Get content to be used for creating embeddings.

        Returns:
            Concatenated string of relevant case study information.
        """
        # Since we're now using default empty strings instead of None, we don't need the "or" clauses
        fields = []

        # Add a unique identifier to ensure each case study has distinct embedding
        fields.append(f"ID: {self.case_study_entry}")
        fields.append(f"Country: {self.country}")

        # Prioritize the full story as it contains the most unique content
        if self.full_story:
            fields.append(f"Description: {self.full_story}")

        if self.focus_area:
            fields.append(f"Focus Area: {self.focus_area}")

        if self.goals:
            fields.append(f"Goals: {self.goals}")

        if self.key_activities:
            fields.append(f"Key Activities: {self.key_activities}")

        if self.outcomes:
            fields.append(f"Outcomes: {self.outcomes}")

        if self.main_theme:
            fields.append(f"Main Theme: {self.main_theme}")

        if self.subtheme:
            fields.append(f"Subtheme: {self.subtheme}")

        if self.gt_themes:
            fields.append(f"GivingTuesday Themes: {self.gt_themes}")

        if self.local_region:
            fields.append(f"Local Region: {self.local_region}")

        if self.lead_name:
            fields.append(f"Lead Name: {self.lead_name}")

        if self.date:
            fields.append(f"Date: {self.date}")

        if self.notes:
            fields.append(f"Notes: {self.notes}")

        # Join with double newlines for better separation
        content = "\n\n".join(fields)

        # Add a log warning if the content is very short (which could lead to poor embeddings)
        if len(content) < 50:
            from src.utils.logging import logger

            logger.warning(
                f"Very short content for embedding in case study: {self.case_study_entry}. Length: {len(content)}"
            )

        return content


class CampaignQuery(BaseModel):
    """User query about GivingTuesday campaign advice."""

    query: str = Field(..., description="User query about campaign advice")


class CampaignAdvice(BaseModel):
    """Campaign advice response."""

    advice: str = Field(..., description="Advice for the GivingTuesday campaign")
    references: List[str] = Field(
        default_factory=list, description="References to case studies"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "advice": "Based on successful campaigns, consider focusing on local community engagement through storytelling and volunteer mobilization.",
                "references": [
                    "Uganda - Community Foundation",
                    "Liberia - Peace Initiative",
                ],
            }
        }
