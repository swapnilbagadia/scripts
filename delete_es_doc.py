import csv
import requests

with open('Test.csv') as filestream:
    for line in filestream:
        currentline = line.split(",")
        print(currentline[0])
        url="https://test.com/test/test/{0}".format(currentline[0])
        print(url)
        print(requests.delete(url))
