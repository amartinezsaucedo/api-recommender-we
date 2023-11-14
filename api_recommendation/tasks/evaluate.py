from models.endpoint import Endpoint
from trainers.train_word2vec import Word2VecModel
from trainers.train_fasttext import FastTextModel


def evaluate_algorithms(endpoints: list[Endpoint], test_queries_path: str, **kwargs):
    available_algorithms = [Word2VecModel, FastTextModel]
    for algorithm in available_algorithms:
        print(str(algorithm))
        instance = algorithm(endpoints)
        instance.evaluate(test_queries_path)
