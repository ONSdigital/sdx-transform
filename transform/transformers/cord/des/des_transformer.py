import decimal
from decimal import Decimal, ROUND_HALF_UP

import structlog

from transform.transformers.cord.cord_formatter import CORDFormatter
from transform.transformers.cord.des.des_transforms import transformations, Transform
from transform.transformers.survey_transformer import SurveyTransformer

logger = structlog.get_logger()


def thousands(value: str) -> str:
    """
    Transform the value for a currency question into thousands.
    Rounding is done on a ROUND_HALF_UP basis.

    :param value:  the value to round
    """
    try:
        decimal.getcontext().rounding = ROUND_HALF_UP
        return str(Decimal(round(Decimal(float(value))) / 1000).quantize(1))

    except TypeError:
        logger.info("Tried to quantize a NoneType object. Returning an empty string")
        return ''


def checkbox(value, ticked, unticked) -> str:
    """
    Transform the value for a checkbox.
    The checkbox is deemed to be ticked if we receive any non None value.

    :param value: the received value
    :param ticked: the return value if ticked
    :param unticked: the return value if not ticked
    """
    if value is None or value == "":
        return unticked
    return ticked


def radio_button(value, mapping: dict) -> str:
    """
    Transform the value from a radio button.

    :param value: the received value
    :param mapping: a dictionary of return values mapped to
                    the first word of each possible response.
    """
    if value is None or value == "":
        return ""
    for k, v in mapping.items():
        if k.startswith(value):
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
    :param mapping: a dictionary of mappings from the answer to a
                    dict containing the qcode and values for if it is ticked or unticked
                    e.g. {
                        "qcode": "277",
                        "ticked": "1",
                        "unticked": "0"
                    }
    """
    result = {}
    for k, v in qcode_mapping.items():
        if value == k:
            result[v['qcode']] = v['ticked']
        else:
            result[v['qcode']] = v['unticked']
    return result


def comment(value, present, not_present) -> str:
    """
    Transformation to indicate if a comment was present.

    :param value: the received value
    :param present: return value if comment is present
    :param not_present: return value if comment is not present
    """
    if value is None or value == "":
        return not_present
    else:
        return present


class DESTransformer(SurveyTransformer):
    """Perform the transforms and formatting for the DES survey.

    The period for Ecommerce is different to other surveys and comes in as YYYY (e.g. 2019).
    This is the required form for pck file.
    However, the ImageTransformer and IDBR receipt formatter will prefix it with a 20, to make 202019.
    The required value for both is actually YYYY12 (e.g. 201912) where the 12 represents the month.
    To adjust for this the period is changed to YYMM before further processing takes place and the initial
    YYYY period used only for creating the pck
    """
    def __init__(self, response, seq_nr=0):
        super().__init__(response, seq_nr)
        period = response['collection']['period']
        if len(period) == 4:
            response['collection']['period'] = period[2:] + '12'

        self.period = period

    def _get_value(self, q_code):
        """Extract the corresponding response from the data for the qcode given"""
        input_dict = self.response['data']
        if q_code in input_dict:
            value = input_dict.get(q_code)
            return value if value != '' else None
        else:
            return None

    def transform(self) -> dict:
        """
        Returns a dictionary of qcode to transformed answer
        by applying the transforms stipulated in the 'transformations' dictionary
        """
        result = {}

        for q_code, t_list in transformations.items():

            value = self._get_value(q_code)
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

    def _create_pck(self, transformed_data):
        """Return a pck file using provided data"""
        pck = CORDFormatter.get_pck(
            transformed_data,
            self.ids.survey_id,
            self.ids.ru_ref,
            self.period,
        )
        return pck

    def create_pck(self):
        bound_logger = logger.bind(ru_ref=self.ids.ru_ref, tx_id=self.ids.tx_id)
        bound_logger.info("Transforming data for processing")
        transformed_data = self.transform()
        bound_logger.info("Data successfully transformed")

        bound_logger.info("Creating PCK")
        pck_name = CORDFormatter.pck_name(self.ids.survey_id, self.ids.tx_id)
        pck = self._create_pck(transformed_data)
        bound_logger.info("Successfully created PCK")
        return pck_name, pck
