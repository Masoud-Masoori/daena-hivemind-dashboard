def integrate_feedback(feedback_data):
    print(" Integrating live user feedback...")
    for entry in feedback_data:
        print(f" - {entry['user']}: {entry['comment']}")
