import requests


def currency(c_from, c_to, value):
    value = value
    from_to = c_from + "_" + c_to
    res = requests.get("https://free.currencyconverterapi.com/api/v6/convert",
                       params={'q': from_to, 'compact': 'ultra'})
    data = res.json()
    result = data[from_to]
    result = result * value
    return result


print(currency("USD", "KZT", 10))  # 10 доллар в тенге
