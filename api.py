from typing import Any, ClassVar

import fastapi
import fastapi_jsonapi
import pydantic
import sqlalchemy
from fastapi_jsonapi.views.utils import HTTPMethod, HTTPMethodConfig
from fastapi_jsonapi.misc.sqla.generics.base import DetailViewBaseGeneric, ListViewBaseGeneric

import database


class SessionDependency(pydantic.BaseModel):
    session: sqlalchemy.ext.asyncio.AsyncSession = fastapi.Depends(database.Connector.get_session)

    class Config:
        arbitrary_types_allowed = True


def get_token(request: fastapi.Request):
    session = request.session
    if not session:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail='Not logged in')
    return session['user']


def session_dependency_handler(
    view: fastapi_jsonapi.views.view_base.ViewBase,
    dto: SessionDependency,
    token = fastapi.Depends(get_token),
) -> dict[str, Any]:
    return {
        "session": dto.session
    }


class BaseDetailView(DetailViewBaseGeneric):
    method_dependencies: ClassVar = {
        HTTPMethod.ALL: HTTPMethodConfig(dependencies = SessionDependency, prepare_data_layer_kwargs = session_dependency_handler)
    }


class BaseListView(ListViewBaseGeneric):
    method_dependencies: ClassVar = {
        HTTPMethod.ALL: HTTPMethodConfig(dependencies = SessionDependency, prepare_data_layer_kwargs = session_dependency_handler)
    }
