# Rate Limiters

A FastAPI application demonstrating rate limiting algorithms: **Token Bucket**, **Leaky Bucket**, and **Fixed Window Counter**.

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

### Fixed Window Counter Algorithm

The Fixed Window Counter algorithm divides time into fixed-duration windows and counts requests within each window. It's one of the simplest rate limiting approaches.

**How it works:**
1. Time is divided into fixed windows (e.g., 60-second intervals)
2. Each window has a maximum request limit (counter)
3. When a request arrives, the counter is decremented
4. If the counter reaches zero, subsequent requests are rejected
5. When the window expires, the counter resets to the maximum

**Characteristics:**
- Simple to implement and understand
- Memory efficient (only stores a counter and timestamp)
- Can have burst issues at window boundaries (2x burst possible)
- Good for simple rate limiting needs

```
[Fixed Window Counter]
    Window: 60 seconds
    ┌─────────────────────────────────────┐
    │  Window 1     │  Window 2     │ ... │
    │  [3 requests] │  [3 requests] │     │
    └─────────────────────────────────────┘
           │
           ▼
    Counter: 3 → 2 → 1 → 0 (rate limited)
                          │
                          ▼ window expires
                    Counter resets to 3
```

### Key Differences

| Aspect | Token Bucket | Leaky Bucket | Fixed Window Counter |
|--------|--------------|--------------|----------------------|
| Burst handling | Allows bursts | Smooths bursts | Allows bursts (2x at boundary) |
| Request processing | Immediate | Queued | Immediate |
| Output rate | Variable (up to burst) | Constant | Variable within window |
| Memory usage | Low | Higher (queue) | Very low |
| Use case | APIs with occasional spikes | Strict rate enforcement | Simple rate limiting |

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

### Fixed Window Counter

Start the Fixed Window Counter server:
```bash
uvicorn app.main_fixed_window_counter:app --reload
```

The Fixed Window Counter is configured with a 60-second window and allows 3 requests per window.

1. **Submit a request:**
```bash
curl http://localhost:8000/fixedWindowCounter
```

Response:
```json
{"status": "request allowed"}
```

2. **Test rate limiting** by sending multiple rapid requests:
```bash
for i in {1..5}; do curl http://localhost:8000/fixedWindowCounter; echo; done
```

After 3 requests, you'll see:
```json
{"status": "fixed window counter rate limited, please try again later"}
```

The counter will reset after 60 seconds.

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
