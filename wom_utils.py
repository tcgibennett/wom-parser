def cleanDataField(field):
    if '.' in field.text:
        return float(field.text.strip().replace(',','').replace('+','') if len(field.text.strip()) > 0 else 0)
    else:
        return int(field.text.strip().replace(',','').replace('+','') if len(field.text.strip()) > 0 else 0)