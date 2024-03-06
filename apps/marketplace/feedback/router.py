import models
from dependencies import get_session
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import Response
from loguru import logger
from sqlalchemy.orm import Session

from .schema import CreateFeedbackSchema, FeedbackSchema
from .services import screenshot_recognize

router = APIRouter(
    prefix="/api/v1",
    tags=["feedbacks"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/feedback/{feedback_id}",
    response_model=FeedbackSchema,
    description="Get feedback by id.",
)
async def get_feedback(
    feedback_id: int,
    session: Session = Depends(get_session),
):
    feedback = models.FeedBack.get_by_id(
        session=session,
        id=feedback_id,
    )
    if feedback:
        return feedback
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found",
        )


@router.get(
    "/feedbacks",
    response_model=list[FeedbackSchema],
    description="Get feedbacks list.",
)
async def get_feedbacks_list(
    session: Session = Depends(get_session),
):
    feedbacks = models.FeedBack.get_list(session=session)
    return feedbacks


@router.delete(
    "/feedback/{feedback_id}",
    description="Delete feedback by id.",
)
async def delete_feedback(
    feedback_id: int,
    session: Session = Depends(get_session),
):
    feedback_deleted = models.FeedBack.delete_by_id(
        session=session,
        id=feedback_id,
    )
    if feedback_deleted:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found",
        )


@router.post(
    "/create_feedback/{product_id}/text",
    response_model=FeedbackSchema,
    description="Create feedback for product.",
)
async def create_feedback(
    request_data: CreateFeedbackSchema,
    product_id: int,
    session: Session = Depends(get_session),
):
    feedback = models.FeedBack.create(
        session=session,
        product_id=product_id,
        text=request_data.text,
    )
    if feedback:
        return feedback
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )


@router.post(
    "/create_feedback/{product_id}/image",
    response_model=FeedbackSchema,
    description="Create feedback for product by image.",
)
async def create_feedback_image(
    file: UploadFile,
    product_id: int,
    session: Session = Depends(get_session),
):
    file_object = await file.read()
    text = screenshot_recognize(file_object)
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't recognize text from image",
        )

    feedback = models.FeedBack.create(
        session=session,
        product_id=product_id,
        text=text,
    )
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return feedback
