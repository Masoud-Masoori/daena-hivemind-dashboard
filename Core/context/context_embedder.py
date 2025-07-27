def embed_context(message, context):
    return f"[Embed]  {context}  {message}"

if __name__ == "__main__":
    print(embed_context("Load models", "Startup"))
