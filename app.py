from contextlib import asynccontextmanager

import uvicorn
import starlette
import fastapi
import fastapi_jsonapi
import authlib

import api
import database
import models



# oauth = authlib.integrations.starlette_client.OAuth(starlette.config.Config())
# oauth.register(
#     'authentik',
#     authorize_url = "http://localhost:9000/application/o/authorize/",
#     access_token_url = "http://localhost:9000/application/o/token/",
#     scope = "identify",
#     client_id = "client_id_here",
#     client_secret = "client_secret_here",
# )


def create_routes(app):
    router = fastapi.APIRouter()

    fastapi_jsonapi.RoutersJSONAPI(
        router = router,
        path = "/api/effect",
        tags = ["Effect"],
        class_detail = api.DetailView,
        class_list = api.ListView,
        model = models.Effect,
        schema = models.Effect,
        resource_type = "effect",
    )

    fastapi_jsonapi.RoutersJSONAPI(
        router = router,
        path = "/api/raw",
        tags = ["RawSample"],
        class_detail = api.DetailView,
        class_list = api.ListView,
        model = models.RawSample,
        schema = models.RawSample,
        resource_type = "raw",
    )

    fastapi_jsonapi.RoutersJSONAPI(
        router = router,
        path = "/api/refined",
        tags = ["RefinedSample"],
        class_detail = api.DetailView,
        class_list = api.ListView,
        model = models.RefinedSample,
        schema = models.RefinedSample,
        resource_type = "refined",
    )

    fastapi_jsonapi.RoutersJSONAPI(
        router = router,
        path = "/api/blood",
        tags = ["BloodSample"],
        class_detail = api.DetailView,
        class_list = api.ListView,
        model = models.BloodSample,
        schema = models.BloodSampleJsonApi,
        resource_type = "blood",
    )

    fastapi_jsonapi.RoutersJSONAPI(
        router = router,
        path = "/api/enlisted",
        tags = ["Enlisted"],
        class_detail = api.DetailView,
        class_list = api.ListView,
        model = models.Enlisted,
        schema = models.EnlistedJsonApi,
        resource_type = "enlisted",
    )

    app.include_router(router, prefix = "")


def root(request):
    return starlette.responses.HTMLResponse("""
<html>
  <body>
    <h1>Krystallivm</h1>
    <ul>
      <li><a href="/api/docs">Documentation</a></li>
      <li><a href="/api/effect">Effects</a></li>
      <li><a href="/api/raw">Raw Samples</a></li>
      <li><a href="/api/refined">Refined Samples</a></li>
      <li><a href="/api/blood">Blood Samples</a></li>
      <li><a href="/api/enlisted">Enlisted</a></li>
    </ul>
  </body>
</html>
""")


# async def login(request):
#     redirect_url = request.url_for('auth')
#     return oauth.authentik.authorize_redirect(request, redirect_url)
#
#
# async def auth(request):
#     try:
#         token = await oauth.authentik.authorize_access_token(request)
#     except authlib.integrations.starlette_client.OAuthError as e:
#         raise fastapi.HTTPException(
#             status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail = e.error
#         )
#
#     return token


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    await database.sqlalchemy_init()
    yield


def create_app():
    app = fastapi.FastAPI(
        title = "Krystalium Backend",
        lifespan = lifespan,
        openapi_url = "/openapi.json",
        docs_url = "/api/docs",
        debug = True,
    )

    # app.add_middleware(
    #     starlette.middleware.sessions.SessionMiddleware,
    #     secret_key = "secret_key_here",
    #     max_age = 3600 * 24 * 7,
    # )

    create_routes(app)
    app.add_route("/api", root)
    # app.add_route("/login", login)
    # app.add_route("/auth", auth)
    fastapi_jsonapi.init(app)
    return app


app = create_app()
