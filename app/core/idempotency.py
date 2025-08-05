import uuid
from fastapi import Request, HTTPException, status
from typing import Dict, Any, Tuple
from datetime import datetime, timedelta

idempotency_cache: Dict[str, Tuple[int, Any, datetime]] = {}
CACHE_EXPIRATION = timedelta(hours=24)

async def handle_idempotency(request: Request):
    idempotency_key = request.headers.get("Idempotency-Key")
    if not idempotency_key:
        return None

    now = datetime.utcnow()
    expired_keys = [
        key for key, (_, _, timestamp) in idempotency_cache.items() 
        if now > timestamp + CACHE_EXPIRATION
    ]
    for key in expired_keys:
        del idempotency_cache[key]

    if idempotency_key in idempotency_cache:
        status_code, response_body, _ = idempotency_cache[idempotency_key]
        raise HTTPException(
            status_code=status_code,
            detail=response_body,
            headers={"X-Idempotent-Replayed": "true"}
        )

    request.state.idempotency_key = idempotency_key
    return idempotency_key

def cache_idempotent_response(key: str, status_code: int, response_body: Any):
    if key:
        idempotency_cache[key] = (status_code, response_body, datetime.utcnow())