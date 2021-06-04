from transform.transformers.common_software import MBSTransformer, MWSSTransformer, CSTransformer
from transform.transformers.common_software.epe_transformer import EPETransformer
from transform.transformers.common_software.low_carbon_transformer import LCTransformer
from transform.transformers.cora import UKISTransformer
from transform.transformers.cora.mes_transformer import MESTransformer
from transform.transformers.cord import Ecommerce2019Transformer, EcommerceTransformer
from transform.transformers.survey import MissingIdsException


def get_transformer(response):
    """Returns the appropriate survey transformer based on survey_id

    :param dict response: A dictionary like object representing the survey response
    :param int sequence_no: A number used by the transformer for naming files
    :raises MissingIdsException if no survey_id
    """

    if 'survey_id' not in response:
        raise MissingIdsException("Missing field survey_id from response")

    survey_id = response['survey_id']

    # CORA
    if survey_id == "144":
        transformer = UKISTransformer(response)
    elif survey_id == "092":
        transformer = MESTransformer(response)

    # CORD
    elif survey_id == "187":
        if response['collection']['instrument_id'] in ['0001', '0002']:
            transformer = Ecommerce2019Transformer(response)
        else:
            transformer = EcommerceTransformer(response)

    # COMMON SOFTWARE
    elif survey_id == "007":
        transformer = LCTransformer(response)
    elif survey_id == "009":
        transformer = MBSTransformer(response)
    elif survey_id == "134":
        transformer = MWSSTransformer(response)
    elif survey_id == "147":
        transformer = EPETransformer(response)
    else:
        transformer = CSTransformer(response)

    return transformer
