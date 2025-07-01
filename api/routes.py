from flask import Blueprint, current_app, url_for, send_file, send_from_directory
from spectree import Response
from api.schemas import PDFResponse, ErrorResponse
from api.auth import require_api_key
from services.pdf_service import get_pdf_by_pmid
from services.db_service import get_article_by_pmid
from api.response_handler import ApiResponse
from utils.error_codes import ErrorCodes
from api.extensions import spec
import os

api_bp = Blueprint('api', __name__)


@api_bp.route('/pdf/<pmid>', methods=['GET'])
@require_api_key
@spec.validate(
    # resp=Response(HTTP_200=PDFResponse, HTTP_404=ErrorResponse, HTTP_500=ErrorResponse),
    # resp=Response(HTTP_200=None, HTTP_404=ErrorResponse, HTTP_500=ErrorResponse),
    tags=['PDF']
)
def get_pdf(pmid):
    """
    Get PDF link by PMID
    
    If the PDF exists in the local database, returns the link / the PDF file stream.
    If not, attempts to download it using PubCrawler.
    """
    try:
        # Use get_pdf_by_pmid function to get PDF information
        # This function checks the database and uses PubCrawler to download if not found
        pdf_info = get_pdf_by_pmid(pmid)
        
        if pdf_info:
            # PDF retrieved successfully, build URL and return
            # pdf_url = url_for('static', filename=f'pdfs/{os.path.relpath(pdf_info["pdf_path"], current_app.config["PDF_ROOT_PATH"])}', _external=True)
            
            # response_data = {
            #     "pmid": pmid,
            #     "pdf_url": pdf_url,
            #     "title": pdf_info.get('title', ''),
            #     "authors": pdf_info.get('authors', ''),
            #     "journal": pdf_info.get('journal', ''),
            #     "year": pdf_info.get('year')
            # }
            # return ApiResponse.success(data=response_data)
            return send_file(
                pdf_info["pdf_path"],
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f"{pmid}.pdf"
            )

        else:
            # Failed to retrieve PDF
            # Check if download was already attempted
            article = get_article_by_pmid(pmid)
            if article and article.download_attempted:
                error_message = f"PDF not available for PMID: {pmid}"
            else:
                error_message = f"Failed to retrieve PDF for PMID: {pmid}"
                
            return ApiResponse.error(
                message=error_message,
                code=ErrorCodes.PDF_NOT_AVAILABLE.name,
                details={"pmid": pmid},
                status_code=404
            )
            
    except Exception as e:
        return ApiResponse.error(
            message=f"An error occurred: {str(e)}",
            code=ErrorCodes.INTERNAL_SERVER_ERROR.name,
            details={"pmid": pmid},
            status_code=500
        )

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return ApiResponse.success(data={"status": "healthy"})