import re

def get_dollars(dollar_string: str) -> str:
    """applies a regex function to extract a dollar amount substring
    from the larger string
    """
    return re.findall('(\$[0-9]+(\.[0-9]+)?)', dollar_string)[0][0]


def get_numeric_total(dollar_string: str) -> str:
    # gets back a purely numeric figure for a dollar amount substring
    return get_dollars(dollar_string).replace("$","")



def get_figures(email_lines: list) -> dict:
    """extracts dollar amounts for the receipt total and sub_total
    key figures.
    """


    sub_total = ""
    total = ""
    for line in email_lines:
        lower = line.lower()

        if 'sub total' in lower or "subtotal" in lower:
            sub_total = get_numeric_total(lower)
            continue

        if "total" in lower:
            total = get_numeric_total(lower)
            continue

    return {"total":total, "subtotal":sub_total}