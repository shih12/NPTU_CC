from flask import Flask, render_template, request, jsonify, make_response, json, send_from_directory, redirect, url_for
import pymongo

myclient = pymongo.MongoClient('mongodb://%s:%s/' % (
        'rs1',    # database addr
        '27041'         # database port
    ))
mydb = myclient["Content"]
mycol = mydb["Info"]

# setup flask app
app = Flask(__name__)
@app.route('/')
@app.route('/readInfo', methods=['GET'])
def readInfo():
    x = mycol.find()
    if x:
      return render_template('index.html',data = x)
    else:
      return 'not found'

@app.route('/update', methods=['GET'])
def edit():
    x = mycol.find()
    if x:
      return render_template('update.html',data = x)
    else:
      return 'not found'

@app.route('/update', methods=['POST'])
def Do_editInfo():
    url = request.form["url"]
    size = request.form["size"]
    remark = request.form["remark"]
    x = mycol.update({"url":url},{"$set":{"size":size, "remark": remark}})
    return "Success"


@app.route('/delete', methods=['GET'])
def deleteInfo():
    x = mycol.find()
    if x:
      return render_template('delete.html',data = x)
    else:
      return 'not found'

@app.route('/deleteInfo', methods=['POST'])
def Do_deleteInfo():
    url = request.form["url"]

    x = mycol.delete_one({"url":url})
    return "Success"

@app.route('/addInfo', methods=['GET'])
def addInfo():
    return render_template("addInfo.html")

@app.route('/addInfo', methods=['POST'])
def Do_addInfo():
    url = request.form["url"]
    size = request.form["size"]
    remark = request.form["remark"]

    x = mycol.insert_one({"url":url, "size":size, "remark": remark})
    return "Success"

app.run(host='0.0.0.0', port=5003)