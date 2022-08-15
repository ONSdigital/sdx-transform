from datetime import datetime, date, timezone
from typing import Union, Dict, Optional

import structlog

logger = structlog.get_logger()


class MissingIdsException(Exception):
    pass


class SurveyResponse:

    def __init__(self, response: dict):
        self.response = response

        # extract string fields
        self.tx_id: str = self._extract("tx_id")
        self.survey_id: str = self._extract("survey_id")
        self.instrument_id: str = self._extract("collection", "instrument_id")
        self.period: str = self._extract("collection", "period")
        ru_ref = self._extract("metadata", "ru_ref")
        self.ru_ref: str = ru_ref[0:-1]
        self.ru_check: str = ru_ref[-1] if ru_ref and ru_ref[-1].isalpha() else ""
        submitted_at = self.response.get("submitted_at")
        self.submitted_at_raw: str = submitted_at if submitted_at else datetime.now(timezone.utc).isoformat()

        self.ref_period_start_date: str = self._extract_optional("metadata", "ref_period_start_date")
        self.ref_period_end_date: str = self._extract_optional("metadata", "ref_period_end_date")

        # extract object fields
        self.submitted_at: Union[datetime, date] = self._parse_date(self.submitted_at_raw)
        self.data: Dict[str, str] = response.get("data")

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
            return self._extract(field_names)
        except MissingIdsException:
            return None

    @staticmethod
    def _parse_date(date_text) -> Union[datetime, date]:
        """Parse a date_text field for a date or timestamp.

        Date and time formats vary across surveys.
        This method reads those formats.

        :rtype: Python date or datetime.

        """
        cls = datetime

        if date_text.endswith("Z"):
            return cls.strptime(date_text, "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=timezone.utc
            )

        try:
            return cls.strptime(date_text, "%Y-%m-%dT%H:%M:%S.%f%z")
        except ValueError:
            pass

        try:
            return cls.strptime(date_text, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            pass

        try:
            return cls.strptime(date_text.partition(".")[0], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            pass

        try:
            return cls.strptime(date_text, "%Y-%m-%d").date()
        except ValueError:
            pass

        try:
            return cls.strptime(date_text, "%d/%m/%Y").date()
        except ValueError:
            pass

        try:
            return cls.strptime(date_text + "01", "%Y%m%d").date()
        except ValueError:
            pass

        raise MissingIdsException("Missing field submitted_at from response")
