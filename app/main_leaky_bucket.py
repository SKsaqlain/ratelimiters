import logging
import uuid

from fastapi import FastAPI

from app.ratelimiter.leaky_bucket import LeakyBucket

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title="Leaky Bucket Rate Limiter API", version="1.0.0")

leaky_bucket_response = dict()
leaky_bucket_rate_limiter = LeakyBucket(3, 3)


@app.get("/leakyBucket")
async def leaky_bucket_request():
    ref_id = uuid.uuid4()
    logger.info(f"Leaky bucket api call with ref_id {ref_id}")
    allowed = leaky_bucket_rate_limiter.rate_limit(process_leaky_bucket_call, ref_id)
    if not allowed:
        return {"status": "leaky bucket rate limited, please try again later"}
    return {"status": f"added to bucket, your request will be processed in some time {ref_id}"}


@app.get("/leakyBucket/{ref_id}")
async def leaky_bucket_get_response(ref_id: str):
    logger.debug(f"Checking response for ref_id: {ref_id}")
    if ref_id in leaky_bucket_response:
        response = leaky_bucket_response[ref_id]
        del leaky_bucket_response[ref_id]
        return response
    else:
        logger.warning(f"No response present with ref id: {ref_id}")
        return {"status": f"No response present with ref id: {ref_id}"}


def process_leaky_bucket_call(*args):
    ref_id = args[0]
    logger.info(f"Processing leaky bucket call ref_id: {ref_id}")
    leaky_bucket_response[str(ref_id)] = f"Processing leaky bucket call ref_id: {ref_id}"


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
