import sys
import os
import inspect
from datetime import datetime

from rkd.api.testing import BasicTestingCase

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../'
sys.path.insert(0, path)

from infracheck.infracheck.model import ExecutedCheckResult


class ExecutedCheckResultTest(BasicTestingCase):
    def test_from_not_ready(self):
        result = ExecutedCheckResult.from_not_ready('Durruti', description='Buenaventura')

        self.assertEqual(False, result.exit_status)
        self.assertIsNone(result.refresh_time)

    def test_to_hash(self):
        check = ExecutedCheckResult(
            configured_name='Durruti',
            output='Viva la revolution!',
            exit_status=True,
            hooks_output='A las barricadas!',
            description='For the triumph of the libertarian confederation!',
            is_silenced=False
        )

        check.refresh_time = datetime(2020, 11, 27, 23, 40, 18)  # mock the time
        as_hash: dict = check.to_hash()

        self.assertEqual({
            'checked_at': '2020-11-27 23-40-18',
            'hooks_output': 'A las barricadas!',
            'ident': 'Durruti=True, silenced=False',
            'output': 'Viva la revolution!',
            'status': True,
            'description': 'For the triumph of the libertarian confederation!'
        }, as_hash)
