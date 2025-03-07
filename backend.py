# Author: Garry Ivanovs
# Created: 06-03-2025
# Modified 07-03-2025


class Rota:
    def __init__(self, filename):  # Load the data from the file
        import json as _json

        self.json = _json
        self.filename = filename

        try:
            with open(filename, "r") as file:
                self.data = self.json.load(file)
        except FileNotFoundError:
            with open(filename, "w") as file:
                self.data = {"workers": [], "lastRotated": None}
                self.json.dump(self.data, file, indent=4)

    def addWorker(self, workerName):  # Add a worker to the list
        for worker in self.data["workers"]:
            if worker["name"] == workerName:
                raise FileExistsError
        self.data["workers"].append({"name": workerName, "lastRotated": None})

    def editWorker(
        self, workerName, newWorkerName, lastRotated
    ):  # Edit a worker in the list
        found = False
        for worker in self.data["workers"]:
            if worker["name"] == workerName:
                worker["name"] = newWorkerName
                if lastRotated:
                    worker["lastRotated"] = lastRotated
                found = True

        if not found:
            raise FileNotFoundError

    def deleteWorker(self, workerName):  # Delete a worker from the list
        found = False
        for worker in self.data["workers"]:
            if worker["name"] == workerName:
                self.data["workers"].remove(worker)
                found = True

        if not found:
            raise FileNotFoundError

    def rotate(self, dateOfRotation):  # Rotate the list of workers
        if dateOfRotation == None:
            raise ValueError

        first = self.data["workers"][0]
        first["lastRotated"] = dateOfRotation

        self.data["workers"].pop(0)
        self.data["workers"].append(first)

        self.data["lastRotated"] = dateOfRotation

    def get(self):  # Get the list of workers and the date of the last rotation
        return self.data

    def commit(self):  # Commit the changes to the file
        with open(self.filename, "w") as file:
            self.json.dump(self.data, file, indent=4)
