from ..Models.risk_information import risk_information

churn_risk_info = risk_information("Risk of Churning", "Customer is known to be at risk of churning. +50 risk points")
Tenure_risk_info = risk_information("Short term tenure", "Customer has a short tenure. +30 risk points")

def GetAllRiskInformation():
    return [churn_risk_info, Tenure_risk_info]

def CalculateRiskScore(customer_data):
	"""
	Calculate the risk score for a customer based on their data.
	Parameters:
	customer_data (dict): A dictionary containing customer information with 'churn' and 'tenure' keys.
	Returns:
	tuple: A tuple containing the risk score and list of risks.
	"""
	# Example calculation logic (this should be replaced with actual logic)
	risk_score = 0
	list_of_risks = []
	# Example factors that might influence the risk score
	if customer_data.get('churn') == True:
		risk_score += 50
		list_of_risks.append(churn_risk_info)
	if customer_data.get('tenure', 0) < 12:
		risk_score += 30
		list_of_risks.append(Tenure_risk_info)
	return risk_score, list_of_risks