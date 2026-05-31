import pickle
import json


def saveData(format,file,data):
    if format.lower()=='binary' or format.lower()=='bin':
        try:
            with open(file, mode="wb") as pickleFile:
                pickle.dump(data, pickleFile)
        except:
            with open(file, mode="wb") as jsonFile:
                pass

    elif format.lower()=='text' or format.lower()=='txt':
        try:
            with open(file, mode="w") as jsonFile:
                json.dump(data,jsonFile,indent=4)
        except:
            with open(file, mode="w") as jsonFile:
                pass
    else:
        print("Format must be either text or binary.")


def loadData(format,file):
    if format.lower()=='binary' or format.lower()=='bin':
        try:
            with open(file, mode="rb") as pickleFile:
                data = pickle.load(pickleFile)
                return data
        except:
            raise FileNotFoundError

    elif format.lower()=='text' or format.lower()=='txt':
        try:
            with open(file) as jsonFile:
                data=json.load(jsonFile)
                return data
        except:
            raise FileNotFoundError
    else:
        print("Format must be either text or binary.")


