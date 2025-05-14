from fastapi import APIRouter, HTTPException, status
from .model_inference_service import ModelInferenceService
from .model_inference_dto import InferenceInputDTO, InferenceResultDTO

model_inference_router = APIRouter(prefix="/model-inference", tags=["ModelInference"])
service = ModelInferenceService()

@model_inference_router.post("/predict", response_model=InferenceResultDTO, status_code=status.HTTP_200_OK)
async def predict_model(input_dto: InferenceInputDTO):
    """Endpoint to run model inference on provided features"""
    return service.infer(input_dto)
    try:
        print("router")
        print(f"input_dto --> ", input_dto)
        return service.infer(input_dto)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Inference failed")
