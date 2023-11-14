import os
import requests
import re
from pathlib import Path
import zipfile
from ruamel.yaml import YAML

from models.endpoint import Endpoint
from models.metadata import Metadata
from tasks.utils import save_to_file, load_from_file

yaml = YAML()

GITHUB_REPO_URL = 'https://api.github.com/repos/APIs-guru/openapi-directory/{action}/{ref}'
APIS_SOURCE_FOLDER_NAME = 'APIs/'
APIS_TARGET_FOLDER_NAME = 'api_recommendation/data/APIs/'
DATASET_COMMIT_FILENAME = 'api_recommendation/data/dataset_info.json'
DATA_FILENAME = 'api_recommendation/data/endpoints.json'


def extract_oapi_data(github_ref='main', **kwargs):
    data_file_exists = os.path.isfile(DATA_FILENAME)
    api_folder_exists = os.path.isdir(APIS_TARGET_FOLDER_NAME)
    if data_file_exists:
        data_list = load_from_file(DATA_FILENAME, lambda x: Endpoint(**x))
    else:
        if not api_folder_exists:
            download_raw_data(github_ref)
            print('Dataset downloaded')
        print('Processing APIs')
        data_list = generate_list(APIS_TARGET_FOLDER_NAME)
        save_to_file([o.__dict__ for o in data_list], DATA_FILENAME)
    print('APIs loaded')
    print('Number of endpoints: ' + str(len(data_list)))
    return data_list


def download_raw_data(github_ref):
    response = requests.get(GITHUB_REPO_URL.format(action='zipball', ref=github_ref))
    if response.ok:
        filename = get_repo_zip_filename(response.headers)
        commit = get_commit(github_ref)
        target_folder_filename = create_target_folder(APIS_TARGET_FOLDER_NAME)
        print('Downloading dataset')
        download_zip(filename, response.content)
        print('Unzipping repository')
        unzip_api_folder(filename, target_folder_filename)
        delete_downloaded_zip(filename)
        save_dataset_commit(commit)
    else:
        print('An error occurred when attempting to download Open API documentation')


def get_repo_zip_filename(headers):
    filename = re.findall('filename=(.+)', headers['content-disposition'])[0]
    return os.path.join(os.getcwd(), filename)


def get_commit(ref):
    if ref != 'main':
        return ref
    response = requests.get(GITHUB_REPO_URL.format(action='commits', ref=ref))
    if response.ok:
        return response.json()['sha']


def create_target_folder(target_folder_name):
    target_folder_filename = os.path.join(os.getcwd(), target_folder_name)
    Path(target_folder_filename).mkdir(parents=True, exist_ok=True)
    return target_folder_filename


def download_zip(filename, content):
    with open(filename, 'wb') as file:
        file.write(content)


def unzip_api_folder(filename, target_folder_filename):
    with zipfile.ZipFile(filename) as archive:
        for file_info in archive.infolist():
            is_file = file_info.filename[-1] != '/'
            if APIS_SOURCE_FOLDER_NAME in file_info.filename and is_file:
                file_info.filename = remove_parent_directory(file_info.filename)
                archive.extract(file_info, target_folder_filename)


def remove_parent_directory(filename):
    return ''.join(filename.split('/', 2)[2:])


def delete_downloaded_zip(filename):
    if os.path.isfile(filename):
        os.remove(filename)


def save_dataset_commit(commit):
    metadata = Metadata()
    metadata.dataset_info = commit
    save_to_file(metadata.__dict__, DATASET_COMMIT_FILENAME)


def generate_list(dataset_location):
    apis = []
    accepted_meth = ['post', 'get', 'put', 'patch', 'delete']
    for absolute_base, _, files in os.walk(dataset_location):
        for f in files:
            if f in ['swagger.yaml', 'openapi.yaml']:
                base = absolute_base.replace(APIS_TARGET_FOLDER_NAME, '')
                try:
                    with open(os.path.join(absolute_base, f), encoding='utf8') as yaml_file:
                        data = yaml.load(yaml_file)
                    print((base + '/' + f))
                    for api in data['paths'].keys():
                        for methodHTTP in data['paths'][api].keys():
                            if methodHTTP.lower() in accepted_meth:
                                if 'description' in list(data['paths'][api][methodHTTP].keys()):
                                    apis.append(Endpoint(endpoint=f"{base}{api}/{methodHTTP}",
                                                         description=data['paths'][api][methodHTTP]['description']))
                except Exception as e:
                    print(f"Not processed: {base}/{f}. Error: {str(e)}")
                    pass
    return apis
