import fastapi
from modules.logger import logger
from models.csv_models import *
from modules.csv_ops import download_csv, get_name, store_file
from fastapi.responses import JSONResponse
from db.mongo_client import *
from fastapi.encoders import jsonable_encoder


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
                        status_code=400, 
                        message=f'{err}')))
    if res.status_code == 200:
        file_stored = await store_file(res.text, csv_download.url, csv_download.topic)
        logger.debug(file_stored)
        return CSVModelResponse(id = str(file_stored.get('_id')), 
                                url=file_stored.get('url'), 
                                topic=file_stored.get('topic')
                                )


@route_v1.get('/files/{topic}')
async def get_files(topic: str) -> list[CSVModelResponse]:
    """
    Get files based on topic
    
    *topic**: The topic of the files to get.
    """
    pass


@route_v1.post('/header', response_model=HeaderModelResponse, 
               status_code=fastapi.status.HTTP_200_OK,
               responses={400: {'model': ErrorResponse}, 
                          404: {'model': ErrorResponse}})
async def get_header(h: HeaderModel) -> HeaderModelResponse:
    """
    Get the header of a file given its id or name
    
    **id (Optional)**: ID of the csv to display its header
    **name (Optional)**: Name of the CSV file to get its header.
    One of the values is required.
    Responses:
    200: Return the Header if is valid
    400: If the request is bad, for example missing ID and name, or given both.
    """
    if not h.name and not h.id:
        return JSONResponse(status_code=400, content=jsonable_encoder(ErrorResponse(
                        status_code=400, 
                        message='Missing id or name of the CSV to get its header.')))
    elif h.name and h.id:
        return JSONResponse(status_code=400, content=jsonable_encoder(ErrorResponse(
                        status_code=400, 
                        message='Has been provided an id and a name. Only one is valid.')))
    elif h.name:
        doc = await  find_document('name', h.name, 'csvfiles')
    elif h.id:
        doc = await get_document(h.id, 'csvfiles')
    logger.debug(f'Doc: {doc} id: {h.id} name: {h.name}')
    if doc:
        return HeaderModelResponse(id= doc.get('_id'), 
                                   header=doc.get('header'))
    else:
        return JSONResponse(status_code=404, content=jsonable_encoder(ErrorResponse(
                        status_code=404, 
                        message='The document with the given ID or name has not been found.')))
