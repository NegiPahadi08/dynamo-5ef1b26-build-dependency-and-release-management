import json
import os
import hashlib
import pytest

OUTPUT_PATH = "/app/reconciled_state.json"
FALLBACK_PATH = "reconciled_state.json"

def load_output():
    path = OUTPUT_PATH if os.path.exists(OUTPUT_PATH) else FALLBACK_PATH
    assert os.path.exists(path), f"Output file not found at {OUTPUT_PATH} or {FALLBACK_PATH}"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def test_file_exists_and_valid_json():
    data = load_output()
    assert isinstance(data, dict), "Output JSON must be an object"

def test_required_keys():
    data = load_output()
    required_keys = ["last_applied_index", "last_applied_term", "state", "state_hash"]
    for key in required_keys:
        assert key in data, f"Missing required key: {key}"

def test_canonical_state_and_hash():
    data = load_output()
    state = data["state"]
    assert isinstance(state, dict), "'state' must be a JSON dictionary"
    
    canonical_bytes = json.dumps(state, sort_keys=True, separators=(',', ':')).encode('utf-8')
    computed_hash = hashlib.sha256(canonical_bytes).hexdigest()
    
    assert data["state_hash"] == computed_hash, f"state_hash mismatch! Expected {computed_hash}, got {data['state_hash']}"

def test_reconciled_values():
    data = load_output()
    assert data["last_applied_index"] == 5
    assert data["last_applied_term"] == 3
    assert data["state"].get("cluster_name") == "prod-east"
    assert data["state"].get("timeout_ms") == 5000
    assert data["state"].get("auth_enabled") is True
