# API recommendation based on Word Embeddings

## Install required dependencies and download files
```sh 
make install
```

## Run tasks
### API extraction
Specify APIs.guru repository commit hash to download APIs (default is master)
```sh 
make run_extraction COMMIT_HASH={commit_hash}
```

### API transformation
Specify APIs.guru repository commit hash to download APIs (default is master) and then transform description
```sh 
make run_transformation COMMIT_HASH={commit_hash}
```

### Recommender evaluation
Specify test queries and test endpoints files paths (default paths are referencing default experiment)
```sh 
make run_evaluation QUERIES_PATH={queries_path} -e TEST_ENDPOINTS_PATH={test_endpoints_path}
```