from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from pathlib import Path
import tempfile

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.auth import get_current_user

from app.models.user import User
from app.models.document import Document
from app.models.document_verification import DocumentVerification

from app.services.ocr_service import OCRService
from app.services.document_analysis_service import (
    DocumentAnalysisService
)
from app.services.document_verification_service import (
    DocumentVerificationService
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


ocr_service = OCRService()

analysis_service = DocumentAnalysisService()

verification_service = DocumentVerificationService()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    language: str = "en",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 1. Check file type
    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/jpg"
    ]

    if file.content_type not in allowed_types:

        raise HTTPException(
            status_code=400,
            detail="Only JPG and PNG documents are supported."
        )

    # 2. Create temporary file
    suffix = Path(
        file.filename
    ).suffix

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp_file:

        content = await file.read()

        temp_file.write(
            content
        )

        temp_path = temp_file.name

    try:

        # 3. OCR
        extracted_text = (
            ocr_service.extract_text(
                temp_path
            )
        )

        # 4. Analyze document
        analysis = (
            analysis_service.analyze(
                extracted_text,
                language=language
            )
        )

        # 5. Verify document
        verification = (
            verification_service.verify(
                extracted_text,
                language=language
            )
        )

        # 6. Save document
        document = Document(
            user_id=current_user.id,
            filename=file.filename,
            document_type=file.content_type,
            extracted_text=extracted_text
        )

        db.add(document)

        await db.commit()

        await db.refresh(document)

        # 7. Save verification
        document_verification = DocumentVerification(
            document_id=document.id,
            status=verification["status"],
            verification_result=verification["result"],
            missing_information=verification[
                "missing_information"
            ]
        )

        db.add(
            document_verification
        )

        await db.commit()

        # 8. Return result
        return {
            "message": "Document processed successfully",

            "document_id": document.id,

            "filename": document.filename,

            "language": language,

            "extracted_text": extracted_text,

            "analysis": analysis["answer"],

            "verification": {
                "status": verification["status"],
                "result": verification["result"],
                "missing_information":
                    verification["missing_information"]
            },

            "sources": analysis["sources"]
        }

    finally:

        # 9. Delete temporary file
        Path(
            temp_path
        ).unlink(
            missing_ok=True
        )