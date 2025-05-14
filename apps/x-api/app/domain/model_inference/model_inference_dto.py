from .model_inference_entity import InferenceInputEntity, InferenceResultEntity

class InferenceInputDTO(InferenceInputEntity):
    """Request DTO for model inference"""
    pass

class InferenceResultDTO(InferenceResultEntity):
    """Response DTO for model inference"""
    pass