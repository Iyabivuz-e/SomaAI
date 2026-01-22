"""Document endpoints."""

from fastapi import APIRouter, Query

from somaai.contracts.docs import DocumentResponse, DocumentViewLinkResponse

router = APIRouter(prefix="/docs", tags=["documents"])


@router.get("/{doc_id}", response_model=DocumentResponse)
async def get_document(doc_id: str):
    """Get document metadata.

    Returns document details including:
    - Filename and title
    - Grade and subject
    - Page and chunk counts
    - Upload and processing timestamps

    Returns 404 if document not found.
    """
    pass


@router.get("/{doc_id}/view", response_model=DocumentViewLinkResponse)
async def get_document_view_link(doc_id: str):
    """Get a viewing link for the document.

    Returns a URL to view the document content.
    """
    pass


# @router.get("/{doc_id}/view", response_model=DocumentViewResponse)
# async def view_document_page(
#     doc_id: str,
#     page: int = Query(1, ge=1, description="Page number (1-indexed)"),
# ):
#     """View a specific page of a document.

#     Returns page content for rendering:
#     - For PDFs: image_url for rendered page
#     - For text docs: text content

#     Also includes chunks extracted from this page for context.

#     Returns 404 if document or page not found.
#     """
#     pass
