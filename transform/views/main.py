from flask import Request, send_file
from jinja2 import Environment, PackageLoader
from sdx_gcp.app import get_logger
from sdx_gcp.errors import DataException

from transform.transformers.response import SurveyResponseV1, SurveyResponseV2, InvalidDataException
from transform.transformers.survey import MissingSurveyException, MissingIdsException
from transform.transformers.transform_selector import get_transformer

env = Environment(loader=PackageLoader('transform', 'templates'))

logger = get_logger()

VERSION = "version"
V1 = "v1"
V2 = "v2"


def transform(req: Request):

    try:
        response = req.get_json(force=True, silent=True)
        if response is None:
            raise DataException("Response is not in json format")

        version = req.args.get(VERSION, V1)
        if version == V2:
            survey_response = SurveyResponseV2(response)
        else:
            survey_response = SurveyResponseV1(response)

        transformer = get_transformer(survey_response)
        zip_file = transformer.get_zip()
        logger.info("Transformation was a success, returning zip file")
        return send_file(zip_file, mimetype='application/zip', etag=False)

    except MissingSurveyException as me:
        raise DataException(f"Unsupported survey/instrument id: {str(me)}")

    except MissingIdsException as mi:
        raise DataException(str(mi))

    except InvalidDataException as ide:
        raise DataException(str(ide))
