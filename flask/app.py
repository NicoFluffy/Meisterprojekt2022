from flask import Flask, Blueprint, render_template, flash, redirect, url_for, request, session, Response, jsonify, logging , send_from_directory, send_file
import random, datetime, os, sys
import HTML_Forms, database

app = Flask(__name__)
app.secret_key = "NicosProject@_{}".format(random.randint(1000000, 9999999))
json_db = database.Json()

# ----------------------------------------------------------------------------------------- #
@app.route("/")
@app.route("/home")
def home():
    json_data = json_db.read()
    return render_template("home.html", json_data=json_data)
# ----------------------------------------------------------------------------------------- #
@app.route("/admin", methods=["GET", "POST"])
def admin():
    form = HTML_Forms.Form(request.form)
    json_data = json_db.read()
    if request.method == "POST":
        name = form.string_input_name.data
        command = form.string_input_command.data
        command_type = form.select_input_type.data
        if "rs232" not in json_data:
            json_data["rs232"] = {}
        tmp_index = len(json_data["rs232"])
        while str(tmp_index) in json_data["rs232"]:
            tmp_index += 1
        json_data["rs232"][tmp_index] = {"name": name, "command": command, "type": command_type}
        json_db.write(json_data)
        flash("Du hast ein neues Kommando hinzugefügt!", "success")
        return redirect(url_for("home"))
    return render_template("admin.html", form=form, json_data=json_data)
# ----------------------------------------------------------------------------------------- #
@app.route("/send_command/<string:command_type>/<string:command>")
def send_command(command, command_type):
    json_data = json_db.read()
    flash("Info: Type: {}, Command: {}".format(command_type, command), "info")
    return redirect(url_for("home"))
# ----------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------- #
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)