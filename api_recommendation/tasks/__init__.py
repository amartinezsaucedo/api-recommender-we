from .evaluate import evaluate_algorithms
from .extract import extract_oapi_data
from .transform import transform_oapi_data

AVAILABLE_TASKS = {
    "evaluate": evaluate_algorithms,
    "extract": extract_oapi_data,
    "transform": transform_oapi_data
}
