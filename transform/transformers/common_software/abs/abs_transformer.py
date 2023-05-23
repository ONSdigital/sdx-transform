import decimal
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from sdx_gcp.app import get_logger

from transform.settings import USE_IMAGE_SERVICE
from transform.transformers.common_software.abs.abs_transforms import motor_trades, whole_sale, catering, \
    property_survey, transport_services, service_commission, computer_industry, other_services, postal, non_marketing, \
    duty, standard, construction

from transform.transformers.common_software.cs_formatter import CSFormatter
from transform.transformers.response import SurveyResponse
from transform.transformers.survey_transformer import SurveyTransformer

logger = get_logger()


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
    """Add the values in the list"""
    total = 0
    for v in values:
        if v is not None and v != '':
            total += round_and_divide_by_one_thousand(v)
    return total


def convert_period_data(value):
    return datetime.strptime(value, "%d/%m/%Y")


class ABSTransformer(SurveyTransformer):
    """Perform the transforms and formatting for the ABS survey."""

    # a dictionary mapping the instrument id to the sector id required downstream
    inst_map = {'1802': '053',
                '1804': '051',
                '1808': '050',
                '1810': '055',
                '1812': '052',
                '1814': '052',
                '1818': '052',
                '1820': '052',
                '1824': '052',
                '1826': '052',
                '1862': '001',
                '1864': '001',
                '1874': '001',
                }

    # a dictionary mapping the instrument id to the required transformations
    transformation_map = {'1802': motor_trades,
                          '1804': whole_sale,
                          '1808': catering,
                          '1810': property_survey,
                          '1812': transport_services,
                          '1814': service_commission,
                          '1818': computer_industry,
                          '1820': other_services,
                          '1824': postal,
                          '1826': non_marketing,
                          '1862': duty,
                          '1864': standard,
                          '1874': construction,
                          }

    def __init__(self, response: SurveyResponse, seq_nr=0):
        period = self._extract_year(response.ref_period_start_date)
        response.period = '20' + period + '12'
        super().__init__(response, seq_nr, use_sdx_image=USE_IMAGE_SERVICE)
        self.period = period

    def _extract_year(self, ref_period_start_date: str):
        """Extract the reference period as YY from the metadata"""
        start_date = datetime.strptime(ref_period_start_date, "%Y-%m-%d")
        return start_date.strftime("%y")

    def _get_value(self, q_code):
        input_dict = self.survey_response.data
        if q_code in input_dict:
            value = input_dict.get(q_code)
            return value if value != '' else None
        else:
            return None

    def transform(self):
        result = {}

        transformations = self.transformation_map.get(self.survey_response.instrument_id)

        for q_code, transformation in transformations.items():

            value = self._get_value(q_code)
            transformed_value = value

            if value is None:
                if type(transformation) == dict:
                    transformed_value = transformation.get(value)

                elif type(transformation) == list:
                    if transformation[0] == 'sum':
                        inputs = []
                        for q in transformation[1:]:
                            inputs.append(self._get_value(q))
                        transformed_value = combine_sum(inputs)

                elif transformation == 'comment':
                    transformed_value = 2

                else:
                    continue

            elif type(transformation) == dict:
                transformed_value = transformation.get(value)
            elif transformation == 'nearest_thousand':
                transformed_value = round_and_divide_by_one_thousand(value)
            elif transformation == 'period_data':
                transformed_value = convert_period_data(value)
            elif transformation == 'comment':
                transformed_value = 1 if value != "" else 2

            result[q_code] = transformed_value

        return result

    def populate_period_data(self):
        """If questions 11 or 12 don't appear in the survey data, then populate
        them with the period start and end date found in the metadata
        """
        data = self.survey_response.data
        if '11' not in data:
            start_date = datetime.strptime(self.survey_response.ref_period_start_date, "%Y-%m-%d")
            data['11'] = start_date.strftime("%d/%m/%Y")
        if '12' not in data:
            end_date = datetime.strptime(self.survey_response.ref_period_end_date, "%Y-%m-%d")
            data['12'] = end_date.strftime("%d/%m/%Y")

    def _format_pck(self, transformed_data):
        """Return a pck file using provided data"""
        pck = CSFormatter.get_pck(
            transformed_data,
            self.survey_response.instrument_id,
            self.survey_response.ru_ref,
            self.survey_response.ru_check,
            self.period
        )
        return pck

    def create_pck(self):
        bound_logger = logger.bind(ru_ref=self.survey_response.ru_ref, tx_id=self.survey_response.tx_id)
        bound_logger.info("Transforming data for processing")
        self.populate_period_data()
        transformed_data = self.transform()
        bound_logger.info("Data successfully transformed")
        sector_id = self.inst_map[self.survey_response.instrument_id]
        pck_name = CSFormatter.pck_name(sector_id, self.survey_response.tx_id)
        pck = self._format_pck(transformed_data)
        return pck_name, pck
