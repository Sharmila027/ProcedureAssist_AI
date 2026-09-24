from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.auth import get_current_user

from app.models.user import User
from app.models.query_history import QueryHistory
from app.models.guidance_history import GuidanceHistory

from app.schemas.query import QueryRequest, QueryResponse

from app.services.preprocessing_service import PreprocessingService
from app.services.retrieval_service import RetrievalService
from app.services.ai_service import AIService
from app.services.procedure_service import ProcedureService
from app.services.language_service import LanguageService
from app.services.classification_service import ClassificationService
from app.services.output_service import OutputService


router = APIRouter(
    prefix="/query",
    tags=["Citizen Query"],
)


preprocessing_service = PreprocessingService()
retrieval_service = RetrievalService()
ai_service = AIService()
procedure_service = ProcedureService()
language_service = LanguageService()
classification_service = ClassificationService()
output_service = OutputService()


@router.post("/", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 1. Validate selected language
    language = language_service.validate(
        request.language
    )

    # 2. Preprocess user query
    processed = preprocessing_service.preprocess(
        request.query,
        language
    )

    cleaned_query = processed["cleaned_query"]

    # 3. Search ChromaDB
    results = retrieval_service.search(
        cleaned_query,
        limit=3
    )

    # 4. Classify procedure
    classification = classification_service.classify(
        results
    )

    # 5. No relevant procedure found
    if not results:

        history = QueryHistory(
            user_id=current_user.id,
            query_text=cleaned_query,
            language=language,
            detected_procedure="Unknown"
        )

        db.add(history)

        await db.commit()

        return QueryResponse(
            procedure="Unknown",
            language=language,
            answer="No relevant government procedure was found.",
            steps=[],
            documents=[],
            sources=[]
        )

    # 6. Get classified procedure
    procedure = classification["procedure"]

    procedure_code = classification["code"]

    # 7. Get structured procedure data
    # from PostgreSQL
    structured_procedure = None

    if procedure_code:

        structured_procedure = (
            await procedure_service.get_by_code(
                procedure_code,
                db
            )
        )

    # 8. Build context
    context_parts = []

    for result in results:

        context_parts.append(
            result["document"]
        )

    # 9. Add PostgreSQL structured data
    if structured_procedure:

        context_parts.append(
            f"""
STRUCTURED GOVERNMENT DATA:

Service Name: {structured_procedure.service_name}
Service Code: {structured_procedure.code}
Department: {structured_procedure.department}
SLA: {structured_procedure.sla_days}
CAN Required: {structured_procedure.can_required}
Validity: {structured_procedure.validity}
File Rules: {structured_procedure.file_rules}
Target Demographic: {structured_procedure.target_demographic}
Government Fee: {structured_procedure.govt_fee}
e-Sevai Fee: {structured_procedure.esevai_fee}
Access Sources: {structured_procedure.access_sources}
Tracker URL: {structured_procedure.tracker_url}
First Appellate Authority: {structured_procedure.first_appellate_authority}
Workflow: {structured_procedure.workflow}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    # 10. Generate AI guidance
    answer = ai_service.generate(
        query=cleaned_query,
        context=context,
        language=language
    )

    # 11. Collect sources
    sources = []

    for result in results:

        source = result["metadata"].get(
            "source"
        )

        if source and source not in sources:

            sources.append(source)

    # 12. Save query history
    history = QueryHistory(
        user_id=current_user.id,
        query_text=cleaned_query,
        language=language,
        detected_procedure=procedure
    )

    db.add(history)

    await db.commit()

    await db.refresh(history)

    # 13. Save guidance history
    guidance_history = GuidanceHistory(
        user_id=current_user.id,
        query_id=history.id,
        language=language,
        procedure=procedure,
        guidance=answer
    )

    db.add(guidance_history)

    await db.commit()

    # 14. Generate structured output
    output = output_service.generate(
        answer=answer,
        procedure=procedure,
        language=language,
        sources=sources
    )

    # 15. Return final response
    return QueryResponse(
        procedure=output["procedure"],
        language=output["language"],
        answer=output["answer"],
        steps=output["steps"],
        documents=output["documents"],
        sources=output["sources"]
    )