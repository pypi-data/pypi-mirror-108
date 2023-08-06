import logging

from .dotted_dict import DottedDict
from .statuses import STATUSES

logger = logging.getLogger(__name__)


class RequestResponse(DottedDict):
    def __init__(self, response, raise_exc=True):
        self.raise_exc = raise_exc
        self.response = response
        self._define_success()

    @classmethod
    def _convert_to_dotted_dict(cls, source_dict):
        for key, value in source_dict.items():
            if not isinstance(value, dict):
                continue
            source_dict[key] = cls._convert_to_dotted_dict(value)
        return DottedDict(source_dict)

    def _define_success(self):
        try:
            json = self.response.json()
        except Exception as exc:
            logging.error("Could not read sms.ru response json.", exc_info=True)
            self.status_message = "Could not read sms.ru response json."

        if self.response.status_code != 200:
            self.success = False
            return

        self.update(self._convert_to_dotted_dict(json))
        self.success = self.status_code in [100, 101, 102, 103, 110]
        self.status_message = STATUSES[self.status_code]
