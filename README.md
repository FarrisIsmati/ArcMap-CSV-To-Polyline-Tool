# ArcMap-CSV-To-Polyline-Tool

  The CSV to Polyline tool takes CSV files formatted with a header, two proper latitude and longitude fields, and a field that names each
specific track. This tool allows you to take CSV files and converts them into a useable shapefile containing polylines for immediate use.
The way to convert CSV data into polylines without the tool requires a few steps. First you need to convert your CSV file into XY data.
After converting the CSV file into XY data you can then put that XY data into the XY to line tool; the tool only allows you to connect
two points together. The CSV to Polyline tool allows you to take full sets of data and connects them together as long as they are in a
logical order. Additionally multiple polylines can be created with the tool as long as each set of latitude and longitude points have
their own distinct feature name.

Created: 4/19/2016
