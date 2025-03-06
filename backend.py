# Author: Garry Ivanovs
# Created: 06-03-2025
# Modified 06-03-2025


class Rota:
    def __init__(self, filename):  # Load the data from the file
        import json as _json

        self.json = _json

        try:
            with open(filename, "r") as file:
                self.data = self.json.load(file)
        except FileNotFoundError:
            with open(filename, "w") as file:
                self.data = {"workers": [], "lastRotated": None}
                self.json.dump(self.data, file, indent=4)

    def addWorker(self, workerName):  # Add a worker to the list
        if workerName in self.data["workers"]:
            raise FileExistsError
        else:
            self.data["workers"].append(workerName)

    def editWorker(self, workerName, newWorkerName):  # Edit a worker in the list
        try:
            self.data["workers"][self.data["workers"].index(workerName)] = newWorkerName
        except ValueError:
            raise FileNotFoundError

    def deleteWorker(self, workerName):  # Delete a worker from the list
        try:
            self.data["workers"].remove(workerName)
        except ValueError:
            raise FileNotFoundError

    def rotate(self, dateOfRotation ):  # Rotate the list of workers
        if dateOfRotation == None:
            raise ValueError
        first = self.data["workers"][0]
        self.data["workers"].pop(0)
        self.data["workers"].append(first)

        self.data["lastRotated"] = dateOfRotation

    def get(self):  # Get the list of workers and the date of the last rotation
        return self.data["workers"], self.data["lastRotated"]

    def commit(self):  # Commit the changes to the file
        with open("rota.json", "w") as file:
            self.json.dump(self.data, file, indent=4)
