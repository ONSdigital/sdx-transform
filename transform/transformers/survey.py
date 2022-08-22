import json
from datetime import datetime, date, timezone
from json import JSONDecodeError
from typing import Union

import structlog

logger = structlog.get_logger()


class MissingIdsException(Exception):
    pass


class MissingSurveyException(Exception):
    pass


class Survey:
    """Provide operations and accessors to survey definition."""

    file_pattern = "./transform/surveys/{survey_id}.{instrument_id}.json"

    @staticmethod
    def load_survey(survey_id: str, instrument_id: str, pattern=file_pattern):
        """Retrieve the survey definition by id.

        This function takes metadata from a survey reply, finds the JSON definition of
        that survey, and loads it as a Python object.

        :param survey_id: Survey response ids.
        :param instrument_id
        :param str pattern: A query for the survey definition. This will be
                            a file path relative to the package location which uniquely
                            identifies the survey definition file. It accepts keyword
                            formatting arguments for any of the attributes of
                            :py:class:`sdx.common.survey.Survey.Identifiers`.

                            For example: `"surveys/{survey_id}.{inst_id}.json"`.
        :raises IOError: Raised if file cannot be opened
        :raises JSONDecodeError:  Raised if returned file isn't valid JSON
        :raises UnicodeDecodeError:
        :rtype: dict

        """

        file_name = pattern.format(survey_id=survey_id, instrument_id=instrument_id)
        try:
            with open(file_name, encoding="utf-8") as fh:
                content = fh.read()
                return json.loads(content)
        except FileNotFoundError:
            logger.error("File not found", file_name=file_name)
            raise MissingSurveyException()
        except (OSError, UnicodeDecodeError):
            logger.exception("Error opening file", file=file_name)
            raise Exception("Error opening file")
        except JSONDecodeError:
            logger.exception("File is not valid JSON", file=file_name)
            raise Exception("invalid file")

    @staticmethod
    def bind_logger(log, ids):
        """Bind a structured logger with survey response metadata.

        :param log: The logger object to be bound.
        :param ids: The survey response ids to bind to the logger.
        :type ids: :py:class:`sdx.common.survey.Survey.Identifiers`

        """
        return log.bind(
            ru_ref=ids.ru_ref,
            tx_id=ids.tx_id,
            user_id=ids.user_id,
        )

    @staticmethod
    def parse_timestamp(text) -> Union[datetime, date]:
        """Parse a text field for a date or timestamp.

        Date and time formats vary across surveys.
        This method reads those formats.

        :param str text: The date or timestamp value.
        :rtype: Python date or datetime.

        """

        cls = datetime

        if text.endswith("Z"):
            return cls.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=timezone.utc
            )

        try:
            return cls.strptime(text, "%Y-%m-%dT%H:%M:%S.%f%z")
        except ValueError:
            pass

        try:
            return cls.strptime(text, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            pass

        try:
            return cls.strptime(text.partition(".")[0], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            pass

        try:
            return cls.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            pass

        try:
            return cls.strptime(text, "%d/%m/%Y").date()
        except ValueError:
            pass

        try:
            return cls.strptime(text + "01", "%Y%m%d").date()
        except ValueError:
            pass

        return None
