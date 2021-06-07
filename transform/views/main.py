import json
import threading
import structlog

from jinja2 import Environment, PackageLoader
from structlog.contextvars import bind_contextvars
from fastapi import HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from transform import app
from transform.transformers.survey import MissingSurveyException, MissingIdsException
from transform.transformers.transform_selector import get_transformer
from pydantic import BaseModel

env = Environment(loader=PackageLoader('transform', 'templates'))

logger = structlog.get_logger()


class Survey(BaseModel):
    json_survey: str


@app.post('/transform')
async def transform(survey: Survey):
    survey_response = survey.json_survey
    survey_dict = json.loads(survey_response)
    tx_id = survey_dict.get("tx_id")
    bind_contextvars(app="sdx-transform")
    bind_contextvars(tx_id=tx_id)
    bind_contextvars(thread=threading.currentThread().getName())

    try:
        transformer = get_transformer(survey_dict)
        zip_file = transformer.get_zip()
        logger.info("Transformation was a success, returning zip file")
        # return send_file(zip_file, mimetype='application/zip', etag=False)
        response = FileResponse(zip_file, media_type='application/zip')
        return response

    except MissingIdsException as e:
        return HTTPException(status_code=400, detail=str(e))

    except MissingSurveyException:
        return HTTPException(status_code=400, detail="Unsupported survey/instrument id")

    except Exception as e:
        survey_id = survey_dict.get("survey_id")
        logger.exception("TRANSFORM:could not create files for survey", survey_id=survey_id, tx_id=tx_id)
        return HTTPException(status_code=500, detail=str(e))


@app.get('/info')
@app.get('/healthcheck')
async def healthcheck():
    """A simple endpoint that reports the health of the application"""
    return {'status': 'OK'}
