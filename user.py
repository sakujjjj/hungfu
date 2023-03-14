from flask import Flask, render_template, request, redirect, session, jsonify, Blueprint
import json
import requests
import mysql.connector
from mysql.connector import pooling
import traceback


user_api = Blueprint("user", __name__)


#   Connection pool
connection_pool = pooling.MySQLConnectionPool(
    pool_name="pynative_pool", pool_size=5, pool_reset_session=True, host='localhost',port = '5000', database='hungfu', user='root', password='1234')


#   GET USER LOGIN_INFO API
@user_api.route("/api/user/", methods=["GET"])
def get_user():
    # print("phone_number:", session["phone_number"])
    # print("name: ", session["name"])
    if session["phone_number"] != "":
        try:
            connection_object = connection_pool.get_connection()
            mycursor = connection_object.cursor(buffered=True)

            sql = "select * from member where phone_number = %s"
            mycursor.execute(sql, (session["phone_number"],))
            results = mycursor.fetchone()
            print("GET_results:", results)

            return jsonify({"data":
                            {
                                "id": results[0],
                                "name": session["name"],
                                "phone_number": results[3],
                                "email": results[4],
                                "tsmc_id": results[5],
                                "level": results[6]
                            }
                            })
        finally:
            if connection_object.is_connected():
                mycursor.close()
                connection_object.close()
                print("MySQL connection is closed")
    else:
        return jsonify({"data": None}), 200


#   USER LOGIN API
@user_api.route("/api/user", methods=["PATCH"])
def login_user():
    try:
        connection_object = connection_pool.get_connection()
        mycursor = connection_object.cursor(buffered=True)

        print("request:", request.get_json())
        json_data = request.get_json()
        phone_number = json_data["phone_number"]
        password = json_data["password"]
        print("phone_number:", phone_number, "password", password)
        # 比對資料庫帳密
        sql = "select * from member where phone_number = %s and password = %s"
        mycursor.execute(sql, (phone_number, password))
        results = mycursor.fetchone()
        print("PATCH_results:", results)

        if results != None:
            sql = "select name from member where phone_number = %s"
            mycursor.execute(sql, (phone_number,))
            session["name"] = results[1]
            session["phone_number"] = results[3]
            print(session["name"])
            
            return jsonify({"ok": True, "level":results[6]}), 200

            
        else:
            return jsonify({"error": True, "message": "登入失敗!帳號或密碼錯誤"}), 400
    except:
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
    finally:
        if connection_object.is_connected():
            mycursor.close()
            connection_object.close()
            print("MySQL connection is closed")


#  USER LOGOUT API
@user_api.route("/api/user", methods=["DELETE"])
def logout():
    # json_data = request.get_json()
    # print(json_data)
    session["name"] = ""
    session["phone_number"] = ""
    return jsonify({"ok": True}), 200
