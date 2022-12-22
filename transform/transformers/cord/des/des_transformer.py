from decimal import Decimal, InvalidOperation

import structlog

from transform.transformers.cord.cord_formatter import CORDFormatter
from transform.transformers.cord.des.des_transforms import transformations, Transform
from transform.transformers.survey_transformer import SurveyTransformer

logger = structlog.get_logger()


def thousands(value: str) -> str:
    """
    Transform the value for a currency question into thousands.
    :param value: the value to round
    """
    if not value:
        return ''
    try:
        return str((Decimal(value)) / 1000)

    except InvalidOperation:
        logger.info("Not a numerical value. Returning an empty string")
        return ''


def checkbox(value, ticked, unticked) -> str:
    """
    Transform the value for a checkbox.
    The checkbox is deemed to be ticked if we receive any non None value.

    :param value: the received value
    :param ticked: the return value if ticked
    :param unticked: the return value if not ticked
    """
    if not value:
        return unticked
    return ticked


def radio_button(value, mapping: dict) -> str:
    """
    Transform the value from a radio button.

    :param value: the received value
    :param mapping: a dictionary of return values mapped to
                    the first word of each possible response.
    """
    if not value:
        return ""
    for k, v in mapping.items():
        if value.startswith(k):
            return v
    return ""


def multi_qcode_radio_button(value, qcode_mapping: dict) -> dict:
    """
    Transform the value from a radio button where the answers represent different qcodes downstream.
    The value will be assigned to a single qcode but the alternative answers will not
    be present in the json even though they are required downstream. Therefore this function
    returns a dictionary mapping all the required qcodes to their radio button status. As radio button
    options are mutually exclusive we can assume all but the received value are unticked.

    :param value: the received value
    :param qcode_mapping: a dictionary of mappings from the answer to a
                    dict containing the qcode and values for if it is ticked or unticked
                    e.g. {
                        "qcode": "277",
                        "ticked": "1",
                        "unticked": "0"
                    }
    """
    result = {}
    answered = False
    is_other_and_ticked = False
    yes_no_choices = []

    if value in qcode_mapping:
        answered = True

    for k, v in qcode_mapping.items():
        q_code = v['qcode']

        if 'excluder' not in v:
            yes_no_choices.append(q_code)
        elif value == k:
            is_other_and_ticked = True

        if value == k:
            result[q_code] = v['ticked']
        else:
            if answered:
                result[q_code] = v['unticked']
            else:
                result[q_code] = ''

    if is_other_and_ticked:
        result = {key: '' if key in yes_no_choices else value for key, value in result.items()}

    return result


def comment(value, present, not_present) -> str:
    """
    Transformation to indicate if a comment was present.

    :param value: the received value
    :param present: return value if comment is present
    :param not_present: return value if comment is not present
    """
    if not value:
        return not_present
    else:
        return present


def perform_transform(response_data: dict, transformations_dict: dict) -> dict:
    """
    Returns a dictionary of qcode to transformed answer
    by applying the transforms stipulated in the 'transformations' dictionary
    """
    result = {}

    for q_code, t_list in transformations_dict.items():

        if q_code in response_data:
            value = response_data.get(q_code)
        else:
            value = ''

        transformation = t_list[0]

        if transformation == Transform.MULTI_RADIO:
            transformed_values = multi_qcode_radio_button(value, qcode_mapping=t_list[1])
            for k, v in transformed_values.items():
                result[k] = v

        else:

            if transformation == Transform.THOUSANDS:
                transformed_value = thousands(value)
            elif transformation == Transform.COMMENT:
                transformed_value = comment(value, present=t_list[1], not_present=t_list[2])
            elif transformation == Transform.RADIO:
                transformed_value = radio_button(value, mapping=t_list[1])
            elif transformation == Transform.CHECKBOX:
                transformed_value = checkbox(value, ticked=t_list[1], unticked=t_list[2])
            else:
                transformed_value = value

            result[q_code] = transformed_value

    return result


class DESTransformer(SurveyTransformer):
    """Perform the transforms and formatting for the DES survey.

    The period for DES comes in as YYYY (e.g. 2021).
    This is the required form for pck file, but the ImageTransformer
    and IDBR receipt require YYYY12 (e.g. 202112).
    Therefore, we change the value on the response before passing to the superclass.
    """
    def __init__(self, response, seq_nr=0):
        period = response.period
        response.period = period + '12'
        super().__init__(response, seq_nr)
        self.period = period

    def _create_pck(self, transformed_data):
        """Return a pck file using provided data"""
        pck = CORDFormatter.get_pck(
            transformed_data,
            self.survey_response.survey_id,
            self.survey_response.ru_ref,
            self.period,
        )
        return pck

    def create_pck(self):
        bound_logger = logger.bind(ru_ref=self.survey_response.ru_ref, tx_id=self.survey_response.tx_id)
        bound_logger.info("Transforming data for processing")
        transformed_data = perform_transform(self.survey_response.data, transformations)
        bound_logger.info("Data successfully transformed")

        bound_logger.info("Creating PCK")
        pck_name = CORDFormatter.pck_name(self.survey_response.survey_id, self.survey_response.tx_id)
        pck = self._create_pck(transformed_data)
        bound_logger.info("Successfully created PCK")
        return pck_name, pck
