import unittest
import sys
import os
import inspect
from unittest_data_provider import data_provider

from infracheck.infracheck.exceptions import CheckNotReadyShouldBeSkippedSignal
from infracheck.infracheck.model import ConfiguredCheck

TESTS_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../'
sys.path.insert(0, TESTS_PATH)

from time import sleep
from infracheck.infracheck.runner import Runner
from infracheck.infracheck.config import ConfigLoader
from infracheck.infracheck.repository import Repository
from rkd.api.inputoutput import IO


class RunnerTest(unittest.TestCase):
    def provide_data() -> list:
        return [
            # url does not exist: will return False
            [
                'http',
                {
                    'url': 'https://duckduckgo-some-invalid-domain.com'
                },
                {
                    'on_each_up': ['echo "is up"'],
                    'on_each_down': ['echo "is down"']
                },
                False,
                'is down'
            ],

            # valid HTTP health check
            # checks also if the on_each_up hook is called
            [
                'http',
                {
                    'url': 'https://duckduckgo.com'
                },
                {
                    'on_each_up': ['echo "it works"'],
                    'on_each_down': ['echo "this should not show"']
                },
                True,
                'it works'
            ],
        ]

    @data_provider(provide_data)
    def test_run_with_hooks(self, check_type: str, input_data: dict, hooks: dict,
                            expected_result: bool, expected_text: str) -> None:

        result = self._create_runner().run_single_check(
            ConfiguredCheck.from_config(
                'some-check-name',
                {
                    'type': check_type,
                    "input": input_data,
                    'hooks': hooks
                },
                IO()
            )
        )

        self.assertEqual(expected_result, result.exit_status)
        self.assertEqual(expected_text, result.hooks_output)

    def test_injects_variables(self) -> None:
        out = self._create_runner().run_single_check(
            ConfiguredCheck.from_config(
                'some-check-name',
                {
                    'type': 'printr',
                    "input": {'message': 'Current user is ${ENV.USER}, running a ${checkName}'},
                },
                IO()
            )
        )

        self.assertEqual('Current user is ' + os.environ['USER'] + ', running a printr', out.output.strip())

    def test_check_will_not_run_twice_if_cache_lifetime_is_not_reached(self) -> None:
        runner = self._create_runner()

        out_first = runner.run_single_check(
            ConfiguredCheck.from_config(
                'cache-check',
                {
                    'type': 'printr',
                    "input": {'message': 'First message'},
                    'results_cache_time': 1
                },
                IO()
            )
        )
        runner.repository.push_to_cache('cache-check', out_first)

        with self.assertRaises(CheckNotReadyShouldBeSkippedSignal):
            runner.run_single_check(
                ConfiguredCheck.from_config(
                    'cache-check',
                    {
                        'type': 'printr',
                        "input": {'message': 'Second message'},
                        'results_cache_time': 1
                    },
                    IO()
                )
            )

        # second attempt: after 2 seconds (where results_cache_time=1s)
        sleep(2)
        out_third = runner.run_single_check(
            ConfiguredCheck.from_config(
                'cache-check',
                {
                    'type': 'printr',
                    "input": {'message': 'Third message'},
                    'results_cache_time': 1
                },
                IO()
            )
        )
        runner.repository.push_to_cache('cache-check', out_third)

        self.assertEqual('First message\n', out_first.output)
        self.assertEqual('Third message\n', out_third.output)

    @staticmethod
    def _create_runner() -> Runner:
        dirs = [TESTS_PATH + '/../example/healthchecks', TESTS_PATH + '/infracheck/']

        return Runner(dirs,
                      config_loader=ConfigLoader(dirs, IO()),
                      repository=Repository(dirs),
                      io=IO())
