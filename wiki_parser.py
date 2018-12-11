import requests
from bs4 import BeautifulSoup

url = "https://ru.wikipedia.org/wiki/Хармс,_Даниил_Иванович"

r = requests.get(url)

# with open('test.html', 'w', encoding='utf8') as output_file:
#   output_file.write(r.text)
# b = BeautifulSoup(r.text)
# writer_box = b.find('table', {'class': 'infobox vcard', 'data-name': "Писатель"})
# writer_box.find('th', {'class': 'plainlist'}, text='Дата рождения').parent.td.find('span', {'class': 'nowrap'})
#
# def get_table_field(soap, title):
#     return soap.find('th', {'class': 'plainlist'}, text=title).parent.td
#
# dates_field = get_table_field(writer_box, 'Дата рождения').find('span', {'class': 'nowrap'})
# dates = [date.text for date in dates_field.find_all('a')]
#
# print(dates)


def process_page(page_html):
    def get_table_field(writer_box, title):
        return writer_box.find('th', {'class': 'plainlist'}, text=title).parent.td

    result_dict = {}

    b = BeautifulSoup(page_html)
    writer_box = b.find('table', {'class': 'infobox vcard', 'data-name': "Писатель"})

    # year of birth
    dates_field = get_table_field(writer_box, 'Дата рождения').find('span', {'class': 'nowrap'})
    year_of_birth = int(dates_field.find_all('a')[1].text)
    result_dict['yesr_of_birth'] = year_of_birth


    # year of death
    dates_field = get_table_field(writer_box, 'Дата смерти').find('span', {'class': 'nowrap'})
    year_of_death = int(dates_field.find_all('a')[1].text)
    result_dict['year_of_death'] = year_of_death

    return result_dict


print(process_page(r.text))
