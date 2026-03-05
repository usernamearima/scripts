import requests
from bs4 import BeautifulSoup


def extract_forms(url):
    forms_data = []

    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "lxml")

        forms = soup.find_all("form")

        for form in forms:
            action = form.get("action")
            method = form.get("method", "GET").upper()

            inputs = []
            for input_tag in form.find_all("input"):
                input_type = input_tag.get("type", "text")
                input_name = input_tag.get("name")
                inputs.append({
                    "type": input_type,
                    "name": input_name
                })

            forms_data.append({
                "action": action,
                "method": method,
                "inputs": inputs
            })

    except requests.RequestException:
        pass

    return forms_data
