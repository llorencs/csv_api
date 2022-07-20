
import requests
from requests import Response
import re


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
    reg_expr = r'?i(http(s)?):\S*/(?P<name>\S+?\.csv)'
    pat = re.compile(reg_expr)
    res = pat.match(reg_expr)
    if res:
        return res.get('name')


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
