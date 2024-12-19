import mariadb
import csv
import os
import time

TIME_COLUMN = "MeasuredTime"


class Exporter:

    def __init__(self):
        pass

    def connect_to_mariadb(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        # try:
        self.conn = mariadb.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        # except mariadb.Error as e:
        #     print(f"Error connecting to MariaDB database: {e}")

    def get_data(self, table, start="", end=""):
        cursor = self.conn.cursor()
        query = "select * from `"+table+"` where "+TIME_COLUMN+" between \""+start+"\" and \""+end+"\""
        try:
            cursor.execute(query)
            result = []
            for row in cursor:
                line = []
                for data in row:
                    line.append(data)
                result.append(row)
            return result
        except mariadb.Error as e:
            print(f"Error reading data:\n {e}\n{query}")
        finally:
            cursor.close()

    def export(self, ui, filename, location, data):
        ui.pushButton_2.setDisabled(True)
        ui.pushButton_2.setText("Exporting...")
        with open(location+filename, 'w', newline="") as csvfile:
            writer = csv.writer(csvfile)
            #writer.writerows(data)
            if(data):
                for row in data:
                    writer.writerow(row)
            else:
                print("no data")
        ui.pushButton_2.setDisabled(False)
        ui.pushButton_2.setText("Export")

    def get_file_name(self, filepath, filename):
        n = 0
        new_filepath = filepath+filename+".csv"
        while (self.path_exists(new_filepath)):
            n = n+1
            new_filepath = filepath+filename+"_"+str(n)+".csv"
        extra=""
        if(n!=0):
            extra = "_"+str(n)
        return filename+extra+".csv"
    
    def path_exists(self, path):
        return os.path.exists(path)