import urllib.request
import json

URL = 'https://www.tinkoff.ru/api/v1/currency_rates/'


response = urllib.request.urlopen(URL)
data = response.read().decode(response.headers.get_content_charset())
response.close()
parsedJson = json.loads(data)


def validate_code_vs_name(category_list, valid_code_name_pairs):
    valid_name_code_pairs = {v: k for k, v in valid_code_name_pairs.items()}  # for reversed Name vs Code check
    errors = []  # to collect wrong code<>currency mappings
    for category in category_list:
        validate_currency(category['fromCurrency'], valid_code_name_pairs, valid_name_code_pairs, errors)
        validate_currency(category['toCurrency'], valid_code_name_pairs, valid_name_code_pairs, errors)
    return errors


def validate_currency(currency, valid_code_name_pairs, valid_name_code_pairs, error_collector):
    # print currency
    code = currency['code']
    name = currency['name']
    if (code in valid_code_name_pairs and name != valid_code_name_pairs[code])\
            or (name in valid_name_code_pairs and code != valid_name_code_pairs[name]):
        error_collector.append("wrong currency code <> name mapping: " + str(currency))


valid_code_name_pairs = {643: 'RUB', 840: 'USD', 978: 'EUR', 826: 'GBP'}

errors = validate_code_vs_name(parsedJson['payload']['rates'], valid_code_name_pairs)

print("total errors: ", len(errors))
for err in errors:
    print(err)

