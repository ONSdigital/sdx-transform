from datetime import datetime, date, timezone
from typing import Union, Dict, Optional

from sdx_gcp.app import get_logger

from transform.transformers.survey import MissingIdsException, Survey

logger = get_logger()


class InvalidDataException(Exception):
    pass


class SurveyResponse:

    def __init__(self, response: dict):
        self.response = response
        self.tx_id: str = ""
        self.survey_id: str = ""
        self.instrument_id: str = ""
        self.period: str = ""
        self.ru_ref: str = ""
        self.ru_check: str = ""
        self.full_ru_ref: str = ""
        self.submitted_at_raw: str = ""
        self.submitted_at: Union[datetime, date] = datetime.now()
        self.data: Dict[str, str] = {}
        self.ref_period_start_date: str = ""
        self.ref_period_end_date: str = ""

    def _extract(self, *field_names) -> str:
        parent = self.response
        child = None
        for f in field_names:
            child = parent.get(f)
            if child:
                parent = child
            else:
                raise MissingIdsException(f"Missing field {f} from response")
        return child

    def _extract_optional(self, *field_names) -> Optional[str]:
        try:
            return self._extract(*field_names)
        except MissingIdsException:
            return None


class SurveyResponseV1(SurveyResponse):
    """Provide a common interface for accessing survey response metadata/data."""

    def __init__(self, response: dict):
        super().__init__(response)

        # extract string fields
        self.tx_id: str = self._extract("tx_id")
        self.survey_id: str = self._extract("survey_id")
        self.instrument_id: str = self._extract("collection", "instrument_id")
        self.period: str = self._extract("collection", "period")
        ru_ref = self._extract("metadata", "ru_ref")
        self.full_ru_ref: str = ru_ref
        self.ru_ref: str = ru_ref[0:-1] if ru_ref[-1].isalpha() else ru_ref
        self.ru_check: str = ru_ref[-1] if ru_ref and ru_ref[-1].isalpha() else ""
        submitted_at = self.response.get("submitted_at")
        self.submitted_at_raw: str = submitted_at if submitted_at else datetime.now(timezone.utc).isoformat()

        # extract object fields
        self.submitted_at: Union[datetime, date] = Survey.parse_timestamp(self.submitted_at_raw)
        data = response.get("data")
        if not isinstance(data, dict):
            raise InvalidDataException("data is not a dictionary")
        self.data: Dict[str, str] = data

        # these fields are only required by some transformers
        self.ref_period_start_date: str = self._extract_optional("metadata", "ref_period_start_date")
        self.ref_period_end_date: str = self._extract_optional("metadata", "ref_period_end_date")


class SurveyResponseV2(SurveyResponse):
    """Provide a common interface for accessing survey response metadata/data."""

    def __init__(self, response: dict):
        super().__init__(response)

        # extract string fields
        self.tx_id: str = self._extract("tx_id")
        self.survey_id: str = self._extract("survey_metadata", "survey_id")
        self.instrument_id: str = self._extract("survey_metadata", "form_type")
        self.period: str = self._extract("survey_metadata", "period_id")
        ru_ref = self._extract("survey_metadata", "ru_ref")
        self.full_ru_ref: str = ru_ref
        self.ru_ref: str = ru_ref[0:-1] if ru_ref[-1].isalpha() else ru_ref
        self.ru_check: str = ru_ref[-1] if ru_ref and ru_ref[-1].isalpha() else ""
        submitted_at = self.response.get("submitted_at")
        self.submitted_at_raw: str = submitted_at if submitted_at else datetime.now(timezone.utc).isoformat()

        # extract object fields
        self.submitted_at: Union[datetime, date] = Survey.parse_timestamp(self.submitted_at_raw)
        data = response.get("data")
        if not isinstance(data, dict):
            raise InvalidDataException("data is not a dictionary")
        self.data: Dict[str, str] = data

        # these fields are only required by some transformers
        self.ref_period_start_date: str = self._extract_optional("survey_metadata", "ref_p_start_date")
        self.ref_period_end_date: str = self._extract_optional("survey_metadata", "ref_p_end_date")
