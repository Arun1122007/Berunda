import json
from pathlib import Path


class ContractChecker:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.contract_path = Path(__file__).parent.parent.parent.parent / "docs" / "contracts"

    def load_contract(self, name: str) -> dict:
        path = self.contract_path / name
        if path.suffix == ".md":
            return {"status": "loaded", "file": str(path)}
        with open(path) as f:
            return json.load(f)

    def validate_endpoint(self, method: str, path: str, expected_status: int, actual_status: int) -> dict:
        return {
            "method": method,
            "path": path,
            "expected_status": expected_status,
            "actual_status": actual_status,
            "match": expected_status == actual_status,
        }

    def validate_response_shape(self, expected_fields: list[str], actual_fields: list[str]) -> dict:
        missing = [f for f in expected_fields if f not in actual_fields]
        extra = [f for f in actual_fields if f not in expected_fields]
        return {
            "match": len(missing) == 0 and len(extra) == 0,
            "missing_fields": missing,
            "extra_fields": extra,
        }
