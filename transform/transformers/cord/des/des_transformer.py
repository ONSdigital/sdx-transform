import decimal
from decimal import Decimal, ROUND_HALF_UP

import structlog

from transform.transformers.cord.cord_formatter import CORDFormatter
from transform.transformers.cord.des.des_transforms import transformations
from transform.transformers.survey_transformer import SurveyTransformer

logger = structlog.get_logger()


def round_and_divide_by_one_thousand(value):
    """Rounding is done on a ROUND_HALF_UP basis and values are divided by 1000 for the pck"""
    try:
        # Set the rounding context for Decimal objects to ROUND_HALF_UP
        decimal.getcontext().rounding = ROUND_HALF_UP
        return Decimal(round(Decimal(float(value))) / 1000).quantize(1)

    except TypeError:
        logger.info("Tried to quantize a NoneType object. Returning an empty string")
        return ''


def checkbox(value, ticked, unticked):
    if value is None or value == "":
        return unticked
    return ticked


def radio_button(value, mapping: dict):
    if value is None or value == "":
        return None
    for k, v in mapping.items():
        if k.startswith(value):
            return v
    return None


class DESTransformer(SurveyTransformer):
    """Perform the transforms and formatting for the DES survey."""

    def __init__(self, response, seq_nr=0):
        super().__init__(response, seq_nr)
        period = response['collection']['period']
        if len(period) == 4:
            response['collection']['period'] = period[2:] + '12'

        self.period = period

    def _get_value(self, q_code):
        input_dict = self.response['data']
        if q_code in input_dict:
            value = input_dict.get(q_code)
            return value if value != '' else None
        else:
            return None

    def transform(self):
        result = {}

        for q_code, transformation in transformations.items():

            value = self._get_value(q_code)

            if transformation == 'value':
                transformed_value = value
            elif transformation == 'thousands':
                transformed_value = round_and_divide_by_one_thousand(value)
            elif transformation == 'value':
                transformed_value = value
            elif transformation == 'comment':
                transformed_value = 1 if value != "" else 2

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
