# Plant Mock API — Technical Reference

## Overview

Plant Mock API is a RESTful service that provides plant taxonomy and care data for smart greenhouse applications. It serves as a mock third-party data source when creating or enriching plant entities.

| Attribute | Value |
|-----------|-------|
| Version | 1.0.0 |
| Protocol | HTTP/1.1, HTTPS |
| Content-Type | `application/json` |
| Base URL | `http://localhost:8000` (default) |

---

## Authentication

All endpoints under `/v1/` require API key authentication.

### Supported Methods

| Header | Format |
|--------|--------|
| `X-API-Key` | `X-API-Key: <api_key>` |
| `Authorization` | `Authorization: Bearer <api_key>` |

### Unauthenticated Response

| Status | Description |
|--------|-------------|
| `401 Unauthorized` | Missing or invalid API key |

Response body:

```json
{
  "detail": "Missing API key. Provide X-API-Key header or Authorization: Bearer <key>"
}
```

---

## Endpoints

### GET /health

Liveness probe. No authentication required.

**Response:** `200 OK`

```json
{
  "status": "ok"
}
```

---

### GET /v1/plants

List plants with optional filters.

**Query parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `search` | string | No | Filter by scientific or common name (case-insensitive substring match) |
| `family` | string | No | Filter by plant family (case-insensitive) |

**Response:** `200 OK`

```json
{
  "plants": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "scientific_name": "Monstera deliciosa",
      "common_name": "Swiss Cheese Plant",
      "family": "Araceae",
      "genus": "Monstera",
      "species": "deliciosa",
      "description": "Tropical plant with iconic split leaves.",
      "native_region": "Central America",
      "care": {
        "watering_frequency": "weekly",
        "light_requirement": "bright indirect",
        "humidity_range": { "min": 60, "max": 80 },
        "temperature_range_c": { "min": 18, "max": 27 },
        "soil_type": "well-draining, peat-based",
        "fertilizing": "monthly in growing season"
      }
    }
  ]
}
```

---

### GET /v1/plants/search

Search plants by name.

**Query parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | Yes | Search query (min length: 1). Matches scientific and common names. |

**Response:** `200 OK`

Returns the same structure as `GET /v1/plants`.

---

### GET /v1/plants/{plant_id}

Retrieve a single plant by ID.

**Path parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `plant_id` | UUID | Plant identifier |

**Responses**

| Status | Description |
|--------|-------------|
| `200 OK` | Plant found |
| `404 Not Found` | Plant does not exist |

**Response body (200):** Single plant object (no `plants` wrapper).

---

## Data Models

### Plant

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique identifier |
| `scientific_name` | string | Binomial nomenclature |
| `common_name` | string | Vernacular name |
| `family` | string | Plant family |
| `genus` | string | Genus |
| `species` | string | Species |
| `description` | string \| null | Short description |
| `native_region` | string \| null | Native geographic region |
| `care` | Care \| null | Care requirements |

### Care

| Field | Type | Description |
|-------|------|-------------|
| `watering_frequency` | string \| null | e.g. `"weekly"` |
| `light_requirement` | string \| null | e.g. `"bright indirect"` |
| `humidity_range` | `{ min: number, max: number }` \| null | Relative humidity (%) |
| `temperature_range_c` | `{ min: number, max: number }` \| null | Temperature in Celsius |
| `soil_type` | string \| null | e.g. `"well-draining"` |
| `fertilizing` | string \| null | Fertilization schedule |

---

## Interactive Documentation

API reference (Scalar) is available at:

```
GET /docs
```

No authentication required. Use it to explore endpoints and make test requests.

---

## Configuration

Environment variables:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `DATABASE_URL` | string | `postgresql+asyncpg://plantuser:plantpass@localhost:5433/plant_mock_db` | PostgreSQL connection string (asyncpg driver) |
| `API_KEY_HEADER` | string | `X-API-Key` | Header name for API key |
| `SECRET_KEY` | string | — | Reserved |
| `DEBUG` | bool | `false` | Enable SQL query logging |

---

## Deployment

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 16 (or use provided Docker setup)

### Database (Docker)

```bash
docker-compose up -d postgres
```

| Setting | Value |
|---------|-------|
| Host | `localhost` |
| Port | `5433` |
| Database | `plant_mock_db` |
| User | `plantuser` |
| Password | `plantpass` |

Port 5433 is used to avoid conflicts with a local PostgreSQL on 5432.

### Application

```bash
# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env

# Migrate
alembic upgrade head

# Seed data and create API key
python -m scripts.seed_plants

# Run
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Add API Key

```bash
python -m scripts.add_api_key <key_name>
```

The plain API key is printed once. Store it securely.

### Docker Commands

```bash
docker-compose stop postgres    # Stop
docker-compose start postgres   # Start
docker-compose down             # Remove container
docker-compose down -v          # Remove container and data
```

---

## Troubleshooting

### 401 — Password authentication failed for user "plantuser"

The client may be reaching a local PostgreSQL instance instead of the Docker container.

1. Ensure `DATABASE_URL` uses port `5433` for the Docker database.
2. Reset the database: `docker-compose down -v && docker-compose up -d postgres`
3. Wait ~15 seconds, then run `alembic upgrade head`.

### Verify database connectivity

```bash
docker-compose exec postgres psql -U plantuser -d plant_mock_db -c "SELECT 1"
```

### Port conflicts

Check host port 5433: `netstat -ano | findstr :5433` (Windows) or `lsof -i :5433` (macOS/Linux).
