from typing import Any, ClassVar

import fastapi
import fastapi_jsonapi
import pydantic

from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi_jsonapi.views.utils import HTTPMethod, HTTPMethodConfig
from fastapi_jsonapi.data_layers.sqla_orm import SqlalchemyDataLayer
from fastapi_jsonapi.misc.sqla.generics.base import DetailViewBaseGeneric, ListViewBaseGeneric

import database


class SessionDependency(pydantic.BaseModel):
    session: AsyncSession = fastapi.Depends(database.get_session)

    class Config:
        arbitrary_types_allowed = True


# def get_token(request: fastapi.Request):
#     session = request.session
#     if not session:
#         raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail='Not logged in')
#     return session['user']


def session_dependency_handler(
    view: fastapi_jsonapi.views.view_base.ViewBase,
    dto: SessionDependency,
    # token = fastapi.Depends(get_token),
) -> dict[str, Any]:
    return {
        "session": dto.session
    }


class DetailView(DetailViewBaseGeneric):
    data_layer_cls = SqlalchemyDataLayer

    method_dependencies: ClassVar = {
        HTTPMethod.ALL: HTTPMethodConfig(dependencies = SessionDependency, prepare_data_layer_kwargs = session_dependency_handler)
    }


class ListView(ListViewBaseGeneric):
    method_dependencies: ClassVar = {
        HTTPMethod.ALL: HTTPMethodConfig(dependencies = SessionDependency, prepare_data_layer_kwargs = session_dependency_handler)
    }
