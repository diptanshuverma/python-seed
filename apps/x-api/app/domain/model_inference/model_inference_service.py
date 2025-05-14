from .model_inference_repo import ModelInferenceRepository
from .model_inference_dto import InferenceInputDTO, InferenceResultDTO

class ModelInferenceService:
    """Service layer that applies business logic for model inference"""

    def __init__(self) -> None:
        self.repo = ModelInferenceRepository()

    def infer(self, data: InferenceInputDTO) -> InferenceResultDTO:
        """Perform model inference and wrap result in DTO"""
        pred, prob_dict = self.repo.predict(data)
        print(f"pred {pred}.. type is {type(pred)}, prob_dict {prob_dict}.. prob_dict is {type(prob_dict)}")
        return InferenceResultDTO(predicted_status=pred, probabilities=prob_dict)