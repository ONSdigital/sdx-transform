from sdx_gcp.app import get_logger

from decimal import Decimal
from transform.settings import USE_IMAGE_SERVICE
from transform.transformers.common_software.cs_formatter import CSFormatter
from transform.transformers.common_software.mwss.mwss_transform_spec import MatchType
from transform.transformers.cord.credit_grantors.credit_grantors_transform_spec import Transform, TRANSFORMS_SPEC
from transform.transformers.response import SurveyResponse
from transform.transformers.survey import Survey
from transform.transformers.survey_transformer import SurveyTransformer

logger = get_logger()


def perform_transforms(data: dict[str, str], transforms_spec: dict[str, Transform]) -> dict[str, int]:

    output_dict = {}

    for k, v in transforms_spec.items():
        try:
            if k not in data:
                continue

            if v == Transform.NO_TRANSFORM:
                output_dict[k] = int(data[k])

        except ValueError:
            logger.error(f"Unable to process qcode: {k} as received non numeric value: {v}")

    return output_dict


def round_towards(value: str, precision: str, rounding_direction: str) -> str:
    val = Decimal(value)
    if precision:
        return str(val.quantize(Decimal(precision), rounding=rounding_direction))
    return value


def aggregate(value: str, values: list[str], weight: str) -> str:
    """Calculate the weighted sum of a question group."""
    return str(Decimal(value) + sum(Decimal(v) * Decimal(weight) for v in values))


def any_matches(value: str, values: list[str], match: str, match_type: MatchType, on_true: str, on_false: str) -> str:
    values.append(value)
    for v in values:
        if matches(v, match, match_type):
            return on_true
    return on_false


def matches(value: str, match: str, match_type: MatchType) -> bool:
    if match_type == MatchType.CONTAINS:
        return value in match
    return False


def any_date(value: str, values: list[str], on_true: str, on_false: str) -> str:
    values.append(value)
    for v in values:
        if Survey.parse_timestamp(v) is not None:
            return on_true

    return on_false



def mean(value: str, values: list[str]) -> str:
    values.append(value)
    data = [Decimal(i) for i in values if i is not None]
    divisor = len(data) or 1
    return str(sum(data) / divisor)



class MWSSTransformer(SurveyTransformer):

    def __init__(self, response: SurveyResponse, seq_nr=0):
        super().__init__(response, seq_nr, use_sdx_image=USE_IMAGE_SERVICE)

    def _format_pck(self, transformed_data) -> str:
        """Common software require Blocks to be form type 0001 even though it is 0002 in Author"""
        pck = CSFormatter.get_pck(
            transformed_data,
            self.survey_response.instrument_id,
            self.survey_response.ru_ref,
            self.survey_response.ru_check,
            self.survey_response.period,
        )
        return pck

    def create_pck(self):
        bound_logger = logger.bind(ru_ref=self.survey_response.ru_ref, tx_id=self.survey_response.tx_id)
        bound_logger.info("Transforming data for processing")
        transformed_data = perform_transforms(self.survey_response.data, TRANSFORMS_SPEC)
        bound_logger.info("Data successfully transformed")

        bound_logger.info("Creating PCK")
        pck_name = CSFormatter.pck_name(self.survey_response.survey_id, self.survey_response.tx_id)
        pck = self._format_pck(transformed_data)
        bound_logger.info("Successfully created PCK")
        return pck_name, pck
