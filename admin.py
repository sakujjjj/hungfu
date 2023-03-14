from flask import Flask, render_template, request, redirect, session, jsonify, Blueprint
import json
import requests
import mysql.connector
from mysql.connector import pooling
import traceback


admin_api = Blueprint("admin", __name__)


#   Connection pool
connection_pool = pooling.MySQLConnectionPool(
    pool_name="pynative_pool", pool_size=5, pool_reset_session=True, host='localhost',port = '5000', database='hungfu', user='root', password='1234')

# show all staff ask leave list
@admin_api.route("/api/admin", methods=["GET"])
def show_all_staff_ask_leave():
  try:
    connection_object = connection_pool.get_connection()
    mycursor = connection_object.cursor(buffered=True)
    phone_number = session["phone_number"]
    sql = "SELECT ask_leave.id, member.name, ask_leave_day, ask_leave_reason FROM hungfu.ask_leave INNER JOIN member on ask_leave.phone_number = member.phone_number;"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    print(results)
    list = []
    for i in results:
        list.append({
            "id": i[0],
            "name": i[1],
            "ask_leave_day": i[2],
            "ask_leave_reason": i[3]
        })

    print(list)
    return jsonify({"data": list}), 200    

  except:
    return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
  finally:
    if connection_object.is_connected():
        mycursor.close()
        connection_object.close()
        print("MySQL connection is closed")

#  show staff list 
@admin_api.route("/api/admin", methods=["PATCH"])
def show_all_staff():
  try:
    connection_object = connection_pool.get_connection()
    mycursor = connection_object.cursor(buffered=True)
    sql = "select * from member "
    mycursor.execute(sql)
    results = mycursor.fetchall()
    print("staff:", results)
    return jsonify({"data": results}), 200
  except:
    return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
  finally:
    if connection_object.is_connected():
        mycursor.close()
        connection_object.close()
        print("MySQL connection is closed")


# Sign up a new user API
@admin_api.route("/api/admin", methods=["POST"])
def create_user():
  try:
    connection_object = connection_pool.get_connection()
    mycursor = connection_object.cursor(buffered=True)
    json_data = request.get_json()
    print("json_data:", json_data)
    name = json_data["name"]
    password = json_data["password"]
    phone_number = json_data["phone_number"]
    email = json_data["email"]
    tsmc_id = json_data["tsmc_id"]
    sql = "select * from member where phone_number = %s"
    print("phone_number:", phone_number)
    mycursor.execute(sql, (phone_number,))
    results = mycursor.fetchone()
    print("results:", results)
    # 比對電話是否重複
    if results == None:
      sql = "insert into member (name, password, phone_number, email, tsmc_id) value (%s, %s, %s, %s, %s)"
      val = (name, password, phone_number, email, tsmc_id)
      mycursor.execute(sql, val)
      print(val)
      connection_object.commit()
      print(mycursor.rowcount, "record inserted.")
      return jsonify({"ok": True, "message": "電話"+phone_number+"註冊成功"}), 200
    else:
      return jsonify({"error": True, "message": "電話已被註冊"}), 400
  except:
    return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
  finally:
    if connection_object.is_connected():
        mycursor.close()
        connection_object.close()
        print("MySQL connection is closed")