import threading

import structlog
from flask import request, send_file, jsonify
from jinja2 import Environment, PackageLoader
from structlog.contextvars import bind_contextvars

from transform import app
from transform.transformers.image_requester import ImageServiceError
from transform.transformers.response import SurveyResponseV1, SurveyResponseV2, InvalidDataException
from transform.transformers.survey import MissingSurveyException, MissingIdsException
from transform.transformers.transform_selector import get_transformer

env = Environment(loader=PackageLoader('transform', 'templates'))

logger = structlog.get_logger()

VERSION = "version"
V1 = "v1"
V2 = "v2"


@app.errorhandler(400)
def errorhandler_400(e):
    return client_error(repr(e))


def client_error(error=None):
    logger.error("Client error", error=error)
    message = {
        'status': 400,
        'message': error,
        'uri': request.url,
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp


@app.errorhandler(500)
def server_error(error=None):
    logger.error("Server error", error=str(error))
    message = {
        'status': 500,
        'message': "Internal server error: " + str(error),
    }
    resp = jsonify(message)
    resp.status_code = 500

    return resp


@app.post('/transform')
@app.post('/transform/<sequence_no>')
def transform(sequence_no=1000):
    response = request.get_json(force=True)
    tx_id = response.get("tx_id")
    bind_contextvars(app="sdx-transform")
    bind_contextvars(tx_id=tx_id)
    bind_contextvars(thread=threading.currentThread().getName())

    if sequence_no:
        sequence_no = int(sequence_no)

    try:
        version = request.args.get(VERSION, V1)
        if version == V2:
            survey_response = SurveyResponseV2(response)
        else:
            survey_response = SurveyResponseV1(response)

        transformer = get_transformer(survey_response, sequence_no)
        zip_file = transformer.get_zip()
        logger.info("Transformation was a success, returning zip file")
        return send_file(zip_file, mimetype='application/zip', etag=False)

    except MissingIdsException as e:
        return client_error(str(e))

    except MissingSurveyException:
        return client_error("Unsupported survey/instrument id")

    except InvalidDataException as ide:
        return client_error(str(ide))

    except ImageServiceError as ise:
        return server_error(ise)

    except Exception as e:
        logger.exception("TRANSFORM:could not create files for survey", tx_id=tx_id)
        return server_error(e)


@app.get('/info')
@app.get('/healthcheck')
def healthcheck():
    """A simple endpoint that reports the health of the application"""
    return jsonify({'status': 'OK'})
