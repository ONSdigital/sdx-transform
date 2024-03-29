from transform.transformers.common_software import MWSSTransformer, CSTransformer
from transform.transformers.common_software.abs.abs_transformer import ABSTransformer
from transform.transformers.common_software.acas.acas_transformer import ACASTransformer
from transform.transformers.common_software.blocks.blocks_transformer import BlocksTransformer
from transform.transformers.common_software.bricks.bricks_transformer import BricksTransformer
from transform.transformers.common_software.sand_and_gravel.land_won_transformer import LandTransformer
from transform.transformers.common_software.sand_and_gravel.marine_dredged_transformer import MarineTransformer
from transform.transformers.cora.mes_transformer import MESTransformer
from transform.transformers.cord import EcommerceTransformer
from transform.transformers.cord.des.des2021_transformer import DES2021Transformer
from transform.transformers.cord.des.des_transformer import DESTransformer
from transform.transformers.no_pck.ari_transformer import ARITransformer
from transform.transformers.response import SurveyResponse
from transform.transformers.no_pck.qfi_transformer import QFITransformer
from transform.transformers.spp.berd.berd_transformer import BERDTransformer
from transform.transformers.survey_transformer import SurveyTransformer, DelegatedImageTransformer


def get_transformer(response: SurveyResponse, sequence_no=1000):
    """Returns the appropriate survey transformer based on survey_id

    :param dict response: A dictionary like object representing the survey response
    :param int sequence_no: A number used by the transformer for naming files
    :raises MissingIdsException if no survey_id
    """

    survey_id = response.survey_id

    # SPP
    if survey_id == "002":
        transformer = BERDTransformer(response, sequence_no)

    # CORA
    elif survey_id == "144":
        transformer = DelegatedImageTransformer(response)
    elif survey_id == "092":
        transformer = MESTransformer(response, sequence_no)

    # CORD
    elif survey_id == "187":
        if response.instrument_id in ['0001', '0002']:
            if response.period == "2021":
                transformer = DES2021Transformer(response, sequence_no)
            else:
                transformer = DESTransformer(response, sequence_no)
        else:
            transformer = EcommerceTransformer(response, sequence_no)
    elif survey_id == "127":
        transformer = DelegatedImageTransformer(response)

    # NO PCK INQUIRIES
    elif survey_id == "007":
        # Low Carbon
        transformer = SurveyTransformer(response, sequence_no)
    elif survey_id == "023":
        # Retail Sales Inquiry (RSI)
        transformer = SurveyTransformer(response, sequence_no)
    elif survey_id == "024":
        # Fuels
        transformer = QFITransformer(response, sequence_no)
    elif survey_id == "147":
        # EPE
        transformer = SurveyTransformer(response, sequence_no)
    elif survey_id == "194":
        # Railways
        transformer = ARITransformer(response, sequence_no)

    # COMMON SOFTWARE
    elif survey_id == "009":
        transformer = DelegatedImageTransformer(response)
    elif survey_id == "134":
        transformer = MWSSTransformer(response, sequence_no)
    elif survey_id == "171":
        transformer = ACASTransformer(response, sequence_no)
    elif survey_id == "202":
        transformer = ABSTransformer(response)
    elif survey_id == "073":
        transformer = BlocksTransformer(response, sequence_no)
    elif survey_id == "074":
        transformer = BricksTransformer(response, sequence_no)
    elif survey_id == "066":
        transformer = LandTransformer(response, sequence_no)
    elif survey_id == "076":
        transformer = MarineTransformer(response, sequence_no)
    else:
        transformer = CSTransformer(response, sequence_no)

    return transformer
