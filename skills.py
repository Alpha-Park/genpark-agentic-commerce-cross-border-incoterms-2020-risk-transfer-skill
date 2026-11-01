# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-agentic-commerce-cross-border-incoterms-2020-risk-transfer-skill
Category: agentic_commerce
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def allocate_incoterms_cost_and_risk(incoterm_rule, origin_charges_usd, main_ocean_freight_usd, destination_charges_usd, customs_duty_import_usd, cargo_commercial_value_usd):
    rule = incoterm_rule.strip().upper()
    
    # Cost allocation matrix
    # Seller responsibility breakdown
    seller_pays = {"origin_charges": False, "freight": False, "insurance": False, "dest_charges": False, "import_duty": False}
    risk_transfer_point = ""
    insurance_mandate = "NONE"
    
    if rule == "EXW":
        risk_transfer_point = "Seller's factory / warehouse floor before loading"
    elif rule == "FCA":
        seller_pays["origin_charges"] = True
        risk_transfer_point = "Loaded onto buyer's carrier at designated origin point"
    elif rule == "FOB":
        seller_pays["origin_charges"] = True
        risk_transfer_point = "On board the vessel at origin port of loading"
    elif rule == "CFR":
        seller_pays["origin_charges"] = True
        seller_pays["freight"] = True
        risk_transfer_point = "On board the vessel at origin port of loading (Risk transfers before transit!)"
    elif rule == "CIF":
        seller_pays["origin_charges"] = True
        seller_pays["freight"] = True
        seller_pays["insurance"] = True
        risk_transfer_point = "On board the vessel at origin port of loading"
        insurance_mandate = "Institute Cargo Clauses (C) - Minimum 110% CIF value"
    elif rule == "DAP":
        seller_pays["origin_charges"] = True
        seller_pays["freight"] = True
        seller_pays["dest_charges"] = True
        risk_transfer_point = "At disposal of buyer on arriving transport at named destination"
    elif rule == "DDP":
        seller_pays["origin_charges"] = True
        seller_pays["freight"] = True
        seller_pays["dest_charges"] = True
        seller_pays["import_duty"] = True
        risk_transfer_point = "Cleared for import at buyer's destination premises"
    else:
        raise ValueError(f"Unsupported Incoterm rule: {incoterm_rule}")
        
    seller_total = 0.0
    buyer_total = 0.0
    
    if seller_pays["origin_charges"]: seller_total += origin_charges_usd
    else: buyer_total += origin_charges_usd
    
    if seller_pays["freight"]: seller_total += main_ocean_freight_usd
    else: buyer_total += main_ocean_freight_usd
    
    if seller_pays["dest_charges"]: seller_total += destination_charges_usd
    else: buyer_total += destination_charges_usd
    
    if seller_pays["import_duty"]: seller_total += customs_duty_import_usd
    else: buyer_total += customs_duty_import_usd
    
    return {
        "incoterm_2020_rule": rule,
        "risk_transfer_boundary": risk_transfer_point,
        "marine_insurance_obligation": insurance_mandate,
        "seller_total_logistics_cost_usd": round(seller_total, 2),
        "buyer_total_logistics_cost_usd": round(buyer_total, 2),
        "seller_cost_responsibility": seller_pays,
        "landed_cost_multiplier": round((cargo_commercial_value_usd + seller_total + buyer_total) / cargo_commercial_value_usd, 3)
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "allocate_incoterms_cost_and_risk",
                        "description": """Allocate transportation costs, customs liabilities, and cargo risk transfer points across ICC Incoterms 2020 rules (EXW, FCA, FOB, CFR, CIF, DAP, DDP).
Identifies marine cargo insurance obligations (Institute Cargo Clauses A vs C) and port destination risk triggers.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = allocate_incoterms_cost_and_risk(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'incoterm_rule': 'CIF', 'origin_charges_usd': 650.0, 'main_ocean_freight_usd': 3200.0, 'destination_charges_usd': 850.0, 'customs_duty_import_usd': 1450.0, 'cargo_commercial_value_usd': 45000.0}
        out = allocate_incoterms_cost_and_risk(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
