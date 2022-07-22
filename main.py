from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routes.api_v1 import route_v1
from modules.logger import logger


logger.debug('Start of the run')

app = FastAPI(title='CSVTools',
                description='CSV upload/download tools.', 
                version='v1'
                )

app.mount('/api/v1', route_v1)


origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8001, debug=True, workers=5)
