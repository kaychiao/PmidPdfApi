from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

# Request models
class PMIDRequest(BaseModel):
    pmid: str = Field(..., description="PubMed ID")

# Response models
class ErrorResponse(BaseModel):
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Error details")

class PDFData(BaseModel):
    pmid: str = Field(..., description="PubMed ID")
    pdf_url: str = Field(..., description="URL to the PDF file")
    title: Optional[str] = Field(None, description="Article title")
    authors: Optional[str] = Field(None, description="Article authors")
    journal: Optional[str] = Field(None, description="Journal name")
    year: Optional[int] = Field(None, description="Publication year")

class PDFResponse(BaseModel):
    status: str = Field(..., description="Response status")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data containing PDF information")

class ArticleMetadata(BaseModel):
    pmid: str = Field(..., description="PubMed ID")
    doi: Optional[str] = Field(None, description="Digital Object Identifier")
    title: Optional[str] = Field(None, description="Article title")
    authors: Optional[str] = Field(None, description="Article authors")
    journal: Optional[str] = Field(None, description="Journal name")
    year: Optional[int] = Field(None, description="Publication year")
    has_pdf: bool = Field(..., description="Whether PDF is available")
    has_abstract: bool = Field(..., description="Whether abstract is available")
    full_text_available: bool = Field(..., description="Whether full text is available")
    commercial_use_allowed: bool = Field(..., description="Whether commercial use is allowed")

# MCP (Model Context Protocol) schemas
class MCPContext(BaseModel):
    query: str = Field(..., description="User query")
    pmid: str = Field(..., description="PubMed ID")
    article_metadata: Optional[ArticleMetadata] = Field(None, description="Article metadata")
    pdf_content: Optional[str] = Field(None, description="PDF content")