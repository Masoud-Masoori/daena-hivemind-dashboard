def contextualize_response(raw_response, user_context):
    return f"[Contextualizer] ({user_context}) => {raw_response}"

if __name__ == "__main__":
    print(contextualize_response("Here is the report.", "Marketing Dept"))
