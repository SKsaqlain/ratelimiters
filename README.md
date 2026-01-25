# Rate Limiters

A FastAPI application demonstrating rate limiting algorithms: **Token Bucket** , **Leaky Bucket**.

## Theory

### Token Bucket Algorithm

The Token Bucket algorithm controls the rate of requests by using a bucket that holds tokens. Each token represents permission to process one request.

**How it works:**
1. A bucket has a maximum capacity of `N` tokens
2. Tokens are added to the bucket at a fixed rate (e.g., 1 token per second)
3. When a request arrives, it consumes one token from the bucket
4. If the bucket is empty, the request is rejected (rate limited)
5. Tokens cannot exceed the bucket's maximum capacity

**Characteristics:**
- Allows bursts of traffic up to the bucket size
- Smooths out traffic over time
- Requests are processed immediately if tokens are available
- Good for APIs where occasional bursts are acceptable

```
[Token Bucket]
    ┌─────────────┐
    │ ● ● ● ● ●   │  ← Bucket (capacity: 5)
    └──────┬──────┘
           │ consume token
           ▼
      [Request] → Allowed (if token available)
                → Rejected (if bucket empty)

    Tokens refill at fixed rate (e.g., 1/second)
```

### Leaky Bucket Algorithm

The Leaky Bucket algorithm shapes traffic by processing requests at a constant rate, like water leaking from a bucket at a steady pace.

**How it works:**
1. Incoming requests are added to a queue (the bucket)
2. The queue has a maximum size; if full, new requests are rejected
3. Requests are processed (leaked) from the queue at a fixed rate
4. This ensures a constant, predictable output rate

**Characteristics:**
- Enforces a strict, constant processing rate
- Queues requests for later processing instead of immediate execution
- Smooths out bursts completely
- Good for systems requiring predictable throughput

```
[Leaky Bucket]
    Incoming requests
           │
           ▼
    ┌─────────────┐
    │ ■ ■ ■ ■ ■   │  ← Queue (max size: 5)
    └──────┬──────┘
           │ process at fixed rate
           ▼
      [Processed] → One request per interval
```

### Key Differences

| Aspect | Token Bucket | Leaky Bucket |
|--------|--------------|--------------|
| Burst handling | Allows bursts | Smooths bursts |
| Request processing | Immediate | Queued |
| Output rate | Variable (up to burst) | Constant |
| Use case | APIs with occasional spikes | Strict rate enforcement |

## Project Setup

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ratelimiters
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Testing the Rate Limiters

### Leaky Bucket

Start the Leaky Bucket server:
```bash
uvicorn app.main_leaky_bucket:app --reload
```

The Leaky Bucket is configured with a queue size of 3 and processes requests every 3 seconds.

1. **Submit a request:**
```bash
curl http://localhost:8000/leakyBucket
```

Response:
```json
{"status": "added to bucket, your request will be processed in some time <ref_id>"}
```

2. **Check the result** (using the ref_id from the response):
```bash
curl http://localhost:8000/leakyBucket/<ref_id>
```

3. **Test rate limiting** by sending multiple rapid requests:
```bash
for i in {1..5}; do curl http://localhost:8000/leakyBucket; echo; done
```

After 3 requests, you'll see:
```json
{"status": "leaky bucket rate limited, please try again later"}
```

### Token Bucket

Start the Token Bucket server:
```bash
uvicorn app.main_token_bucket:app --reload
```

The Token Bucket is configured with 5 tokens and refills 1 token every 2 seconds.

1. **Submit a request:**
```bash
curl http://localhost:8000/tokenBucket
```

Response:
```json
{"status": "request allowed"}
```

2. **Test rate limiting** by sending multiple rapid requests:
```bash
for i in {1..7}; do curl http://localhost:8000/tokenBucket; echo; done
```

After 5 requests, you'll see:
```json
{"status": "token bucket rate limited, please try again later"}
```

### API Documentation

FastAPI provides automatic interactive documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{"status": "healthy"}
```
