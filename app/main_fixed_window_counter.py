import logging

from fastapi import FastAPI

from app.ratelimiter.fixed_window_counter import FixedWindowCounter

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title="Fixed Window Counter Rate Limiter API", version="1.0.0")

fixed_window_counter_limiter = FixedWindowCounter(window_size=60, max_requests=3)


@app.get("/fixedWindowCounter")
async def fixed_window_counter_request():
    logger.info("Fixed window counter api call")
    allowed = fixed_window_counter_limiter.rate_limit()
    if not allowed:
        return {"status": "fixed window counter rate limited, please try again later"}
    return {"status": "request allowed"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
