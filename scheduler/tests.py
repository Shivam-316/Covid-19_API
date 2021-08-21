from django.test import TestCase
from .management.commands._v1private import get_cases_data, get_state_codes, get_vaccination_data
import pandas

class CasesTestCase(TestCase):
    def test_cases_data(self):
        cases = get_cases_data()
        self.assertIsInstance(cases, pandas.core.frame.DataFrame)

class VaccinationTestCase(TestCase):  
    def test_vacc_data(self):
        vacc = get_vaccination_data()
        self.assertIsInstance(vacc, pandas.core.frame.DataFrame)

class CodesTestCase(TestCase):
    def test_codes_data(self):
        codes = get_state_codes()
        self.assertIsInstance(codes, pandas.core.frame.DataFrame)
