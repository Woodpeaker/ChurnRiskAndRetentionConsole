import os
import sys
import unittest

# Ensure repo root is on sys.path so we can import the Backend package
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from Backend.App.Services import risk_score_service, outreach_service
from Backend.App.Models.outreach import Outreach


class DummyCustomer:
    def __init__(self, outreach=None):
        self.outreach = outreach


class ServicesTestCase(unittest.TestCase):
    def test_get_all_risk_information(self):
        infos = risk_score_service.GetAllRiskInformation()
        self.assertIsInstance(infos, list)
        self.assertEqual(len(infos), 2)

    def test_calculate_risk_score_all_factors(self):
        customer = {"churn": True, "tenure": 6}
        score, risks = risk_score_service.CalculateRiskScore(customer)
        self.assertEqual(score, 80)
        self.assertIsInstance(risks, list)
        self.assertEqual(len(risks), 2)

    def test_calculate_risk_score_no_risks(self):
        customer = {"churn": False, "tenure": 24}
        score, risks = risk_score_service.CalculateRiskScore(customer)
        self.assertEqual(score, 0)
        self.assertEqual(risks, [])

    def test_update_outreach_status_transitions(self):
        c = DummyCustomer(Outreach.NOT_CONTACTED)
        c = outreach_service.UpdateOutreachStatus(c)
        self.assertEqual(c.outreach, Outreach.IN_PROGRESS)

        c = outreach_service.UpdateOutreachStatus(c)
        self.assertEqual(c.outreach, Outreach.RESOLVED)

        # RESOLVED should remain RESOLVED (no further change in service)
        c = outreach_service.UpdateOutreachStatus(c)
        self.assertEqual(c.outreach, Outreach.RESOLVED)


if __name__ == "__main__":
    unittest.main()
