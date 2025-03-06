class Rota:
    def __init__(self, filename):
        import json as _json

        self.json = _json

        try:
            with open(filename, "r") as file:
                self.data = self.json.load(file)
        except FileNotFoundError:
            with open(filename, "w") as file:
                self.data = {"workers": [], "lastRotated": None}
                self.json.dump(self.data, file, indent=4)

    def addWorker(self, workerName):
        self.data["workers"].append(workerName)

    def editWorker(self, workerName, newWorkerName):
        self.data["workers"][self.data["workers"].index(workerName)] = newWorkerName

    def deleteWorker(self, workerName):
        self.data["workers"].remove(workerName)

    def rotate(self, dateOfRotation):
        first = self.data["workers"][0]
        self.data["workers"].pop(0)
        self.data["workers"].append(first)

        self.data["lastRotated"] = dateOfRotation

    def get(self):
        return self.data["workers"], self.data["lastRotated"]

    def commit(self):
        with open("rota.json", "w") as file:
            self.json.dump(self.data, file, indent=4)
