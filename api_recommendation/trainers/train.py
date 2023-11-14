import json
import os

import numpy as np

from trainers.evaluation import recall_at_k, precision_at_k, ndcg_at_k, f1_score_at_k


class BaseModel:
    _model = None
    _vocab_count = None
    _endpoints = []
    _test = None
    _train = None
    _validation = None

    def __init__(self, endpoints, pretrained=True):
        self._endpoints = endpoints
        self._load_model(pretrained)
        if pretrained:
            self._load_api_bows()

    def _load_model(self, pretrained):
        pass

    def _load_api_bows(self):
        for endpoint in self._endpoints:
            endpoint.bow = [word for word in endpoint.bow if word in self._model.key_to_index]

    def train_test_split(self, queries_file_path, target_file_path, test_percentage=0.2, random_state=10,
                         save_test=True):
        random_state = np.random.RandomState(random_state)
        keys = [endpoint.id for endpoint in self._endpoints]
        random_state.shuffle(keys)
        train_keys = keys[:int(len(keys) * (1 - test_percentage))]
        test_keys = keys[-int(len(keys) * test_percentage):]
        train_apis_bows = dict()
        test_apis_bows = dict()
        train = []
        for key in train_keys:
            value = [endpoint for endpoint in self._endpoints if endpoint.id == key][0]
            train_apis_bows.update({key: value.endpoint})
            train.append(value.endpoint)
        if save_test:
            for key in test_keys:
                value = [endpoint for endpoint in self._endpoints if endpoint.id == key][0]
                api = value.endpoint
                test_apis_bows[api] = value.bow
            if not os.path.exists(f"{target_file_path}/test.json"):
                with open(f"{target_file_path}/test.json", "w") as fp:
                    json.dump(test_apis_bows, fp)
        with open(queries_file_path, "r") as file:
            validation = json.load(file)
        return train, test_apis_bows, validation

    def get_predictions(self, query, k):
        query_bow = list([x for x in query.split() if x in self._model.key_to_index])
        predictions = []
        for endpoint in self._endpoints:
            if len(endpoint.bow) > 0:
                predictions.append((endpoint, self._model.n_similarity(query_bow, endpoint.bow)))
            else:
                predictions.append((endpoint, 0))
        return [api[0] for api in sorted(predictions, key=lambda item: -item[1])[0:k]]

    def evaluate(self, queries_file_path):
        with open(queries_file_path, "r") as file:
            validation = json.load(file)
        scores = {"recall": 0, "precision": 0, "ndcg": 0, "f1": 0}
        for item in validation:
            query_item = item["query"]
            ground_truth = item["results"]
            try:
                recommendations = self.get_predictions(query_item, 10)
            except KeyError:
                pass
            else:
                print(query_item)
                print(recommendations)
                scores["recall"] += recall_at_k(10, ground_truth, recommendations)[-1]
                scores["precision"] += precision_at_k(10, ground_truth, recommendations)[-1]
                scores["ndcg"] += ndcg_at_k(10, ground_truth, recommendations)[-1]
                scores["f1"] += f1_score_at_k(precision_at_k(10, ground_truth, recommendations),
                                              recall_at_k(10, ground_truth, recommendations))[-1]
        scores["recall"] /= len(validation)
        scores["precision"] /= len(validation)
        scores["ndcg"] /= len(validation)
        scores["f1"] /= len(validation)
        print(scores)
