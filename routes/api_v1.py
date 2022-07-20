import fastapi
from modules.logger import logger
from models.csv_models import *
from modules.csv_ops import download_csv, get_name
from fastapi.responses import JSONResponse


route_v1 = fastapi.APIRouter(prefix='/v1', 
        tags=['csv'], 
        responses={404: {'description': 'Not found'}})


@route_v1.post('/download', response_model=CSVModelResponse, 
               status_code=fastapi.status.HTTP_201_CREATED,
               responses={400: {'model': ErrorResponse},
                          409: {'model': ErrorResponse}, 
                          404: {'model': ErrorResponse}
                          } 
               )
async def get_csv(csv_download: CSVModel) -> CSVModelResponse:
    """
    Download the CSV from a specific URL.
    Args:
        csv_download (CSVModel):
            URL: URL where the CSV file is located
            topic: The topic of the CSV.
    
    Returns:
        CSVModelResponse: DESCRIPTION
    """
    try:
        res = download_csv(csv_download.url)
    except ValueError as err:
        if 'The url' in err:
            return JSONResponse(status_code=400, content=jsonable_encoder(ErrorResponse(
                        status=409, 
                        message=f'{err}')))
    if res.status_code == 200:
        store_file(res.text)


@route_v1.get('/files/{topic}')
async def get_files(topic: str) -> str:
    """
    Get files based on topic
    Args:
        topic (str):
            DESCRIPTION
    
    Returns:
        str: DESCRIPTION
    """
    pass
