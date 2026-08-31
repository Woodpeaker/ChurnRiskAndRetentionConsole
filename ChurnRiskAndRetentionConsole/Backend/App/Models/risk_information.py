class risk_information:
    def __init__(self, risk_name: str, risk_breakdown: str):
        self.risk_name = risk_name
        self.risk_breakdown = risk_breakdown

    def __repr__(self):
        return f"risk_information(risk_name='{self.risk_name}', risk_breakdown='{self.risk_breakdown}')"