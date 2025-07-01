from flask import current_app
import os
import logging
from services.db_service import get_article_by_pmid, save_article

logger = logging.getLogger(__name__)

def get_pdf_by_pmid(pmid):
    """
    Get PDF information for a given PMID from the database or download it using PubCrawler
    
    Args:
        pmid (str): PubMed ID
        
    Returns:
        dict: PDF information or None if not found
    """
    # 1. Check if PDF exists in database
    pdf_info = get_pdf_from_database(pmid)
    if pdf_info:
        return pdf_info
    
    # 2. If not found in database or file doesn't exist, download using PubCrawler
    return download_pdf_with_pubcrawler(pmid)


def get_pdf_from_database(pmid):
    """
    Get PDF information from database
    
    Args:
        pmid (str): PubMed ID
        
    Returns:
        dict: PDF information or None if not found
    """
    article = get_article_by_pmid(pmid)
    
    if not article or not article.has_pdf:
        return None
    
    # Build absolute path to PDF file
    pdf_path = os.path.join(current_app.config['PDF_ROOT_PATH'], article.relative_path, 'article.pdf')
    
    # Verify if PDF file actually exists
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
        return {
            'pmid': pmid,
            'pdf_path': pdf_path,
            'title': article.title,
            'authors': article.authors,
            'journal': article.journal,
            'year': article.year
        }
    else:
        # PDF file doesn't exist, update database record
        article.has_pdf = False
        save_article(article)
        return None


def download_pdf_with_pubcrawler(pmid):
    """
    Download PDF using PubCrawler
    
    Args:
        pmid (str): PubMed ID
        
    Returns:
        dict: PDF information or None if download failed
    """
    try:
        # Initialize PubCrawler
        crawler = initialize_pubcrawler()
        
        # Process PMID with PubCrawler
        result = crawler.process_pmid(pmid)
        
        if result['success'] and result['has_pdf']:
            return process_successful_download(pmid, result)
        else:
            handle_failed_download(pmid, result)
            return None
            
    except Exception as e:
        logger.error(f"Error using PubCrawler for PMID {pmid}: {str(e)}")
        return None


def initialize_pubcrawler():
    """
    Initialize PubCrawler instance
    
    Returns:
        PubCrawler: Initialized PubCrawler instance
    """
    from pubcrawler import PubCrawler
    
    return PubCrawler(
        email=current_app.config.get('NCBI_EMAIL', 'your.email@example.com'),
        base_dir=current_app.config.get('PDF_ROOT_PATH', '/app/downloads'),
        # api_key=current_app.config.get('NCBI_API_KEY', None),
        max_concurrent_downloads=5,
        requests_per_second=3.0
    )


def process_successful_download(pmid, result):
    """
    Process successful download result
    
    Args:
        pmid (str): PubMed ID
        result (dict): PubCrawler result
        
    Returns:
        dict: PDF information
    """
    # Extract relative path from result
    base_dir = current_app.config.get('PDF_ROOT_PATH', '/app/downloads')
    relative_path = os.path.relpath(result['path'], base_dir)
    
    # Build absolute path to PDF file
    pdf_path = os.path.join(result['path'], 'article.pdf')
    
    # Update or create database record
    article = get_article_by_pmid(pmid)
    
    if article:
        update_existing_article(article, relative_path)
    else:
        article = create_new_article(pmid, result['path'], relative_path)
    
    # Return PDF information
    return {
        'pmid': pmid,
        'pdf_path': pdf_path,
        'title': article.title if hasattr(article, 'title') else '',
        'authors': article.authors if hasattr(article, 'authors') else '',
        'journal': article.journal if hasattr(article, 'journal') else '',
        'year': article.year if hasattr(article, 'year') else None
    }


def update_existing_article(article, relative_path):
    """
    Update existing article record
    
    Args:
        article: Article record object
        relative_path (str): Relative path
    """
    article.has_pdf = True
    article.relative_path = relative_path
    save_article(article)


def create_new_article(pmid, full_path, relative_path):
    """
    Create new article record
    
    Args:
        pmid (str): PubMed ID
        full_path (str): Full path
        relative_path (str): Relative path
        
    Returns:
        article: Created article record
    """
    # Extract metadata from PubCrawler result
    metadata_path = os.path.join(full_path, 'metadata.json')
    
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        # Create new article record
        new_article = {
            'pmid': pmid,
            'doi': metadata.get('doi'),
            'title': metadata.get('title'),
            'authors': metadata.get('authors', ''),
            'journal': metadata.get('journal'),
            'year': metadata.get('year'),
            'has_pdf': True,
            'has_abstract': bool(metadata.get('abstract')),
            'full_text_available': True,
            'commercial_use_allowed': False,  # Default value, may need to be adjusted
            'relative_path': relative_path,
            'download_attempted': True
        }
    else:
        # If no metadata file exists, create a basic record
        new_article = {
            'pmid': pmid,
            'has_pdf': True,
            'relative_path': relative_path,
            'download_attempted': True
        }
    
    return save_article(new_article)


def handle_failed_download(pmid, result):
    """
    Handle failed download
    
    Args:
        pmid (str): PubMed ID
        result (dict): PubCrawler result
    """
    logger.error(f"Failed to download PDF for PMID {pmid}: {result.get('error', 'Unknown error')}")
    
    # Update database record
    article = get_article_by_pmid(pmid)
    
    if article:
        article.download_attempted = True
        save_article(article)
    else:
        # Create new record, mark download attempt as failed
        new_article = {
            'pmid': pmid,
            'has_pdf': False,
            'download_attempted': True
        }
        save_article(new_article)
