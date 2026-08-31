from ..Models.outreach import Outreach

def UpdateOutreachStatus(customer_data):
	current_outreach = customer_data.outreach
	if current_outreach == Outreach.NOT_CONTACTED:
		customer_data.outreach = Outreach.IN_PROGRESS
	elif current_outreach == Outreach.IN_PROGRESS:
		customer_data.outreach = Outreach.RESOLVED
	return customer_data
