import re


def remove_diacritics(text: str):
    chars = "àáäâèéëêìíïîòóöôùúüûñç"
    trans = "aaaaeeeeiiiioooouuuunc"
    trans_table = str.maketrans(chars, trans)
    return text.translate(trans_table)


def slugify(text: str):
    text = text.lower()
    text = remove_diacritics(text)
    # Remove whitespace
    text = re.sub(r"[\s_]+", "-", text)
    # Remove special characters
    text = re.sub(r"[^a-z0-9\-]", "", text)
    # Remove consecutive hyphens
    text = re.sub(r"-+", "-", text)
    # Trim to 40 chars max
    text = text[:40]
    # Strip hyphens from beginning and end
    text = text.strip("-")
    return text


def or_empty(text: str | None):
    return "" if text is None else text
