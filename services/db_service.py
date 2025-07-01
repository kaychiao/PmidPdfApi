from models import db, Article
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

def get_article_by_pmid(pmid):
    """
    Get article from database by PMID
    
    Args:
        pmid (str): PubMed ID
        
    Returns:
        Article: Article object or None if not found
    """
    try:
        return Article.query.filter_by(pmid=pmid).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving article with PMID {pmid}: {str(e)}")
        return None

def save_article(article_data):
    """
    Save article to database
    
    Args:
        article_data (dict or Article): Article data or object
        
    Returns:
        Article: Saved article object or None if error
    """
    try:
        if isinstance(article_data, dict):
            # Create new article from dictionary
            article = Article(**article_data)
            db.session.add(article)
        else:
            # Update existing article object
            article = article_data
            
        db.session.commit()
        return article
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error saving article: {str(e)}")
        return None