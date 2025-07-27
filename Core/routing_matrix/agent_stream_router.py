def route_agent_request(agent_type, payload):
    routes = {"finance": "AlphaFi", "security": "ShadowSentinel", "frontend": "UINexus"}
    return f"[Router]  To {routes.get(agent_type, 'DefaultHandler')}: {payload}"

if __name__ == "__main__":
    print(route_agent_request("frontend", "Build UI"))
