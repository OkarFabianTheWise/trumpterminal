def remove_quotes(text):
    try:
        if text.startswith('"') and text.endswith('"'):
            return text[1:-1]
        return text
    except Exception as error:
        print("Error::remove_quotes:", error)
        return text