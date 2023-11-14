COMMIT_HASH="fb28391"
QUERIES_PATH="api_recommendation/data/test/queries.json"
TEST_ENDPOINTS_PATH="api_recommendation/data/test/test_endpoints.json"


install: install_requirements download_weights

install_requirements:
	poetry install

download_weights:
	cd api_recommendation/data/weights/word2vec && curl -k -o SO_vectors_200.bin -L https://zenodo.org/records/1199620/files/SO_vectors_200.bin?download=1
	cd api_recommendation/data/weights/fast_text && curl -k -LO https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M-subword.zip && unzip crawl-300d-2M-subword.zip && rm crawl-300d-2M-subword.zip && rm crawl-300d-2M-subword.vec

run_extraction:
	poetry run python api_recommendation/main.py -t extract -c $(COMMIT_HASH)

run_transformation:
	poetry run python api_recommendation/main.py -t transform -c $(COMMIT_HASH)

run_evaluation:
	poetry run python api_recommendation/main.py -t evaluate -q $(QUERIES_PATH) -e $(TEST_ENDPOINTS_PATH)