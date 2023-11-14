import collections

from gensim.models import KeyedVectors, Word2Vec

from trainers.train import BaseModel

EMBEDDING_FILE = "api_recommendation/data/weights/word2vec/SO_vectors_200.bin"


class Word2VecModel(BaseModel):
    def _load_model(self, pretrained):
        if pretrained:
            self._model = KeyedVectors.load_word2vec_format(EMBEDDING_FILE, binary=True)
            self._model.init_sims(replace=True)
        else:
            data = [endpoint.bow for endpoint in self._endpoints]
            self._model = Word2Vec(window=10, sg=1, hs=0,
                                   negative=10,  # for negative sampling
                                   alpha=0.03, min_alpha=0.0007,
                                   seed=14, vector_size=300)
            self._model.build_vocab(data, progress_per=200)
            self._model.train(data, total_examples=self._model.corpus_count, epochs=20)
            words = [item for list_words in data for item in list_words]
            self._vocab_count = collections.Counter(words)

    def __repr__(self):
        return f"Word2Vec {EMBEDDING_FILE.split('/')[-1]}"

    def __str__(self):
        return f"Word2Vec {EMBEDDING_FILE.split('/')[-1]}"

