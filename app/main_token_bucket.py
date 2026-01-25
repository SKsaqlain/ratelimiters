import logging

from fastapi import FastAPI

from app.ratelimiter.token_bucket import TokenBucket

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title="Token Bucket Rate Limiter API", version="1.0.0")

token_bucket_rate_limiter = TokenBucket(bucket_size=5, refill_seconds=2)


@app.get("/tokenBucket")
async def token_bucket_request():
    logger.info("Token bucket api call")
    allowed = token_bucket_rate_limiter.rate_limit()
    if not allowed:
        return {"status": "token bucket rate limited, please try again later"}
    return {"status": "request allowed"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
