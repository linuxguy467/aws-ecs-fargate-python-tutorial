from flask import Flask, render_template, redirect, url_for, request, jsonify
import boto3
import os
import datetime

app = Flask(__name__)

os.environ["AWS_ENDPOINT_URL"] = "http://localhost:4566"
dynamodb = boto3.client("dynamodb")


def getLeaveDays():
    response = dynamodb.scan(TableName="leavedays")
    items = response.get("Items", [])

    values = [
        {
            key: value.get("S") if value.get("S") else value.get("N")
            for key, value in item.items()
        }
        for item in items
    ]

    return values


def addLeaveDay(name, from_date, to_date):
    leave_id = str(int(datetime.datetime.now().timestamp()))
    item = {
        "leave_id": {"N": leave_id},
        "name": {"S": name},
        "from_date": {"S": str(from_date)},
        "to_date": {"S": str(to_date)},
    }
    dynamodb.put_item(TableName="leavedays", Item=item)


# Generate a function named deleteLeaveDay that takes leave_id as a parameter
# This function will delete a leave day item from the dynamodb table
# leavedays by the leave_id
def deleteLeaveDay(leave_id):
    dynamodb.delete_item(TableName="leavedays", Key={"leave_id": {"N": str(leave_id)}})


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        from_date = request.form["from_date"]
        to_date = request.form["to_date"]
        name = request.form["user_name"]

        addLeaveDay(name, from_date, to_date)

        return redirect(url_for("index"))

    leave_days = getLeaveDays()
    return render_template("index.html", leave_days=leave_days)


@app.route("/<int:leave_id>", methods=["DELETE"])
def delete_leave(leave_id):
    deleteLeaveDay(leave_id)
    return jsonify({"success": True})


@app.route("/health", methods=["GET"])
def health_check():
    return "Healthy"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
