"""ML module — risk scoring, feature engineering, training, inference, and monitoring."""

from src.ml.evaluation import EvalMetrics, ModelEvaluator, ValidationSuite
from src.ml.features import (
    BaseFeatureExtractor,
    CaseFeatureExtractor,
    EntityFeatureExtractor,
    FeaturePipeline,
    GeoFeatureExtractor,
)
from src.ml.inference import BatchPredictor, ModelRegistry, predict_model
from src.ml.monitoring import AlertManager, BiasMonitor, DataQualityChecker, DriftDetector
from src.ml.preprocessing import FeatureScaler, Preprocessor
from src.ml.registry import ArtifactStore, DeploymentTracker, ModelVersion
from src.ml.training import ModelTrainer, TrainConfig, train_model_async

__all__ = [
    "BaseFeatureExtractor",
    "CaseFeatureExtractor",
    "EntityFeatureExtractor",
    "GeoFeatureExtractor",
    "FeaturePipeline",
    "ModelTrainer",
    "TrainConfig",
    "train_model_async",
    "ModelRegistry",
    "BatchPredictor",
    "predict_model",
    "ModelEvaluator",
    "ValidationSuite",
    "EvalMetrics",
    "ModelVersion",
    "ArtifactStore",
    "DeploymentTracker",
    "Preprocessor",
    "FeatureScaler",
    "DriftDetector",
    "DataQualityChecker",
    "BiasMonitor",
    "AlertManager",
]
