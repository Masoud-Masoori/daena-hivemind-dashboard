def check_sanity(response):
    suspicious = any(phrase in response.lower() for phrase in ["kill", "hack", "illegal"])
    return "[SanityCheck]  Invalid Output" if suspicious else "[SanityCheck]  Passed"

if __name__ == "__main__":
    print(check_sanity("Hack the mainframe."))
