from collections import namedtuple
import datetime
import logging


class CSFormatter:

    formIds = {
        "008": "MS31B",
        "017": "STW01",
        "050": "0008",
        "134": "0004",
        "141": "HE2015",
        "0102": "RSI5B",  # TODO: Check which mapping
    }

    Identifiers = namedtuple("Identifiers", [
        "batchNr", "seqNr", "ts", "txId", "surveyId", "instId",
        "formId", "ruRef", "ruChk", "period"
    ])

    @staticmethod
    def identifiers(data, batchNr=0, seqNr=0, log=None):
        log = log or logging.getLogger(__name__)
        ruRef = data.get("metadata", {}).get("ru_ref")
        rv = CSFormatter.Identifiers(
            batchNr, seqNr, datetime.date.today(),
            data.get("tx_id"),
            data.get("survey_id"),
            data.get("collection", {}).get("instrument_id"),
            CSFormatter.formIds.get(data.get("collection", {}).get("instrument_id")),
            ''.join(i for i in ruRef if i.isdigit()),
            ruRef[-1] if ruRef[-1].isalpha() else "",
            data.get("collection", {}).get("period")
        )
        if any(i is None for i in rv):
            log.warning("Missing an id from {0}".format(rv))
            return None
        else:
            return rv

    @staticmethod
    def batch_header(batchNr, ts):
        return "{0}{1:06}{2}".format("FBFV", batchNr, ts.strftime("%d/%m/%y"))

    @staticmethod
    def form_header(formId, ruRef, ruChk, period):
        formId = "{0:04}".format(formId) if isinstance(formId, int) else formId
        return "{0}:{1}{2}:{3}".format(formId, ruRef, ruChk, period)

    @staticmethod
    def pck_lines(data, batchNr, ts, formId, ruRef, ruChk, period, **kwargs):
        return [
            CSFormatter.batch_header(batchNr, ts),
            "FV",
            CSFormatter.form_header(formId, ruRef, ruChk, period),
        ] + [
            " ".join((q, a)) for q, a in data.items()
        ]
