import regex as re
import phonenumbers

def handle_phone_number(pn_raw):
    pn_raw = str(pn_raw) #cast to string if not already
    pn = None
    try:
        pn = phonenumbers.format_number(
            phonenumbers.parse(pn_raw),
            phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )
        return pn
    except:
        print(f'NO COUNTRY CODE: {pn_raw}; prepending +1 (USA)')
        try:
            pn_raw = '+1' + pn_raw
            pn = phonenumbers.format_number(
            phonenumbers.parse(pn_raw),
            phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )
            return pn
        except:
            print(f'Phone number {pn_raw} could not be parsed.')
            return pn_raw

def handle_fishery_id(pid):
    match = re.match(r'(\d+)[A-Za-z]+', pid.upper())
    if match:
        _id = int(match.group(1))
        return _id
    else:
        return -1