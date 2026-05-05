import io
import unittest
from unittest.mock import patch

from pxgrid_util import Config
from pxgrid_util.filtering import build_query_payload
from pxgrid_util.filtering import validate_filter_syntax


class TestFiltering(unittest.TestCase):
    def test_validate_filter_syntax_accepts_valid_expression(self):
        expression = "sessions[?state == 'STARTED']"
        self.assertEqual(validate_filter_syntax(expression), expression)

    def test_validate_filter_syntax_rejects_invalid_expression(self):
        with self.assertRaisesRegex(ValueError, "invalid JMESPath filter syntax"):
            validate_filter_syntax("sessions[?")

    def test_build_query_payload_omits_empty_values(self):
        self.assertEqual(build_query_payload(), {})

    def test_build_query_payload_includes_timestamp_and_filter(self):
        payload = build_query_payload(
            start_timestamp="2026-05-01T00:00:00.000+00:00",
            filter_value="sessions[?state == 'STARTED']",
        )
        self.assertEqual(
            payload,
            {
                "startTimestamp": "2026-05-01T00:00:00.000+00:00",
                "filter": "sessions[?state == 'STARTED']",
            },
        )

    def test_config_accepts_valid_filter(self):
        argv = ["session-query-all", "--filter", "sessions[?state == 'STARTED']"]
        with patch("sys.argv", argv):
            config = Config()
            self.assertEqual(config.filter, "sessions[?state == 'STARTED']")

    def test_config_rejects_invalid_filter(self):
        argv = ["session-query-all", "--filter", "sessions[?"]
        with patch("sys.argv", argv), patch("sys.stderr", new=io.StringIO()):
            config = Config()
            with self.assertRaises(SystemExit):
                config.parse_args()


if __name__ == "__main__":
    unittest.main()
