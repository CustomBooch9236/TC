import requests
from bs4 import BeautifulSoup

def get_third_country_duty(commodity_code: str) -> str:
    url = f"https://www.trade-tariff.service.gov.uk/commodities/{commodity_code}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.find_all("tr", class_="govuk-table__row")

    for row in rows:
        country_col = row.find("td", class_="country-col")
        measure_type_col = row.find("td", class_="measure-type-col")
        
        if country_col and measure_type_col:
            if "All countries (1011)" in country_col.text and "Third country duty" in measure_type_col.text:
                duty_rate_col = row.find("td", class_="duty-rate-col")
                if duty_rate_col:
                    duty = duty_rate_col.find("span", class_="duty-expression")
                    if duty:
                        return duty.text.strip()

    return "Third country duty not found"

commodity_code = input("Enter Commodity Code: ")
duty = get_third_country_duty(commodity_code)
print(f"Third country duty for {commodity_code}: {duty}")
