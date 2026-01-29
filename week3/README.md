# Week 3 - FastAPI Smart Agriculture API

This module exposes sensor data and irrigation decisions via a REST API.

## Endpoints

### GET /
Health check.

### GET /status
Returns:
- Latest sensor readings
- Status evaluation (LOW / OK / HIGH)
- Irrigation decision

### GET /history
Returns last sensor records from CSV.

## Run
```bash
uvicorn app:app --reload
