import joblib
import pandas as pd
from pathlib import Path
from .model_inference_entity import InferenceInputEntity

import joblib
import pandas as pd
import logging
from pathlib import Path
from .model_inference_entity import InferenceInputEntity

logger = logging.getLogger(__name__)

class ModelInferenceRepository:
    """Loads a trained model pipeline and performs predictions"""

    # Assuming project structure: project_root/models/solar_status_model.pkl
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    MODEL_PATH = BASE_DIR / "models" / "solar_status_model.pkl"

    def __init__(self):
        if not self.MODEL_PATH.exists():
            logger.error(f"Model file not found at {self.MODEL_PATH}")
            raise FileNotFoundError(f"Model file missing: {self.MODEL_PATH}")
        bundle = joblib.load(self.MODEL_PATH)
        self.pipeline = bundle.get("pipeline")
        self.label_encoder = bundle.get("label_encoder")
        logger.info(f"Loaded model from {self.MODEL_PATH}")

    def predict(self, inp: InferenceInputEntity) -> tuple[str, dict[str, float]]:
        """Run inference and return predicted label plus class probabilities"""
        df = pd.DataFrame([inp.model_dump()])
        # Predict probabilities and convert to Python floats
        proba_list = self.pipeline.predict_proba(df)[0].tolist()
        # Get encoded class labels from classifier, then decode to original status strings
        enc_classes = self.pipeline.named_steps["classifier"].classes_
        labels = self.label_encoder.inverse_transform(enc_classes)
        # Build a dict[str, float] mapping status->probability
        prob_dict = { label: float(proba_list[i]) for i, label in enumerate(labels) }
        # Predict encoded class and decode to status
        pred_enc = self.pipeline.predict(df)[0]
        pred = self.label_encoder.inverse_transform([pred_enc])[0]
        print(f"pred - {pred}, prob_dict - {prob_dict}")
        return pred, prob_dict
        try:
            # Create DataFrame preserving feature names for sklearn
            df = pd.DataFrame([inp.model_dump()])
            # Predict probabilities and convert to Python floats
            proba_list = self.pipeline.predict_proba(df)[0].tolist()
            # Get encoded class labels from classifier, then decode to original status strings
            enc_classes = self.pipeline.named_steps["classifier"].classes_
            labels = self.label_encoder.inverse_transform(enc_classes)
            # Build a dict[str, float] mapping status->probability
            prob_dict = { label: float(proba_list[i]) for i, label in enumerate(labels) }
            # Predict encoded class and decode to status
            pred_enc = self.pipeline.predict(df)[0]
            pred = self.label_encoder.inverse_transform([pred_enc])[0]
            print(f"pred - {pred}, prob_dict - {prob_dict}")
            return pred, prob_dict
        except Exception as e:
            logger.exception("Error during model inference")
            raise