import logging

from fastapi import FastAPI

from app.ratelimiter.sliding_window_log import SlidingWindowLog

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sliding Window Log Rate Limiter API", version="1.0.0")

sliding_window_log_limiter = SlidingWindowLog(window_size=10, request_limit=3)


@app.get("/slidingWindowLog")
async def sliding_window_log_request():
    logger.info("Sliding window log api call")
    allowed = sliding_window_log_limiter.rate_limit()
    if not allowed:
        return {"status": "sliding window log rate limited, please try again later"}
    return {"status": "request allowed"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
