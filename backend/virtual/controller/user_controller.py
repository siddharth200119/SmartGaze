from app import app
from model.user_model import user_model
from flask import request

obj = user_model()

@app.route("/user/getall", methods=["GET"])
def user_getall_controller():
    return obj.user_getall_model()


@app.route("/user/addone", methods=["POST"])
def user_addone_controller():
    return obj.user_addone_model(request.form)


@app.route("/user/update", methods=["PUT"])
def user_update_controller():
    return obj.user_update_model(request.form)


@app.route("/user/delete/<TID>", methods=["DELETE"])
def user_delete_controller(TID):
    return obj.user_delete_model(TID)

@app.route("/user/delete", methods=["POST"])
def user_delete2_controller():
    return obj.user_delete2_model(request.form)
