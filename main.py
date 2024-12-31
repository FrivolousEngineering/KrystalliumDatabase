import uvicorn
import starlette
import fastapi
import fastapi_jsonapi
import authlib

import api
import database
import schemas


oauth = authlib.integrations.starlette_client.OAuth(starlette.config.Config())
oauth.register(
    'authentik',
    authorize_url = "http://localhost:9000/application/o/authorize/",
    access_token_url = "http://localhost:9000/application/o/token/",
    scope = "identify",
    client_id = "client_id_here",
    client_secret = "client_secret_here",
)


def create_routes(app):
    router = fastapi.APIRouter()

    fastapi_jsonapi.RoutersJSONAPI(
        router = router,
        path = "/raw",
        tags = ["RawSample"],
        class_detail = api.BaseDetailView,
        class_list = api.BaseListView,
        model = database.RawSample,
        schema = schemas.RawSample,
        resource_type = "raw",
    )

    fastapi_jsonapi.RoutersJSONAPI(
        router = router,
        path = "/refined",
        tags = ["RefinedSample"],
        class_detail = api.BaseDetailView,
        class_list = api.BaseListView,
        model = database.RefinedSample,
        schema = schemas.RefinedSample,
        resource_type = "refined",
    )

    fastapi_jsonapi.RoutersJSONAPI(
        router = router,
        path = "/blood",
        tags = ["BloodSample"],
        class_detail = api.BaseDetailView,
        class_list = api.BaseListView,
        model = database.BloodSample,
        schema = schemas.BloodSample,
        resource_type = "blood",
    )

    app.include_router(router, prefix = "")


def root(request):
    return starlette.responses.HTMLResponse("""
<html>
  <body>
    <h1>Krystallivm</h1>
    <ul>
      <li><a href="/docs">Documentation</a></li>
      <li><a href="/api/raw">Raw Samples</a></li>
      <li><a href="/api/refined">Refined Samples</a></li>
      <li><a href="/api/blood">Blood Samples</a></li>
    </ul>
  </body>
</html>
""")


async def login(request):
    redirect_url = request.url_for('auth')
    return oauth.authentik.authorize_redirect(request, redirect_url)


async def auth(request):
    try:
        token = await oauth.authentik.authorize_access_token(request)
    except authlib.integrations.starlette_client.OAuthError as e:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = e.error
        )

    return token


def create_app():
    app = fastapi.FastAPI(title = "Krystalium Backend", debug = True, openapi_url = "/openapi.json", docs_url = "/docs")

    app.add_middleware(
        starlette.middleware.sessions.SessionMiddleware,
        secret_key = "secret_key_here",
        max_age = 3600 * 24 * 7,
    )

    create_routes(app)
    app.add_route("/", root)
    app.add_route("/login", login)
    app.add_route("/auth", auth)
    app.on_event("startup")(database.sqlalchemy_init)
    fastapi_jsonapi.init(app)
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 8000)
