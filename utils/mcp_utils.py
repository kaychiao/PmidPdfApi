"""
Model Context Protocol (MCP) utilities

This module provides utilities for working with the Model Context Protocol,
which is a standard for communicating context between systems and large language models.
"""

from api.schemas import MCPContext, ArticleMetadata
import json

def create_mcp_context(pmid, article=None, pdf_content=None, query=None):
    """
    Create an MCP context object for a given PMID and article
    
    Args:
        pmid (str): PubMed ID
        article (Article, optional): Article object from database
        pdf_content (str, optional): PDF content as text
        query (str, optional): Original user query
        
    Returns:
        MCPContext: MCP context object
    """
    article_metadata = None
    
    if article:
        article_metadata = ArticleMetadata(
            pmid=pmid,
            doi=article.doi,
            title=article.title,
            authors=article.authors,
            journal=article.journal,
            year=article.year,
            has_pdf=article.has_pdf,
            has_abstract=article.has_abstract,
            full_text_available=article.full_text_available,
            commercial_use_allowed=article.commercial_use_allowed
        )
    
    return MCPContext(
        query=query or f"Information about PMID: {pmid}",
        pmid=pmid,
        article_metadata=article_metadata,
        pdf_content=pdf_content
    )

def serialize_mcp_context(context):
    """
    Serialize MCP context to JSON
    
    Args:
        context (MCPContext): MCP context object
        
    Returns:
        str: JSON string
    """
    return json.dumps(context.dict(), ensure_ascii=False)

def deserialize_mcp_context(json_str):
    """
    Deserialize MCP context from JSON
    
    Args:
        json_str (str): JSON string
        
    Returns:
        MCPContext: MCP context object
    """
    data = json.loads(json_str)
    return MCPContext(**data)