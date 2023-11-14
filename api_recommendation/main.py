import argparse

from models.endpoint import Endpoint
from tasks import AVAILABLE_TASKS
from tasks.evaluate import evaluate_algorithms
from tasks.extract import extract_oapi_data
from tasks.transform import transform_oapi_data
from tasks.utils import load_from_file

parser = argparse.ArgumentParser("API recommender based on Word Embeddings")
parser.add_argument("-q", "--queries_path", help="Path of file storing test queries and recommended APIs (ground truth)", type=str, required=False, default="api_recommendation/data/test/queries.json")
parser.add_argument("-e", "--test_endpoints_path", help="Path of file storing test endpoints to use for test queries recommendation", type=str, required=False, default="api_recommendation/data/test/test_endpoints.json")
parser.add_argument("-c", "--commit_hash", help="APIs.guru repository commit to download APIs from", type=str, required=False, default="fb28391")
parser.add_argument("-t", "--task", help="Task to execute", choices=AVAILABLE_TASKS.keys(), type=str, required=True)
args = parser.parse_args()

task = args.task

if task == "evaluate":
    queries_path = args.queries_path
    test_endpoints_path = args.test_endpoints_path
    test_endpoints = load_from_file(test_endpoints_path, lambda x: Endpoint(**x))
    evaluate_algorithms(test_endpoints, queries_path)
elif task == "extract":
    commit_hash = args.commit_hash
    extract_oapi_data(commit_hash)
elif task == "transform":
    commit_hash = args.commit_hash
    endpoints = extract_oapi_data(commit_hash)
    endpoints = transform_oapi_data(endpoints)
