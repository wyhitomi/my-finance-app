# health-check Specification

## Purpose
Lets operators, load balancers and CI smoke tests confirm the API process is running and which version is deployed.

## Requirements

### Requirement: Health endpoint reports liveness
The API SHALL expose `GET /api/v1/health` without authentication, returning HTTP 200 with a JSON body containing `status` equal to `"ok"` and the running `version`.

#### Scenario: Service is up
- **GIVEN** the API is running
- **WHEN** a client sends `GET /api/v1/health`
- **THEN** the response status is 200
- **AND** the body is `{"status": "ok", "version": "<semver>"}`

### Requirement: API contract is published
The API SHALL publish its OpenAPI document at `GET /api/openapi.json`, including every `/api/v1` route.

#### Scenario: OpenAPI lists the health route
- **WHEN** a client sends `GET /api/openapi.json`
- **THEN** the response status is 200
- **AND** the document contains the path `/api/v1/health`
