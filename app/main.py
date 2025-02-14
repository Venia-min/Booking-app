import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.logger import logger
from app.pages.router import router as router_pages
from app.users.router import router as router_users


# # Redis are necessary
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    print("lifespan started")
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    print("Cache init")
    yield
    print("lifespan ended")
    await redis.close()


app = FastAPI(lifespan=lifespan)

# Sentry configuration
if settings.MODE != "TEST":
    sentry_sdk.init(
        dsn="https://5785d3a2a2f51d15812b29e35425a55b@o4508801822097408.ingest.de.sentry.io/4508801831469136",
        send_default_pii=True,
        traces_sample_rate=1.0,
        _experiments={
            "continuous_profiling_auto_start": True,
        },
    )

# Routers
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)

# Additional routers
app.include_router(router_pages)
app.include_router(router_images)

# CORSM middleware
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


# Logging middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.monotonic()
    response = await call_next(request)
    process_time = time.monotonic() - start_time
    logger.info(
        "Request handling time", extra={"process_time": round(process_time, 4)}
    )
    return response


# # FastAPI API versioning
# app = VersionedFastAPI(
#     app,
#     version_format="{major}",
#     prefix_format="/v{major}",
# )

# Redis for testing
if settings.MODE == "TEST":
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")

# Derpicated
# @app.on_event("startup")
# def startup():
#     redis = aioredis.from_url(
#         f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
#         encoding="utf8",
#         decode_responses=True,
#     )
#     FastAPICache.init(RedisBackend(redis), prefix="cache")


# Admin panel
admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(BookingsAdmin)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), "static")

# Prometheus configuration
# metrics_app = make_asgi_app()
# app.mount("/metrics", metrics_app)
instrumentator = Instrumentator(
    should_group_status_codes=False,  # Disable status grouping (200, 400, etc.)
    should_ignore_untemplated=True,  # Ignore requests that don’t match
    excluded_handlers=["/metrics", r"/admin.*"],  # Exclude certain endpoints
)

instrumentator.instrument(app).expose(app)
