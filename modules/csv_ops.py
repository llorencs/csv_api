
import requests
from requests import Response
import re
from db.mongo_client import *
from .logger import logger
from pathlib import Path


def download_csv(url: str) -> Response:
    """
    Download the CSV file from an url.
    Args:
        url (str):
            Url to download the tool.
    
    Returns:
        Response: DESCRIPTION
    """
    if isinstance(url, str):
        url=r'https://vincentarelbundock.github.io/Rdatasets/csv/AER/Affairs.csv'
        if url.startswith('http') or url.startswith('https') and url.lower().endswith('.csv'):
            res = requests.get(url)
            return res
        else:
            raise ValueError(f'The url {url} is not valid as does not contain HTTP/HTTPS values.'
                             'And or is not a valid CSV file.')


def get_name(url: str) -> str:
    """
    Check if an url is valid or not
    Args:
        url (str):
            DESCRIPTION
    
    Returns:
        bool: DESCRIPTION
    """
    reg_expr = r'(?i)(http(s)?):\S*/(?P<name>\S+?\.csv)'
    pat = re.compile(reg_expr)
    res = pat.search(url)
    if res:
        return res.group('name')


def read_header(document: str) -> list[str]:
    """
    Get the header of the CSV file.
    Args:
        document (str):
            The CSV as text file.
    
    Returns:
        list[str]: List of the values of the header
    """
    lines = document.split('\n')
    return lines[0].replace('"', '').split(',')


async def store_file(document: str, url: str, topic: str) -> dict:
    """
    Store the file in the file system and database
    
    @param document The contents of the file to be stored
    @type str
    @param url The url of the file to be stored in the database
    @type str
    """
    res = await insert({'url':  url, 'topic': topic,
                    'header': read_header(document),
                    'name': get_name(url)},
                                 'csvfiles')
    logger.debug(f'New item: {res.inserted_id}, Acknowledged: {res.acknowledged}')
    folder = Path(f'files/{res.inserted_id}')
    name = get_name(url)
    folder.mkdir(parents=True, exist_ok=True)
    logger.debug(f'URL: {url} and name: {name}')
    with Path(folder, name).open('w', encoding='utf-8') as fhandle:
        fhandle.write(document)
    return await get_document(res.inserted_id, 'csvfiles')


if __name__ == '__main__':
    res= insert({'url': 'https://datagrams/open.csv', 'topic': 'testing'}, 'csvfiles')
    print(res)
    
