#!.venv/bin/python3

# Made with ❤ by Garry
# 25/01/2024

from InquirerPy.separator import Separator
from InquirerPy import inquirer as inq
from tabulate import tabulate
import pickle, os

clear = lambda: os.system("cls" if os.name == "nt" else "clear")


def printError(message):
    print(len(message) * "-")
    print(message)
    print(len(message) * "-")
    print("")


class Rota:
    def __init__(self):
        self.rota = []

    def populate(self):
        self.rota = [
            {"name": "John Doe", "lastWorked": "2021-10-01"},
            {"name": "Jane Doe", "lastWorked": "2021-10-02"},
            {"name": "John Smith", "lastWorked": "2021-10-03"},
            {"name": "Jane Smith", "lastWorked": "2021-10-04"},
        ]

    def addWorker(self, name, lastWorked):
        self.rota.append({"name": name, "lastWorked": lastWorked})

    def removeWorker(self, name):
        for worker in self.rota:
            if worker["name"] == name:
                self.rota.remove(worker)
                break

    def get(self):
        return self.rota

    def save(self):
        with open("rota.bin", "wb") as file:
            pickle.dump(self.rota, file)

    def load(self):
        try:
            with open("rota.bin", "rb") as file:
                self.rota = pickle.load(file)
            return 0
        except FileNotFoundError:
            return 1

    def rotate(self):
        first = self.rota[0]
        self.rota.pop(0)
        self.rota.append(first)

    def editLastWorked(self, name, lastWorked):
        for worker in self.rota:
            if worker["name"] == name:
                worker["lastWorked"] = lastWorked
                break


class Menu:
    def __init__(self):
        self.rota = Rota()
        self.running = True
        self.unsavedChanges = False

        while self.running:
            if self.rota.get() == []:
                self.loaded = False
            else:
                self.loaded = True

            try:
                self.mainMenu()
            except Exception as e:
                if not self.loaded:
                    unloadedError = (
                        "CRITICAL: An unexpected error occurred, is the Rota loaded?"
                    )
                    printError(unloadedError)
                    input("Press enter to continue...")
                else:
                    criticalError = "CRITICAL: An unexpected error occurred, check the log for more information."
                    printError(criticalError)
                    with open("error.log", "w") as file:
                        file.write(str(e))
                    input("Press enter to continue...")

    def mainMenu(self):
        clear()

        if not self.loaded:
            unloadedMessage = "WARNING: Rota not loaded into memory."
            printError(unloadedMessage)

        if self.unsavedChanges:
            unsavedMessage = "WARNING: Unsaved changes detected."
            printError(unsavedMessage)

        selection = inq.select(
            message="Overtime Scheduler",
            choices=[
                "View Rota",
                "Edit Last Worked",
                "Rotate Rota",
                Separator(),
                "Save",
                "Load",
                Separator(),
                "Add Worker",
                "Remove Worker",
                Separator(),
                "Exit",
            ],
            qmark="📅",
        ).execute()

        match selection:
            case "View Rota":
                self.viewRota()
            case "Edit Last Worked":
                self.editLastWorked()
                self.unsavedChanges = True
            case "Rotate Rota":
                clear()
                self.rota.rotate()
                self.unsavedChanges = True
                print("Rotated Successfully.")
                input("\nPress enter to continue...")
            case "Save":
                clear()
                self.rota.save()
                self.unsavedChanges = False
                print("Saved Successfully.")
                input("\nPress enter to continue...")
            case "Load":
                clear()
                loadOverwrite = True

                if self.unsavedChanges:
                    loadOverwrite = inq.confirm(
                        message="WARNING: Unsaved changes detected, do you want to overwrite current Rota?",
                        default=False,
                        qmark="⚠️",
                        amark="✅",
                    ).execute()

                if loadOverwrite:
                    status = self.rota.load()
                    if status == 1:
                        printError("ERROR: Rota file not found.")
                        input("\nPress enter to continue...")
                    elif status == 0:
                        self.unsavedChanges = False
                        print("Loaded Successfully.")
                        input("\nPress enter to continue...")

            case "Add Worker":
                self.addWorker()
                self.unsavedChanges = True
            case "Remove Worker":
                self.removeWorker()
                self.unsavedChanges = True
            case "Exit":
                if self.unsavedChanges:
                    saveBeforeExit = inq.confirm(
                        message="WARNING: Unsaved changes detected, do you want to save before exiting?",
                        default=True,
                        qmark="⚠️",
                        amark="✅",
                    ).execute()
                    if saveBeforeExit:
                        self.rota.save()

                self.running = False
                clear()

    def viewRota(self):
        clear()
        if self.rota.get() == []:
            print("No workers in the Rota.")
            input("\nPress enter to continue...")
            return
        else:
            table = tabulate(self.rota.get(), headers="keys", tablefmt="github")
            print(table)
            input("\nPress enter to continue...")

    def editLastWorked(self):
        clear()
        names = [worker["name"] for worker in self.rota.get()]
        chosenWorker = inq.fuzzy(
            "Edit Last Worked", choices=names, qmark="✏️", amark="✅"
        ).execute()
        lastWorked = [
            worker["lastWorked"]
            for worker in self.rota.get()
            if worker["name"] == chosenWorker
        ][0]
        currentDate, currentMonth, currentYear = lastWorked.split("-")
        date = inq.number(
            "Enter the date:",
            min_allowed=1,
            max_allowed=31,
            default=int(currentDate),
            amark="✅",
        ).execute()
        month = inq.fuzzy(
            "Select the month:",
            choices=[
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ],
            default=currentMonth,
            amark="✅",
        ).execute()
        year = inq.number(
            "Enter the year:", min_allowed=2025, default=int(currentYear), amark="✅"
        ).execute()

        self.rota.editLastWorked(chosenWorker, f"{date}-{month[:3]}-{year}")
        print("Edited Successfully.")
        input("\nPress enter to continue...")

    def addWorker(self):
        pass

    def removeWorker(self):
        pass


if __name__ == "__main__":
    try:
        Menu()
    except KeyboardInterrupt:
        clear()
        exit()
