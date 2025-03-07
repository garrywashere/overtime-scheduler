# Author: Garry Ivanovs
# Created: 06-03-2025
# Modified: 07-03-2025

from backend import Rota
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

FILENAME = "rota.json"


@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404


@app.route("/")  # Show the rota
def index():
    if request.method == "GET":
        rota = Rota(FILENAME)
        workers = rota.get()["workers"]
        lastRotated = rota.get()["lastRotated"]
        return render_template("index.html", workers=workers, lastRotated=lastRotated)
    else:
        return "Method not allowed", 405


@app.route("/addWorker", methods=["GET", "POST"])  # GET the form, POST the worker name
def addWorker():
    if request.method == "GET":  # Render addWorker.html
        return render_template("addWorker.html", title="Adding Worker...")
    elif (
        request.method == "POST"
    ):  # Recieve worker name from form, add worker to rota, commit changes
        rota = Rota(FILENAME)
        try:
            rota.addWorker(request.form["workerName"])
            rota.commit()
        except FileExistsError:
            return "Worker already exists", 409
        return redirect("/")
    else:
        return "Method not allowed", 405


@app.route(
    "/editWorker", methods=["GET", "POST"]
)  # GET the worker info, POST the new info
def editWorker():
    if (
        request.method == "GET"
    ):  # GET worker info from url argument, render editWorker.html with worker info
        try:
            workerName = request.args.get("workerName")

            rota = Rota(FILENAME)
            workers = rota.get()["workers"]

            found = False
            for worker in workers:
                if worker["name"] == workerName:
                    found = True
                    return render_template(
                        "editWorker.html",
                        title="Editing Worker...",
                        workerName=worker["name"],
                        lastRotated=worker["lastRotated"],
                    )
            if not found:
                return "Worker not found", 404
        except KeyError:
            return "Empty request", 400
    elif (
        request.method == "POST"
    ):  # Recieve new worker info from form, edit worker info, commit changes
        rota = Rota(FILENAME)
        workers = rota.get()["workers"]

        found = False
        for worker in workers:
            if worker["name"] == request.args.get("workerName"):
                rota.editWorker(
                    worker["name"],
                    request.form["newWorkerName"],
                    request.form["newLastRotated"],
                )
                rota.commit()
                found = True
        if not found:
            return "Worker not found", 404
        return redirect("/")
    else:
        return "Method not allowed", 405


@app.route("/deleteWorker", methods=["GET", "POST"])  # GET the confirmation
def deleteWorker():
    if request.method == "GET":
        try:
            workerName = request.args.get("workerName")

            rota = Rota(FILENAME)
            workers = rota.get()["workers"]

            found = False
            for worker in workers:
                if worker["name"] == workerName:
                    found = True
                    return render_template(
                        "deleteWorker.html",
                        title="Deleting Worker...",
                        workerName=worker["name"],
                    )
            else:
                return "Worker not found", 404
        except KeyError:
            return "Empty request", 400
    elif request.method == "POST":
        try:
            workerName = request.args.get("workerName")

            rota = Rota(FILENAME)
            try:
                rota.deleteWorker(request.args.get("workerName"))
                rota.commit()
            except FileNotFoundError:
                return "Worker not found", 404
            return redirect("/")
        except KeyError:
            return "Empty request", 400
    else:
        return "Method not allowed", 405


@app.route("/rotate", methods=["POST"])  # POST the date of rotation
def rotate():
    if request.method == "POST":
        rota = Rota(FILENAME)
        try:
            rota.rotate(request.form["dateOfRotation"])
            rota.commit()
        except ValueError:
            return "Invalid date", 400
        return redirect("/")
    else:
        return "Method not allowed", 405


if __name__ == "__main__":
    app.run(debug=True, port=8080)
