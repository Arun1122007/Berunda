from __future__ import annotations

import json
from datetime import datetime, timezone

from sqlalchemy import select

from src.models.gov_models import FairnessCheckResult
from src.models.int_models import RiskScore, RiskScoreFeatureImportance
from src.models.src_models import CaseMaster
from src.schemas.fairness import FairnessCheckResponse
from src.services.base import BaseService


class FairnessService(BaseService):
    async def run_feature_audit(self, user: str = "system") -> FairnessCheckResponse:
        now = datetime.now(timezone.utc)
        findings: list[dict] = []
        all_passed = True

        scores = await self.session.execute(
            select(RiskScore).order_by(RiskScore.RiskScoreID.desc()).limit(100)
        )
        for score in scores.scalars().all():
            if not score.FeaturesJSON:
                continue
            try:
                features = json.loads(score.FeaturesJSON)
                sensitive = [
                    k
                    for k in features
                    if any(s in k.lower() for s in ["caste", "religion", "casteid", "religionid"])
                ]
                if sensitive:
                    all_passed = False
                    findings.append(
                        {
                            "type": "sensitive_feature_in_risk_model",
                            "severity": "critical",
                            "detail": f"RiskScore {score.RiskScoreID} contains: {sensitive}",
                        }
                    )
            except (json.JSONDecodeError, TypeError):
                pass

        importances = await self.session.execute(select(RiskScoreFeatureImportance).limit(200))
        for imp in importances.scalars().all():
            if any(s in (imp.FeatureName or "").lower() for s in ["caste", "religion"]):
                all_passed = False
                findings.append(
                    {
                        "type": "sensitive_feature_importance",
                        "severity": "critical",
                        "detail": (
                            f"Feature '{imp.FeatureName}' "
                            f"in RiskScoreImportance {imp.RiskScoreImportanceID}"
                        ),
                    }
                )

        cases = await self.session.execute(select(CaseMaster).limit(50))
        for case in cases.scalars().all():
            for complainant in case.complainants:
                if complainant.ReligionID is not None or complainant.CasteID is not None:
                    findings.append(
                        {
                            "type": "sensitive_data_in_complainant_record",
                            "severity": "info",
                            "detail": (
                                f"Case {case.CaseMasterID}: complainant has "
                                f"religion/caste data stored (audit only)"
                            ),
                        }
                    )

        status = "PASSED" if all_passed else "FLAGGED"
        details = (
            f"Feature audit {status}: checked {len(findings)} findings, "
            f"{sum(1 for f in findings if f['severity'] == 'critical')} critical."
        )

        result_model = FairnessCheckResult(
            CheckType="feature_audit",
            Timestamp=now,
            Passed=int(all_passed),
            Details=json.dumps(findings),
            CheckedBy=user,
        )
        self.session.add(result_model)
        await self.session.commit()

        return FairnessCheckResponse(
            CheckType="feature_audit",
            Passed=all_passed,
            Details=details,
            Findings=findings,
            CheckedBy=user,
            Timestamp=now,
        )
