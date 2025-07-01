from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Article(db.Model):
    """
    Article model representing scientific articles from PubMed.
    
    This model stores metadata and file information for articles retrieved
    from PubMed using their PMID (PubMed ID). While PMID is the natural identifier
    in the PubMed system, we use an auto-incremented integer as the primary key
    for better database performance, with PMID as a unique indexed field for lookups.
    """
    __tablename__ = 'articles'
    
    # Database primary key (surrogate key)
    id = db.Column(db.Integer, primary_key=True, 
                  comment="Primary key, auto-incremented unique identifier for internal use")
    
    # Business identifiers
    pmid = db.Column(db.String(20), unique=True, nullable=False, index=True,
                    comment="PubMed ID, unique identifier for the article in PubMed database, indexed for efficient lookups")
    doi = db.Column(db.String(100), index=True, nullable=True,
                   comment="Digital Object Identifier, a persistent identifier for the article. May be NULL for some articles.")
    
    # Article metadata fields
    title = db.Column(db.String(500), nullable=True,
                     comment="Title of the article")
    authors = db.Column(db.Text, nullable=True,
                       comment="Authors of the article, stored as text")
    journal = db.Column(db.String(255), nullable=True,
                       comment="Name of the journal where the article was published")
    year = db.Column(db.Integer, nullable=True,
                    comment="Year of publication")
    
    # Availability flags
    has_pdf = db.Column(db.Boolean, default=False,
                       comment="Flag indicating if PDF is available for this article")
    has_abstract = db.Column(db.Boolean, default=False,
                           comment="Flag indicating if abstract is available for this article")
    full_text_available = db.Column(db.Boolean, default=False,
                                   comment="Flag indicating if full text is available for this article")
    commercial_use_allowed = db.Column(db.Boolean, default=False,
                                      comment="Flag indicating if commercial use is allowed for this article")
    
    # File storage information
    relative_path = db.Column(db.String(255), nullable=True,
                             comment="Relative path to the PDF file in the storage system")
    
    # Download status
    download_attempted = db.Column(db.Boolean, default=False,
                                  comment="Flag indicating if download has been attempted for this article")
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow,
                          comment="Timestamp when the record was created")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
                          comment="Timestamp when the record was last updated")
    
    def __repr__(self):
        return f"<Article pmid={self.pmid}, title={self.title}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'pmid': self.pmid,
            'doi': self.doi,
            'title': self.title,
            'authors': self.authors,
            'journal': self.journal,
            'year': self.year,
            'has_pdf': self.has_pdf,
            'has_abstract': self.has_abstract,
            'full_text_available': self.full_text_available,
            'commercial_use_allowed': self.commercial_use_allowed,
            'relative_path': self.relative_path,
            'download_attempted': self.download_attempted,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }