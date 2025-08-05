import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi_i18n import I18nJsonResponse, i18n_init, _
from json import JSONDecodeError

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.idempotency import cache_idempotent_response

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.RATE_LIMIT_GUEST])

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Nutrichain logistics report service.",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "Idempotency-Key", "Accept-Language"],
    )

i18n_init(app, translation_source="json", translation_file_path="app/translations")

@app.middleware("http")
async def idempotency_and_logging_middleware(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    
    idempotency_key = request.state.idempotency_key if hasattr(request.state, 'idempotency_key') else None
    
    try:
        response = await call_next(request)
        
        if idempotency_key and response.status_code in [200, 201]:
            response_body_bytes = b""
            async for chunk in response.body_iterator:
                response_body_bytes += chunk
            
            try:
                response_body_json = json.loads(response_body_bytes)
                cache_idempotent_response(idempotency_key, response.status_code, response_body_json)
            except JSONDecodeError:
                pass
            
            return JSONResponse(
                content=json.loads(response_body_bytes), 
                status_code=response.status_code, 
                headers=dict(response.headers)
            )

        logger.info(f"Response: {response.status_code}")
        return response
    except Exception as exc:
        logger.error(f"Request failed: {exc}")
        if isinstance(exc, HTTPException) and exc.headers and exc.headers.get("X-Idempotent-Replayed") == "true":
            logger.info(f"Idempotent replay for key: {idempotency_key}")
            return I18nJsonResponse(content=exc.detail, status_code=exc.status_code, headers=exc.headers)
        
        raise exc


app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", summary="Health Check")
def read_root():
    """Helth check."""
    return I18nJsonResponse({"message": _("welcome_message")})