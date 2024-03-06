import models
from dependencies import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session

from .schema import CreateProductSchema, ProductSchema, UpdateProductSchema
from .services import create_csv

router = APIRouter(
    prefix="/api/v1",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/product/{product_id}",
    response_model=ProductSchema,
    description="Get product by id.",
)
async def get_product(
    product_id: int,
    session: Session = Depends(get_session),
):
    product = models.Product.get_by_id(
        session=session,
        id=product_id,
    )
    if product:
        return product
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )


@router.get(
    "/product/{product_id}/feedbacks",
    response_model=ProductSchema,
    description="Get feedbacks for product by id.",
)
async def get_product_feedbacks(
    product_id: int,
    session: Session = Depends(get_session),
):
    product = models.Product.get_by_id(
        session=session,
        id=product_id,
    )
    if product:
        return product
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )


@router.get(
    "/products",
    response_model=list[ProductSchema],
    description="Get products list.",
)
async def get_products_list(
    session: Session = Depends(get_session),
):
    products = models.Product.get_list(session=session)
    return products


@router.get(
    "/products_csv",
    response_class=FileResponse,
    description="Get products list in csv.",
)
async def get_products_list_csv(
    session: Session = Depends(get_session),
):
    products = models.Product.get_list(session=session)
    csv_file = create_csv(products, models.Product)
    return FileResponse(csv_file, media_type="text/csv", filename="products.csv")


@router.put(
    "/product/{product_id}",
    response_model=ProductSchema,
    description="Update product by id.",
)
async def update_product(
    product_id: str,
    product: UpdateProductSchema,
    session: Session = Depends(get_session),
):
    updated_product = models.Product.update_by_id(
        session=session,
        id=product_id,
        new_product=product,
    )
    if updated_product:
        return updated_product
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )


@router.delete(
    "/product/{product_id}",
    description="Delete product by id.",
)
async def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
):
    product_deleted = models.Product.delete_by_id(
        session=session,
        id=product_id,
    )
    if product_deleted:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )


@router.post(
    "/get_or_create_product",
    response_model=ProductSchema,
    description="Get or create product by name.",
)
async def get_or_create_product(
    request_data: CreateProductSchema,
    session: Session = Depends(get_session),
):
    product = models.Product.get_or_create_by_name(
        session=session,
        name=request_data.name,
    )
    return product
