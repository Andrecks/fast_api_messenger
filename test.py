import phonenumbers

def test(phone):
    parsed_number = phonenumbers.parse(phone)
    return phonenumbers.is_valid_number(parsed_number) and phonenumbers.is_possible_number(parsed_number)

print(test('+79166477954'))