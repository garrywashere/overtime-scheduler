# Author: Garry Ivanovs
# Created: 06-03-2025
# Modified: 06-03-2025

from backend import Rota
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

FILENAME = "rota.json"

@app.route("/")  # Show the rota
def index():
    if request.method == "GET":
        rota = Rota(FILENAME)
        workers, lastRotated = rota.get()
        return render_template("index.html", workers=workers, lastRotated=lastRotated)
    else:
        return "Method not allowed", 405


@app.route("/addWorker", methods=["GET", "POST"])  # GET the form, POST the worker name
def addWorker():
    if request.method == "GET":  # Render addWorker.html
        return render_template("addWorker.html")
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
            workers, _ = rota.get()

            if workerName in workers:
                return render_template("editWorker.html", workerName=workerName)
            else:
                return "Worker not found", 404
        except KeyError:
            return "Worker not found", 404
    elif (
        request.method == "POST"
    ):  # Recieve new worker info from form, edit worker info, commit changes
        rota = Rota(FILENAME)
        try:
            rota.editWorker(request.args.get("workerName"), request.form["newWorkerName"])
            rota.commit()
        except FileNotFoundError:
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
            workers, _ = rota.get()

            if workerName in workers:
                return render_template("deleteWorker.html", workerName=workerName)
            else:
                return "Worker not found", 404
        except KeyError:
            return "Worker not found", 404
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
            return "Worker not found", 404
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