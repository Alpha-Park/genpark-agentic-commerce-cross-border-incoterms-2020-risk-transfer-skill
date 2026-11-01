# genpark-agentic-commerce-cross-border-incoterms-2020-risk-transfer-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

Incoterms 2020 (FOB vs CIF vs DDP) marine insurance, cargo risk transfer demarcation & freight cost allocator.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `allocate_incoterms_cost_and_risk`
- **Category**: `agentic_commerce`

### Method Documentation
Allocate transportation costs, customs liabilities, and cargo risk transfer points across ICC Incoterms 2020 rules (EXW, FCA, FOB, CFR, CIF, DAP, DDP).
Identifies marine cargo insurance obligations (Institute Cargo Clauses A vs C) and port destination risk triggers.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "allocate_incoterms_cost_and_risk",
    "arguments": {
    "incoterm_rule": "CIF",
    "origin_charges_usd": 650.0,
    "main_ocean_freight_usd": 3200.0,
    "destination_charges_usd": 850.0,
    "customs_duty_import_usd": 1450.0,
    "cargo_commercial_value_usd": 45000.0
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
