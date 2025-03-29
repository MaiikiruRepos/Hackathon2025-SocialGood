import pycountry

def country_code_to_name(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return None
