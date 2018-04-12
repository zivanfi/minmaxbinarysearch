def contains_value(pages, value):
    for page in pages:
        for record in page['contents']:
            if record == value:
                return True
    return False
