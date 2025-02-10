from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, Response

from models.genre import GenreDTO
from services.genre import GenreService
from services.service_factory import service_for
from fastapi_cache.decorator import cache


router = APIRouter()


@router.get(
    '/',
    response_model=List[GenreDTO],
    summary='Get genres',
    description='Get all genres.',
)
@cache(expire=60)
async def get_genres(
    request: Request,
    response: Response,
    genre_service: GenreService = Depends(service_for("genre"))
) -> List[GenreDTO]:
    genres = await genre_service.search()
    if not genres:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='genres not found'
        )
    return genres


@router.get(
    '/{genre_id}',
    response_model=GenreDTO,
    summary='Get genre',
    description='Get genre details.',
)
@cache(expire=60)
async def genre_details(
    request: Request,
    response: Response,
    genre_id: Annotated[
        str,
        Path(
            title="genre id",
            description="Genre id for the item to search in the database",
        ),
    ],
    genre_service: GenreService = Depends(service_for("genre"))
) -> GenreDTO:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='genre not found'
        )
    return genre
