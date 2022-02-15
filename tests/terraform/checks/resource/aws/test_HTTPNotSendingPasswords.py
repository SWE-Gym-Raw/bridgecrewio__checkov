import unittest
from pathlib import Path

from checkov.terraform.runner import Runner
from checkov.runner_filter import RunnerFilter
from checkov.terraform.checks.resource.aws.GlueSecurityConfigurationEnabled import check


class TestHTTPNotSendingPasswords(unittest.TestCase):
    def test(self):
        # given
        test_files_dir = Path(__file__).parent / "exampe_HTTPNotSendingPasswords"

        # when
        report = Runner().run(root_folder=str(test_files_dir), runner_filter=RunnerFilter(checks=[check.id]))

        # then
        summary = report.get_summary()

        passing_resources = {
            "aws_glue_crawler.enabled",
            "aws_glue_dev_endpoint.enabled",
            "aws_glue_job.enabled",
        }
        failing_resources = {
            "aws_glue_crawler.default",
            "aws_glue_dev_endpoint.default",
            "aws_glue_job.default",
        }

        passed_check_resources = {c.resource for c in report.passed_checks}
        failed_check_resources = {c.resource for c in report.failed_checks}

        self.assertEqual(summary["passed"], 3)
        self.assertEqual(summary["failed"], 3)
        self.assertEqual(summary["skipped"], 0)
        self.assertEqual(summary["parsing_errors"], 0)

        self.assertEqual(passing_resources, passed_check_resources)
        self.assertEqual(failing_resources, failed_check_resources)


if __name__ == "__main__":
    unittest.main()
