#Converts CSV Files to Polylines
import arcpy, csv, operator, numpy

#Parses CSV Data
#Sorts polyline track names, and stores data into a dict
class CSV_File():
    def __init__(self, file_name):
        self.read_file = open(file_name, 'r')
        self.csv_file = csv.reader(self.read_file)
        self.header = next(self.csv_file)

    def Parse_Data(self, x_coor, y_coor, track_name):
        self.sorted_csv = sorted(self.csv_file, key=operator.itemgetter(3))
        
        track_names = []
        track_dict = {}
        track_coordinates = {}

        coord_x = x_coor
        coord_y = y_coor
        
        #Find track name within header
        for i in range(len(self.header)):
            if track_name == self.header[i]:
                track_name_pos = i
        
        #Find coordinates within header
        for i in range(len(self.header)):
            if coord_x == self.header[i]:
                coord_x_pos = i
            if coord_y == self.header[i]:
                coord_y_pos = i 
        
        #Sort CSV file
        for sort in self.sorted_csv:
            if sort[0] not in self.header:
                if sort[track_name_pos] not in track_names:
                    track_names.append(sort[track_name_pos])
        
        #Get unique track names
        for track in track_names:     
            for sort in self.sorted_csv:
                if sort[track_name_pos] == track:
                    track_coordinates[float(sort[coord_x_pos])] = float(sort[coord_y_pos])
            track_dict[track] = track_coordinates
            track_coordinates = {}
            
        return (track_names, track_dict)

#Takes parsed CSV data and creates a polyline
class Polyline():
    def __init__(self):
        self.spatialRef = arcpy.SpatialReference(3785)

    def Create_Polyline(self, name, location, csv_features):
        polyline_features = []
        array_points = []
        #Creates feature class which will store polyline information
        arcpy.CreateFeatureclass_management(location, name, 'POLYLINE','','','', self.spatialRef)
        arcpy.AddField_management(location + '\\' + name, "target_id", "TEXT")
        cursor = arcpy.da.InsertCursor(location + '\\' + name, ["SHAPE@", "target_id"])

        for track in csv_data[0]:
            '''Gets Key value Pairs of Each animal'''
            for key, value in csv_data[1][track].iteritems():
                temp = [key, value]
                #create an array of key an value pairs of the animal instance
                array_points.append(temp)
            #Append the array of coordinates of the instance animal
            polyline_features.append(arcpy.Polyline(
                    arcpy.Array([arcpy.Point(*points) for points in array_points])))
            cursor.insertRow([arcpy.Polyline(
                    arcpy.Array([arcpy.Point(*points) for points in array_points])),track])
            #Reset polyline features/points for next track
            polyline_features = []
            array_points = []

        del cursor
        
#ArcScript Input Parameters
input_file = arcpy.GetParameterAsText(0)
tracks = arcpy.GetParameterAsText(1)
x_coordinates = arcpy.GetParameterAsText(2)
y_coordinates = arcpy.GetParameterAsText(3)
folder_location = arcpy.GetParameterAsText(4)
file_name = arcpy.GetParameterAsText(5)

new_file = CSV_File(input_file)
csv_data = new_file.Parse_Data(x_coordinates, y_coordinates, tracks)
polyline1 = Polyline()
polyline1.Create_Polyline(file_name, folder_location, csv_data)
