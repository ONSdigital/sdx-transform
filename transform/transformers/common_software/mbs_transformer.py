import datetime
import decimal
from decimal import ROUND_HALF_UP, Decimal

import structlog

from transform.transformers.common_software.cs_formatter import CSFormatter
from transform.transformers.response import SurveyResponseV1
from transform.transformers.survey_transformer import SurveyTransformer

logger = structlog.get_logger()


class MBSTransformer(SurveyTransformer):
    """Perform the transforms and formatting for the MBS survey."""

    @staticmethod
    def round_mbs(value):
        """MBS rounding is done on a ROUND_HALF_UP basis and values are divided by 1000 for the pck"""
        try:
            # Set the rounding context for Decimal objects to ROUND_HALF_UP
            decimal.getcontext().rounding = ROUND_HALF_UP
            return Decimal(round(Decimal(float(value))) / 1000).quantize(1)

        except TypeError:
            logger.info("Tried to quantize a NoneType object. Returning None")
            return None

    @staticmethod
    def convert_str_to_int(value):
        """Convert submitted data to int in the transform"""
        try:
            return int(value)
        except TypeError:
            logger.info("Tried to transform None to int. Returning None.")
            return None

    @staticmethod
    def parse_timestamp(text):
        """Parse a text field for a date or timestamp.

        Date and time formats vary across surveys.
        This method reads those formats.

        :param str text: The date or timestamp value.
        :rtype: Python date or datetime.

        """

        cls = datetime.datetime

        if text:
            if text.endswith("Z"):
                return cls.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(
                    tzinfo=datetime.timezone.utc
                )

            try:
                return cls.strptime(text, "%Y-%m-%dT%H:%M:%S.%f%z")

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

            if len(text) != 6:
                return None

            try:
                return cls.strptime(text + "01", "%Y%m%d").date()

            except ValueError:
                return None

    def __init__(self, response: SurveyResponseV1, seq_nr=0):

        super().__init__(response, seq_nr)

        self.employment_questions = ("51", "52", "53", "54")
        self.turnover_questions = ("49",)

        self.idbr_ref = {
            "0106": "T106G",
            "0111": "T111G",
            "0161": "T161G",
            "0117": "T117G",
            "0123": "T123G",
            "0158": "T158G",
            "0167": "T167G",
            "0173": "T173G",
            "0201": "MB01B",
            "0202": "MB01B",
            "0203": "MB03B",
            "0204": "MB03B",
            "0205": "MB15B",
            "0216": "MB15B",
            "0251": "MB51B",
            "0253": "MB53B",
            "0255": "MB65B",
            "0817": "T817G",
            "0823": "T823G",
            "0867": "T867G",
            "0873": "T873G",
        }

    def check_employee_totals(self):
        """Populate qcode 51:54 based on d50"""
        if self.survey_response.data.get("d50") == "Yes":
            logger.info("Setting default values to 0 for question codes 51:54")
            return {q_id: 0 for q_id in self.employment_questions}

        else:
            logger.info("d50 not yes. No default values set for question codes 51:54.")
            employee_totals = {}

            for q_id in self.employment_questions:
                # QIDSs 51 - 54 aren't compulsory. If a value isn't present,
                # then it doesn't need to go in the PCK file.
                try:
                    employee_totals[q_id] = self.convert_str_to_int(
                        self.survey_response.data.get(q_id)
                    )
                except TypeError:
                    logger.info(f"No answer supplied for {q_id}. Skipping.")

            return employee_totals

    def check_turnover_totals(self):
        """Populate qcode 49 based on d49"""
        if self.survey_response.data.get("d49") == "Yes":
            logger.info("Setting default value to 0 for question code 49")
            return {q_id: 0 for q_id in self.turnover_questions}

        else:
            logger.info("d49 not yes. No default values set for question code 49.")
            turnover_totals = {}

            for q_id in self.turnover_questions:
                try:
                    turnover_totals[q_id] = self.round_mbs(
                        self.survey_response.data.get(q_id)
                    )
                except TypeError:
                    logger.info(f"No answer supplied for {q_id}. Skipping.")

            return turnover_totals

    def survey_dates(self):
        """If questions 11 or 12 don't appear in the survey data, then populate
        them with the period start and end date found in the metadata
        """
        try:
            start_date = MBSTransformer.parse_timestamp(self.survey_response.data["11"])
        except KeyError:
            logger.info("Populating start date using metadata")
            ref_period_start_date = self.survey_response.ref_period_start_date
            if ref_period_start_date is None:
                raise KeyError
            start_date = MBSTransformer.parse_timestamp(ref_period_start_date)

        try:
            end_date = MBSTransformer.parse_timestamp(self.survey_response.data["12"])
        except KeyError:
            logger.info("Populating end date using metadata")
            ref_period_end_date = self.survey_response.ref_period_end_date
            if ref_period_end_date is None:
                raise KeyError
            end_date = MBSTransformer.parse_timestamp(ref_period_end_date)

        return {"11": start_date, "12": end_date}

    def _transform(self):
        """Perform a transform on survey data."""
        employee_totals = self.check_employee_totals()
        turnover_totals = self.check_turnover_totals()
        dates = self.survey_dates()

        logger.info(
            "Transforming data for {}".format(self.survey_response.ru_ref),
            tx_id=self.survey_response.tx_id
        )

        transformed_data = {
            "146": 1 if self.survey_response.data.get("146") is not None else 2,
            "40": self.round_mbs(self.survey_response.data.get("40")),
            "42": self.round_mbs(self.survey_response.data.get("42")),
            "43": self.round_mbs(self.survey_response.data.get("43")),
            "46": self.round_mbs(self.survey_response.data.get("46")),
            "47": self.round_mbs(self.survey_response.data.get("47")),
            "90": self.round_mbs(self.survey_response.data.get("90")),
            "50": MBSTransformer.convert_str_to_int(self.survey_response.data.get("50")),
            "110": MBSTransformer.convert_str_to_int(self.survey_response.data.get("110")),
        }

        return {
            k: v
            for k, v in {**transformed_data, **employee_totals, **turnover_totals, **dates}.items()
            if v is not None
        }

    def create_pck(self, img_seq=None):
        logger.info("Creating PCK", ru_ref=self.survey_response.ru_ref)
        pck_name = CSFormatter.pck_name(self.survey_response.survey_id, self.survey_response.tx_id)
        transformed_data = self._transform()
        pck = CSFormatter.get_pck(
            transformed_data,
            self.idbr_ref[self.survey_response.instrument_id],
            self.survey_response.ru_ref,
            self.survey_response.ru_check,
            self.survey_response.period,
        )

        return pck_name, pck
