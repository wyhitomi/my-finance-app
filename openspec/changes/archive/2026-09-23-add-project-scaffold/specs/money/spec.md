# Spec Delta

## Purpose

Guarantees that every monetary amount in the system is exact, carries its currency, and is never subject to floating-point rounding errors.

## ADDED Requirements

### Requirement: Monetary amounts are exact decimals with a currency
Every monetary amount SHALL be an exact decimal paired with an ISO 4217 currency code. Amounts SHALL NOT be created from binary floating-point numbers.

#### Scenario: Exact addition
- **WHEN** 0.10 BRL is added to 0.20 BRL
- **THEN** the result is exactly 0.30 BRL

#### Scenario: Floats are rejected
- **WHEN** a monetary amount is created from the float 0.1
- **THEN** creation fails with a validation error

#### Scenario: Unknown currency is rejected
- **WHEN** a monetary amount is created with currency code `XYZ`
- **THEN** creation fails with a validation error

### Requirement: Currencies are never mixed implicitly
Arithmetic and comparison between amounts of different currencies SHALL fail instead of converting implicitly.

#### Scenario: Adding different currencies
- **WHEN** 10.00 BRL is added to 10.00 USD
- **THEN** the operation fails with a currency mismatch error

### Requirement: Rounding to the currency's minor unit
Rounding an amount to its currency SHALL use banker's rounding (half-even) at the currency's number of minor-unit digits.

#### Scenario: Half-even rounding
- **WHEN** 10.125 BRL and 10.135 BRL are rounded
- **THEN** the results are 10.12 BRL and 10.14 BRL

### Requirement: Monetary amounts serialize as strings
When exchanged over the API, a monetary amount SHALL be represented as `{"amount": "<decimal string>", "currency": "<ISO 4217>"}`.

#### Scenario: Serialization
- **WHEN** 1234.50 BRL is serialized
- **THEN** the result is `{"amount": "1234.50", "currency": "BRL"}`
