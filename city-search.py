import os
import requests
import configparser
from xml.etree import ElementTree
import csv
import time


def city_lookup(zip_list):
    """
    Get list of City, State, ZIP when searching by ZIP code
    writes a comma-delimited file named city-st-zip.csv
    :param zip_list: ZIP codes as iterable
    :returns console output and comma-delimited file named city-st-zip.csv
    """
    results = []

    if not isinstance(zip_list, list):
        zip_list = [zip_list]

    for zipcode in zip_list:
        url_query = (('http://production.shippingapis.com/'
                      'ShippingAPITest.dll?API=CityStateLookup'
                      '&XML=<CityStateLookupRequest '
                      'USERID="{userid}"><ZipCode ID="0">'
                      '<Zip5>{zip5}</Zip5></ZipCode>'
                      '</CityStateLookupRequest>').format(userid=userid,
                                                          zip5=zipcode[:5]))

        response = requests.get(url_query)
        root = ElementTree.fromstring(response.content)

        for element in root.findall('*'):
            r = dict()
            try:
                r['city'] = element.find('City').text
                r['state'] = element.find('State').text
                r['zip-search'] = element.find('Zip5').text
            except AttributeError:
                r['city'] = "n/a"
                r['state'] = ""
                r['zip-search'] = zipcode

            results.append(r)

    with open('city-st-zip.csv', 'w', newline='') as s:
        csvw = csv.DictWriter(s, delimiter=',', fieldnames=['zip-search', 'city', 'state'], quoting=csv.QUOTE_ALL)
        csvw.writeheader()
        for row in results:
            print("{:5}: {} {}".format(row['zip-search'], row['city'], row['state']))
            csvw.writerow(row)


def init_api():
    global userid
    global password

    config = configparser.ConfigParser()
    config.read('config.ini')

    userid = config['api-credentials']['userid']
    password = config['api-credentials']['password']


def main():
    try:
        ans1 = int(input('Search from command input or file? (0 input / 1 file): '))

        if ans1 == 1:
            ans2 = input("Enter file name (this directory, NOT 'city-st-zip.csv'): ")
            try:
                with open(os.path.join(os.curdir, ans2), 'r') as r:
                    zip_list = r.read().splitlines()
                    city_lookup(zip_list)
            except FileNotFoundError:
                print("Invalid file name")
                time.sleep(3)

        elif ans1 == 0:
            zip_list = []
            ans3 = 99
            while ans3 != '0':
                ans3 = input('Enter 5-digit ZIP to search for, 0 when done: ')
                if ans3 == '0':
                    break
                zip_list.append(ans3)

            city_lookup(zip_list)

        else:
            print("Invalid Choice, try again")
            time.sleep(3)
            return

    except ValueError:
        print("Invalid Choice, try again")
        time.sleep(3)
        return


if __name__ == '__main__':
    init_api()
    main()
