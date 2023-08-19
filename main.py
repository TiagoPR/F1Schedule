import requests
from xml.etree import ElementTree as ET
from datetime import datetime
import pytz

# api-endpoint
URL = "http://ergast.com/api/f1/current"

# sending get request and saving the response as response object
response = requests.get(url=URL)

# XML data from the API response
xml_data = response.text

# Parse the XML data
root = ET.fromstring(xml_data)

# Create a dictionary to map country names to their timezones
country_timezones = {
    "Bahrain": "Asia/Bahrain",
    "Saudi Arabia": "Asia/Riyadh",
    "Australia": "Australia/Sydney",
    "Azerbaijan": "Asia/Baku",
    "Miami": "America/New_York",
    "Monaco": "Europe/Monaco",
    "Spain": "Europe/Madrid",
    "Canada": "America/Toronto",
    "Austria": "Europe/Vienna",
    "United Kingdom": "Europe/London",
    "Hungary": "Europe/Budapest",
    "Belgium": "Europe/Brussels",
    "Netherlands": "Europe/Amsterdam",
    "Italy": "Europe/Rome",
    "Singapore": "Asia/Singapore",
    "Japan": "Asia/Tokyo",
    "Qatar": "Asia/Qatar",
    "United States": "America/New_York",
    "Mexico": "America/Mexico_City",
    "Brazil": "America/Sao_Paulo",
    "Las Vegas": "America/Los_Angeles",
    "UAE": "Asia/Dubai"
}

# Iterate through each <Race> element
for race_element in root.findall('.//{http://ergast.com/mrd/1.5}Race'):
    race_name = race_element.find('{http://ergast.com/mrd/1.5}RaceName').text
    race_time = race_element.find('{http://ergast.com/mrd/1.5}Time')
    country = race_element.find('.//{http://ergast.com/mrd/1.5}Country').text.strip()

    print(f"Race: {race_name}")
    print(f"Qualifying Time: {race_time.text}")
    
    if race_time is not None and country in country_timezones:
        timezone = pytz.timezone(country_timezones[country])
        race_date = race_element.find('{http://ergast.com/mrd/1.5}Date').text
        race_datetime = datetime.strptime(race_date + ' ' + race_time.text, '%Y-%m-%d %H:%M:%SZ')
        localized_time = race_datetime.astimezone(timezone)
        
        print(f"Race Time: {race_time.text}")
        print(f"Country: {country}")
        print(f"Original Time: {race_time.text}")
        print(f"Localized Time: {localized_time.strftime('%H:%M:%S %Z%z')}")
        print("-" * 20)