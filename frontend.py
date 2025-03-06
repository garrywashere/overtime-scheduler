# Author: Garry Ivanovs
# Created: 06-03-2025
# Modified: 06-03-2025

from backend import Rota
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")  # Show the rota
def index():
    render_template("index.html")


@app.route("/addWorker", methods=["GET", "POST"])  # GET the form, POST the worker name
def addWorker():
    if request.method == "GET":  # Render addWorker.html
        return render_template("addWorker.html")
    elif (
        request.method == "POST"
    ):  # Recieve worker name from form, add worker to rota, commit changes
        rota = Rota("rota.json")
        rota.addWorker(request.form["workerName"])
        rota.commit()
        return redirect("/")
    else:
        return "Method not allowed", 405


@app.route(
    "/editWorker/<workerName>", methods=["GET", "POST"]
)  # GET the worker info, POST the new info
def editWorker():
    if (
        request.method == "GET"
    ):  # GET worker info from url argument, render editWorker.html with worker info
        try:
            workerName = request.args.get("workerName")

            rota = Rota("rota.json")
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
        pass
    else:
        return "Method not allowed", 405


@app.route(
    "/deleteWorker", methods=["GET", "POST"]
)  # GET the confirmation, POST the worker name
def deleteWorker():
    pass


@app.route("/rotate", methods=["POST"])  # POST the date of rotation
def rotate():
    pass
