#-*- coding: utf-8 -*-
import os
import json
import datetime


class Json:
    def __init__(self, *dbs):
        cwd = os.getcwd()
        if not os.path.exists(os.path.join(cwd, "dbs")):
            os.mkdir(os.path.join(cwd, "dbs"))
        self.cwd = os.path.join(cwd, "dbs")
        if dbs:
            for db in dbs:
                if not os.path.exists(os.path.join(self.cwd, str(db) + ".json")):
                    self.write({}, db)
        else:
            if not os.path.exists(os.path.join(self.cwd, str("db") + ".json")):
                self.write({}, "db")

    def read(self, filename="db"):
        with open(os.path.join(self.cwd,filename + ".json"), "r") as file:
            data = json.load(file)
        return data

    def write(self, data, filename="db"):
        with open(os.path.join(self.cwd,filename + ".json"), "w") as file:
            json.dump(data, file, indent=4)
        return data
    
    def delete(self, filename="db", *args): # (filename="db", *args):

        try:
            len_args = len(args)
            json_data = self.read(filename)
            tmp_data = json_data.copy()
            
            for i, arg in enumerate(args):
                print(i, arg)
                
                if i < len(args)-1:
                    tmp_data = tmp_data[arg]
                else:
                    del tmp_data[arg]

            return json_data
        except:
            return False


class Backup:
    def __init__(self, backup_path="", *args):
        if not os.path.exists(os.path.join(backup_path)):
            os.mkdir(backup_path)
        if not os.path.exists(os.path.join(backup_path, str(datetime.datetime.now().date()))):
            os.mkdir(os.path.join(backup_path, str(datetime.datetime.now().date())))
        backup_path = os.path.join(backup_path, str(datetime.datetime.now().date()))
        for arg in args:
            if os.path.exists(str(arg)):
                for f in os.listdir(arg):
                    print(arg, f)
                    file_data = self.read(os.path.join(arg, f))
                    self.write(file_data, os.path.join(backup_path, str(datetime.datetime.now()) + "__" + str(f)))
        
    def read(self, filepath):
        with open(filepath, "r") as file:
            data = file.read()
        return data
    
    def write(self, data, filepath):
        with open(filepath, "w") as file:
            file.write(data)
        return data



