from transform.transformers.common_software import MBSTransformer, MWSSTransformer, CSTransformer
from transform.transformers.common_software.abs.abs_transformer import ABSTransformer
from transform.transformers.cora import UKISTransformer
from transform.transformers.cora.mes_transformer import MESTransformer
from transform.transformers.cord import EcommerceTransformer
from transform.transformers.cord.des.des_transformer import DESTransformer
from transform.transformers.survey import MissingIdsException
from transform.transformers.no_pck.qfi_transformer import QFITransformer
from transform.transformers.survey_transformer import SurveyTransformer


def get_transformer(response, sequence_no=1000):
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
        transformer = UKISTransformer(response, sequence_no)
    elif survey_id == "092":
        transformer = MESTransformer(response, sequence_no)

    # CORD
    elif survey_id == "187":
        if response['collection']['instrument_id'] in ['0001', '0002']:
            transformer = DESTransformer(response, sequence_no)
        else:
            transformer = EcommerceTransformer(response, sequence_no)

    # NO PCK INQUIRIES
    elif survey_id == "024":
        transformer = QFITransformer(response, sequence_no)
    elif survey_id == "007":
        # Low Carbon
        transformer = SurveyTransformer(response, sequence_no)
    elif survey_id == "147":
        # EPE
        transformer = SurveyTransformer(response, sequence_no)

    # COMMON SOFTWARE
    elif survey_id == "009":
        transformer = MBSTransformer(response, sequence_no)
    elif survey_id == "134":
        transformer = MWSSTransformer(response, sequence_no)
    elif survey_id == "202":
        transformer = ABSTransformer(response, sequence_no)
    else:
        transformer = CSTransformer(response, sequence_no)

    return transformer
