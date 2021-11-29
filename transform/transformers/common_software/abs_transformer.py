import decimal
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

import structlog

from transform.transformers.common_software.cs_formatter import CSFormatter
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


def combine_sum(values: list):
    total = 0
    for v in values:
        total += float(v)
    return total


def convert_period_data(value):
    derived_date = datetime.strptime(value, "%d/%m/%Y")
    return derived_date.strftime("%d%m%y")


# This dict defines how the transformation is done.  The key is the qcode, the value describes what transformation
# needs to be done on the value.  A dict for the value generally describes what to do with a radio button input and a
# string describes all other inputs.
transforms = {
    '11': 'period_data',
    '12': 'period_data',
    '399': 'nearest_thousand',
    '80': {'Yes': '10', 'No': '1', None: '0'},
    '81': {'0-9%': '10000', '10-24%': '1000', '25-49%': '100', '50-74%': '0100', '75-100%': '1', None: '0'},
    '450': 'nearest_thousand',
    '403': 'nearest_thousand',
    '420': 'nearest_thousand',
    '400': 'nearest_thousand',
    '500': 'nearest_thousand',
    '599': 'nearest_thousand',
    '600': 'nearest_thousand',
    '699': 'nearest_thousand',
    '163': 'nearest_thousand',
    '164': 'nearest_thousand',
    '15': {'Yes': '10', 'No': '1', None: '0'},
    '16': {'Yes': '10', 'No': '1', None: '0'},
    '9': {'Yes': '10', 'No': '1', None: '0'},
    '146': 'comment',
    '499': ['sum', '403', '420']
}


class ABSTransformer(SurveyTransformer):
    """Perform the transforms and formatting for the ABS survey."""

    def __init__(self, response, seq_nr=0):
        super().__init__(response, seq_nr)

    def _get_value(self, q_code):
        input_dict = self.response['data']
        if q_code in input_dict:
            value = input_dict.get(q_code)
            return value if value != '' else None
        else:
            return None

    def transform(self):
        result = {}

        for q_code, transformation in transforms.items():

            value = self._get_value(q_code)
            transformed_value = value

            if value is None:
                if type(transformation) == dict:
                    transformed_value = transformation.get(value)
                else:
                    continue

            if type(transformation) == dict:
                transformed_value = transformation.get(value)
            elif type(transformation) == list:
                if transformation[0] == 'sum':
                    inputs = []
                    for q in transformation[1:]:
                        inputs.append(self._get_value(q))
                    transformed_value = combine_sum(inputs)
            elif transformation == 'nearest_thousand':
                transformed_value = round_and_divide_by_one_thousand(value)
            elif transformation == 'period_data':
                transformed_value = convert_period_data(value)
            elif transformation == 'comment':
                transformed_value = '1' if value != "" else '2'

            result[q_code] = transformed_value

        return result

    def _create_pck(self, transformed_data):
        """Return a pck file using provided data"""
        pck = CSFormatter.get_pck(
            transformed_data,
            self.ids.survey_id,
            self.ids.ru_ref,
            self.ids.ru_check,
            self.ids.period
        )
        return pck

    def create_pck(self):
        bound_logger = logger.bind(ru_ref=self.ids.ru_ref, tx_id=self.ids.tx_id)
        bound_logger.info("Transforming data for processing")
        transformed_data = self.transform()
        bound_logger.info("Data successfully transformed")
        pck_name = CSFormatter.pck_name(self.ids.survey_id, self.ids.tx_id)
        pck = self._create_pck(transformed_data)
        return pck_name, pck
