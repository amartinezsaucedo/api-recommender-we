from gensim.models.fasttext import load_facebook_vectors

from trainers.train import BaseModel

EMBEDDING_FILE = "api_recommendation/data/weights/fast_text/crawl-300d-2M-subword.bin"


class FastTextModel(BaseModel):
    def _load_model(self, pretrained):
        if pretrained:
            self._model = load_facebook_vectors(EMBEDDING_FILE)
            self._model.init_sims(replace=True)

    def __repr__(self):
        return f"FastText {EMBEDDING_FILE.split('/')[-1]}"

    def __str__(self):
        return f"FastText {EMBEDDING_FILE.split('/')[-1]}"
