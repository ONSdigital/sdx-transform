from sdx_gcp.app import get_logger

from decimal import Decimal
from transform.settings import USE_IMAGE_SERVICE
from transform.transformers.common_software.cs_formatter import CSFormatter
from transform.transformers.common_software.mwss.mwss_transform_spec import MatchType, TEMPLATE, TRANSFORMS, Transform
from transform.transformers.response import SurveyResponse
from transform.transformers.survey import Survey
from transform.transformers.survey_transformer import SurveyTransformer

logger = get_logger()


def perform_transforms(
        data: dict[str, str],
        template: dict[str, str]) -> dict[str, int]:

    result = {}

    for qcode, v in template.items():
        if v.startswith("#"):
            x = data[v[1:]]
        elif v.startswith("$"):
            x = execute_transform(value=data.get(qcode, None), identifier=v)
        else:
            x = None

        if x is not None:
            result[qcode] = int(x)

    return result


def execute_transform(value: str, identifier: str) -> str:
    transform = TRANSFORMS.get(identifier)
    name = transform["name"]
    args = transform["args"]
    post = transform.get("post", None)
    x = ""

    if name == Transform.EXISTS:
        x = exists(value, **args)
    elif name == Transform.ROUND:
        x = round_towards(value, **args)
    elif name == Transform.AGGREGATE:
        x = aggregate(value, **args)
    elif name == Transform.ANY_MATCHES:
        x = any_matches(value, **args)
    elif name == Transform.MEAN:
        x = mean(value, **args)
    elif name == Transform.ANY_DATE:
        x = any_date(value, **args)
    elif name == Transform.CONCAT:
        x = concat(value, **args)

    if post is not None:
        x = execute_transform(value=x, identifier=post)

    return x


def exists(value: str, on_true: str, on_false: str) -> str:
    if value is not None and value != "":
        return on_true
    return on_false


def round_towards(value: str, precision: str, rounding_direction: str) -> str:
    val = Decimal(value)
    if precision:
        return str(val.quantize(Decimal(precision), rounding=rounding_direction))
    return value


def aggregate(value: str, values: list[str], weight: str) -> str:
    if value is None:
        value = 0
    return str(Decimal(value) + sum(Decimal(v) * Decimal(weight) for v in values if v is not None))


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


def concat(value: str, values: list[str], seperator: str) -> str:
    values.append(value)
    return seperator.join(values)


def mean(value: str, values: list[str]) -> str:
    values.append(value)
    data = [Decimal(i) for i in values if i is not None]
    divisor = len(data) or 1
    return str(sum(data) / divisor)


class MWSSTransformer2(SurveyTransformer):

    def __init__(self, response: SurveyResponse, seq_nr=0):
        super().__init__(response, seq_nr, use_sdx_image=USE_IMAGE_SERVICE)

    def _format_pck(self, transformed_data) -> str:
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
        transformed_data = perform_transforms(self.survey_response.data, TEMPLATE)
        bound_logger.info("Data successfully transformed")

        bound_logger.info("Creating PCK")
        pck_name = CSFormatter.pck_name(self.survey_response.survey_id, self.survey_response.tx_id)
        pck = self._format_pck(transformed_data)
        bound_logger.info("Successfully created PCK")
        return pck_name, pck
