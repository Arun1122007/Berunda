from __future__ import annotations

import numpy as np

from src.ml.evaluation import ModelEvaluator, ValidationSuite
from src.ml.features import (
    CaseFeatureExtractor,
    EntityFeatureExtractor,
    FeaturePipeline,
    GeoFeatureExtractor,
)
from src.ml.inference import ModelRegistry
from src.ml.monitoring import AlertManager, BiasMonitor, DataQualityChecker, DriftDetector
from src.ml.preprocessing import FeatureScaler, Preprocessor
from src.ml.registry import ArtifactStore, DeploymentTracker, ModelVersion
from src.ml.training import ModelTrainer, TrainConfig, train_model_async


class TestFeatures:
    def test_case_extractor_empty(self):
        ext = CaseFeatureExtractor()
        features = ext.extract([])
        assert features["case_count"] == 0

    def test_case_extractor_with_data(self):
        ext = CaseFeatureExtractor()
        cases = [
            {"crimeHead": "Theft", "firDate": "2024-01-15"},
            {"crimeHead": "Assault", "firDate": "2024-06-20"},
        ]
        features = ext.extract(cases)
        assert features["case_count"] == 2
        assert features["offense_diversity"] == 1.0

    def test_entity_extractor(self):
        ext = EntityFeatureExtractor()
        entity = {"linkedCases": [1, 2, 3], "relationships": [1], "avgRiskScore": 0.5}
        features = ext.extract(entity)
        assert features["link_count"] == 3
        assert features["relationship_count"] == 1

    def test_geo_extractor_empty(self):
        ext = GeoFeatureExtractor()
        features = ext.extract([])
        assert features["case_density"] == 0

    def test_feature_pipeline(self):
        pipe = FeaturePipeline()
        cases = [{"crimeHead": "Theft", "firDate": "2024-01-15", "districtCode": "KA01"}]
        features = pipe.extract_all(cases=cases)
        assert "case_count" in features
        assert "offense_diversity" in features


class TestTraining:
    def test_trainer_creation(self):
        trainer = ModelTrainer()
        assert trainer.config.test_size == 0.2

    def test_train_config_defaults(self):
        cfg = TrainConfig()
        assert cfg.model_type == "linear"
        assert cfg.cv_folds == 5

    def test_train_baseline(self):
        cfg = TrainConfig(model_type="baseline")
        trainer = ModelTrainer(cfg)
        x_data = np.random.rand(20, 3)
        y = np.random.randint(0, 2, 20)
        metrics = trainer.train(x_data, y)
        assert "train_score" in metrics
        assert "test_score" in metrics

    def test_cross_validate(self):
        trainer = ModelTrainer()
        x_data = np.random.rand(30, 3)
        y = np.random.randint(0, 2, 30)
        cv = trainer.cross_validate(x_data, y)
        assert "mean_score" in cv
        assert "std_score" in cv

    def test_get_model(self):
        trainer = ModelTrainer()
        x_data = np.random.rand(20, 3)
        y = np.random.randint(0, 2, 20)
        trainer.train(x_data, y, "test_model")
        model = trainer.get_model("test_model")
        assert model is not None

    def test_train_model_async(self):
        x_data = np.random.rand(20, 3)
        y = np.random.randint(0, 2, 20)
        result = train_model_async(x_data, y)
        assert "train_score" in result


class TestInference:
    def test_registry_singleton(self):
        r1 = ModelRegistry()
        r2 = ModelRegistry()
        assert r1 is r2

    def test_register_and_get(self):
        reg = ModelRegistry()
        reg.register("test", "dummy_model")
        assert reg.get("test") == "dummy_model"

    def test_list_models(self):
        reg = ModelRegistry()
        reg.register("a", "model_a", {"version": "1"})
        reg.register("b", "model_b", {"version": "2"})
        models = reg.list_models()
        assert "a" in models
        assert "b" in models

    def test_deregister(self):
        reg = ModelRegistry()
        reg.register("test", "model")
        assert reg.deregister("test")
        assert not reg.deregister("nonexistent")


class TestEvaluation:
    def test_evaluate_metrics(self):
        ev = ModelEvaluator()
        y_true = np.array([0, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 1])
        metrics = ev.evaluate(y_true, y_pred)
        assert metrics.accuracy == 1.0
        assert metrics.precision == 1.0

    def test_classification_report(self):
        ev = ModelEvaluator()
        y_true = np.array([0, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 1])
        report = ev.classification_report(y_true, y_pred)
        assert "0" in report
        assert "1" in report

    def test_validation_suite(self):
        vs = ValidationSuite()
        y_true = np.array([0, 1, 0, 1])
        y_pred = np.array([0, 0, 0, 1])
        results = vs.run_checks(y_true, y_pred)
        assert len(results) >= 1

    def test_confusion_matrix(self):
        ev = ModelEvaluator()
        y_true = np.array([0, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 1])
        cm = ev.confusion_matrix(y_true, y_pred)
        assert len(cm) == 2


class TestRegistry:
    def test_model_version_creation(self):
        mv = ModelVersion("test", "1.0", "linear", metrics={"accuracy": 0.9})
        assert mv.name == "test"
        assert mv.version == "1.0"
        assert mv.version_hash

    def test_model_version_hash(self):
        mv1 = ModelVersion("test", "1.0", "linear")
        mv2 = ModelVersion("test", "1.0", "linear")
        assert mv1.version_hash != mv2.version_hash  # different timestamps

    def test_artifact_store(self, tmp_path):
        store = ArtifactStore(base_path=str(tmp_path / "models"))
        path = store.save("dummy_model_content", "test_model", "v1")
        assert path.endswith("model.pkl")
        loaded = store.load("test_model", "v1")
        assert loaded == "dummy_model_content"

    def test_deployment_tracker(self, tmp_path):
        tracker = DeploymentTracker(state_path=str(tmp_path / "deployments.json"))
        tracker.deploy("model_a", "1.0", "production")
        dep = tracker.get_deployment("production")
        assert dep["model_name"] == "model_a"


class TestPreprocessing:
    def test_normalize(self):
        p = Preprocessor()
        data = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
        normalized = p.normalize(data)
        assert normalized.shape == data.shape

    def test_minmax_scale(self):
        p = Preprocessor()
        data = np.array([[1.0], [2.0], [3.0]])
        scaled = p.minmax_scale(data)
        assert scaled.min() >= 0.0
        assert scaled.max() <= 1.0

    def test_encode_categorical(self):
        p = Preprocessor()
        import pandas as pd

        series = pd.Series(["a", "b", "c", "a"])
        encoded = p.encode_categorical(series)
        assert len(encoded) == 4
        assert encoded[0] == encoded[3]  # same category

    def test_feature_scaler(self):
        fs = FeatureScaler()
        data = np.array([[1.0, 2.0], [3.0, 4.0]])
        transformed = fs.fit_transform(data, "test")
        assert transformed.shape == data.shape
        same = fs.transform(data, "test")
        assert same.shape == data.shape


class TestMonitoring:
    def test_drift_detector(self):
        dd = DriftDetector()
        ref = np.random.rand(100, 3)
        curr = np.random.rand(50, 3)
        result = dd.detect(ref, curr)
        assert "drift_detected" in result

    def test_data_quality(self):
        qc = DataQualityChecker()
        data = np.array([[1.0, 2.0], [3.0, np.nan]])
        result = qc.check(data)
        assert result["nan_count"] == 1
        assert not result["passed"]

    def test_bias_monitor(self):
        bm = BiasMonitor()
        y_pred = np.array([0.8, 0.2, 0.7, 0.3])
        sensitive = np.array([0, 1, 0, 1])
        result = bm.check(y_pred, sensitive)
        assert "group_rates" in result
        assert "max_disparity" in result

    def test_alert_manager(self):
        am = AlertManager()
        alert = am.check_and_alert("drift", False, {"drift": True})
        assert alert is not None
        assert len(am.get_alerts()) == 1
        am.clear_alerts()
        assert len(am.get_alerts()) == 0
