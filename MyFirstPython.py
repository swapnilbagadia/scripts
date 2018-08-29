#! /usr/bin/env python
import base64
import MySQLdb
import sys
import csv
from xlsxwriter.workbook import Workbook

# https://example.com/test/?lksrc=c3JjPU1PQklTWSZ0eXBlPWVjb20mcmVmaWQ9TU9CSVNZMDAx#!/home


print("Hey, What do you want to do - generate a leadSrc Url or decode one?");
menu_input = int(raw_input('Please press 1 for generating encoded merchant url, 2 for checking the validity of the entered URL, 3 for mysql to excel (menu_input) : '));
if menu_input == 1:
	src = raw_input('Please enter lead source value (src) : ');
	print("Generating URL with values")
	print("src="+src)
	print("type=ecom")
	print("refId="+src+"001")
	print("-----")
	toEncodeString="src="+src+"&type=ecom&refid="+src+"001";
	print toEncodeString
	encoded = base64.b64encode(toEncodeString)
	url = "https://example.com/test/?lksrc="+encoded+"#!/home"
	print ("Please forward this url to Merchant \n\n")
	print url
	print ("")
elif menu_input == 2:
	url = raw_input('Please enter generated url: ');
	data = url.split("?");
	for temp in data:
    		if "lksrc" in temp:
			lksrc = temp.split("#");
			encoded = lksrc[0].split("=");
			decoded = base64.b64decode(encoded[1]);
			print decoded
elif menu_input == 3:
	connection = MySQLdb.connect (host = "localhost", user = "root", passwd = "root", db = "springbootdb")
	cursor = connection.cursor ();
	# prepare a cursor object using cursor() method
	cursor = connection.cursor ()
	# execute the SQL query usig execute() method.
	cursor.execute ("select * from shipmentRouteEvent")
	# fetch all of the rows from the query
	data = cursor.fetchall ()
	# close the cursor object
	cursor.close ()

	cursor = connection.cursor()
	cursor.execute("select Column_name from Information_schema.columns where Table_name like 'shipmentRouteEvent'")

	fields = cursor.fetchall()
	cursor.close()

	# close the connection
	connection.close ()

	#Enter data in excel
	workbook = Workbook('outfile.xlsx')
	sheet = workbook.add_worksheet()
	
	#Column Names ~ Could be made bold, Also auto generated from field names gotten above
	sheet.write('A1','Col 1')
	sheet.write('B1','Col 2')
	sheet.write('C1','Col 3')

	#Actual Data
	for r, row in enumerate(data):
    		for c, col in enumerate(row):
        		sheet.write(r+1, c, col)

	#Workbook Close
	workbook.close()

	#Enter data in csv
	with open('outfile.csv','w') as f:
        	writer = csv.writer(f)
    		for row in data:
        		writer.writerow(row)

	#Mail Files ~ TODO

	
else:
	print ('Wrong Entry!!')
# Exit
sys.exit()
