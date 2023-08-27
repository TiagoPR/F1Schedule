import requests
from xml.etree import ElementTree as ET
from datetime import datetime
import pytz
from event import create_event

# api-endpoint
URL = "http://ergast.com/api/f1/current"

# sending get request and saving the response as response object
response = requests.get(url=URL)

# XML data from the API response
xml_data = response.text

# Parse the XML data
root = ET.fromstring(xml_data)

portugal_timezone = pytz.timezone('Europe/Lisbon')

for race_element in root.findall('.//{http://ergast.com/mrd/1.5}Race'):
    race_name = race_element.find('{http://ergast.com/mrd/1.5}RaceName').text
    race_time = race_element.find('{http://ergast.com/mrd/1.5}Time')
    race_date = race_element.find('{http://ergast.com/mrd/1.5}Date').text
    country = race_element.find('.//{http://ergast.com/mrd/1.5}Country').text.strip()

    print(f"Race: {race_name}")
    print(f"Qualifying Time: {race_time.text}")
    
    if race_time is not None:
        race_utc_time = datetime.strptime(race_date + ' ' + race_time.text, '%Y-%m-%d %H:%M:%SZ')
        race_utc_time_str = race_utc_time.strftime('%Y-%m-%dT%H:%M:%S')

        create_event(race_name, race_utc_time_str)

        print(f"Race Time (UTC): {race_time.text}")
        print(f"Country: {country}")
        print("-" * 20)