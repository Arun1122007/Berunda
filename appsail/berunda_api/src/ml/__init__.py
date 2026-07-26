"""ML module — risk scoring, feature engineering, training, inference, and monitoring."""

from src.ml.evaluation import (
    ClassificationEvaluator,
    EvalMetrics,
    ModelComparisonReport,
    ModelEvaluator,
    RegressionEvaluator,
    ValidationSuite,
)
from src.ml.features import (
    BaseFeatureExtractor,
    CaseFeatureExtractor,
    EntityFeatureExtractor,
    FeaturePipeline,
    FeatureStore,
    GeoFeatureExtractor,
    build_features,
    get_feature_names,
)
from src.ml.inference import BatchPredictor, CrimePredictor, ModelRegistry, PredictionExplanation, predict_model
from src.ml.monitoring import AlertManager, BiasMonitor, DataQualityChecker, DriftDetector
from src.ml.preprocessing import (
    DataValidator,
    FeatureScaler,
    Preprocessor,
    PreprocessingPipeline,
    clean_dataframe,
)
from src.ml.registry import ArtifactStore, DeploymentTracker, ModelRegistry as PersistentModelRegistry, ModelVersion
from src.ml.training import BaseTrainer, CrimePatternTrainer, HyperparamConfig, ModelTrainer, TrainConfig, train_model_async

__all__ = [
    "AlertManager",
    "ArtifactStore",
    "BaseFeatureExtractor",
    "BaseTrainer",
    "BatchPredictor",
    "BiasMonitor",
    "CaseFeatureExtractor",
    "ClassificationEvaluator",
    "CrimePatternTrainer",
    "CrimePredictor",
    "DataQualityChecker",
    "DataValidator",
    "DeploymentTracker",
    "DriftDetector",
    "EntityFeatureExtractor",
    "EvalMetrics",
    "FeaturePipeline",
    "FeatureScaler",
    "FeatureStore",
    "GeoFeatureExtractor",
    "HyperparamConfig",
    "ModelComparisonReport",
    "ModelEvaluator",
    "ModelRegistry",
    "ModelTrainer",
    "ModelVersion",
    "PersistentModelRegistry",
    "PredictionExplanation",
    "Preprocessor",
    "PreprocessingPipeline",
    "RegressionEvaluator",
    "TrainConfig",
    "ValidationSuite",
    "build_features",
    "clean_dataframe",
    "get_feature_names",
    "predict_model",
    "train_model_async",
]
