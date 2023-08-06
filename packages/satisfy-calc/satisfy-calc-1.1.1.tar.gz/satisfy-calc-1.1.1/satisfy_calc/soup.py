from bs4 import BeautifulSoup
from building import Building
import requests

# URL = 'https://satisfactory.gamepedia.com/Manufacturer'
# page = requests.get(URL)

# soup = BeautifulSoup(page.content, 'html.parser')

# print(soup.prettify())

# inputs = soup.find('b', string='Inputs')
# outputs = soup.find('b', string='Outputs')
# power = soup.find('b', string='Power Usage')

# values = soup.find_all(class_='infobox-row-value')
# for result in results:
#     print(result.prettify())

# for label in labels:
#     print(label)
# print('###############')
# for value in values:
#     print(value)

# for label in labels[-7:-3]:
#     if label.text.strip() == 'Outputs':
#         print(label.text.strip())

# for value in values[-7:-3]:
#     print((value.text).strip())

# print(inputs.parent.parent.find('td').text.strip())
# print(outputs.parent.parent.find('td').text.strip())
# print(power.parent.parent.find('td').text.strip())

# Need to dynamically form this list from a prior scrape
buildings = ['Manufacturer', 'Assembler', 'Constructor']

# Import from a config file maybe?
base_URL = 'https://satisfactory.fandom.com/'

for building in buildings:
    building_page = requests.get(base_URL + building)
    building_soup = BeautifulSoup(building_page.content, 'html.parser')

    # Good enough for basic stuff, needs to be able to handle lists for refineries and packagers
    inputs = building_soup.find('b', string='Inputs')
    outputs = building_soup.find('b', string='Outputs')
    power = building_soup.find('b', string='Power Usage')

    if None in (inputs, outputs, power):
        continue
    
    # print(inputs.parent.parent.find('td').text.strip())
    # print(outputs.parent.parent.find('td').text.strip())
    # print(power.parent.parent.find('td').text.strip())

    test = Building(name=building, 
                input_num= inputs.parent.parent.find('td').text.strip(),
                output_num= inputs.parent.parent.find('td').text.strip(),
                base_power_use= inputs.parent.parent.find('td').text.strip(),
                overclock=0)

    print(test)


