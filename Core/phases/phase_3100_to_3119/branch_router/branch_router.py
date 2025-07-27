# branch_router.py

def route_decision(input_text):
    if 'finance' in input_text.lower():
        return 'finance_agent'
    elif 'marketing' in input_text.lower():
        return 'marketing_agent'
    elif 'legal' in input_text.lower():
        return 'compliance_agent'
    else:
        return 'general_agent'
