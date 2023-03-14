from flask import Flask, render_template, request, redirect, session, jsonify, Blueprint
import json
import requests
import mysql.connector
from mysql.connector import pooling
import traceback


staff_api = Blueprint("staff", __name__)

#   Connection pool
connection_pool = pooling.MySQLConnectionPool(
    pool_name="pynative_pool", pool_size=5, pool_reset_session=True, host='localhost',port = '5000', database='hungfu', user='root', password='1234')


#   SHOW All Ask Leave List API
@staff_api.route("/api/staff", methods=["GET"])
def show_all_leave_list():
    try:
        connection_object = connection_pool.get_connection()
        mycursor = connection_object.cursor(buffered=True)
        phone_number = session["phone_number"]
        sql = "SELECT * FROM hungfu.ask_leave where phone_number = %s"
        mycursor.execute(sql, (phone_number,))
        results = mycursor.fetchall()
        print(results)
        list = []
        for i in results:
            list.append({
                "id": i[0],
                "phone_number": phone_number,
                "ask_leave_day": i[2],
                "ask_leave_reason": i[3]
            })

        # print(list)
        # print(type(list))
        # print(jsonify({"data": list}))
        # print({"data": list})
        return jsonify({"data": list}), 200

    except:
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
    finally:
        if connection_object.is_connected():
            mycursor.close()
            connection_object.close()
            print("MySQL connection is closed")


#   SHOW ONE Ask Leave List API
@staff_api.route("/api/staff/<int:ask_leave_id>", methods=["GET"])
def show_one_leave_list(ask_leave_id):
    try:
        connection_object = connection_pool.get_connection()
        mycursor = connection_object.cursor(buffered=True)

        sql = "SELECT * FROM hungfu.ask_leave where id = %s"
        mycursor.execute(sql, (ask_leave_id,))
        results = mycursor.fetchall()
        print(results)
        return jsonify({"data": results}), 200

    except:
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
    finally:
        if connection_object.is_connected():
            mycursor.close()
            connection_object.close()
            print("MySQL connection is closed")


#   create Ask Leave List API
@staff_api.route("/api/staff", methods=["POST"])
def create_ask_leave_list():
    try:
        connection_object = connection_pool.get_connection()
        mycursor = connection_object.cursor(buffered=True)
        json_data = request.get_json()
        print("json_data:", json_data)
        phone_number = json_data["phone_number"]
        ask_leave_day = json_data["ask_leave_day"]
        ask_leave_reason = json_data["ask_leave_reason"]
        print("ask_leave_day:", ask_leave_day)
        print(type(ask_leave_day))
        if ask_leave_day and ask_leave_reason != "":
            sql = "insert into ask_leave (phone_number, ask_leave_day, ask_leave_reason) value (%s, %s, %s)"
            val = (phone_number, ask_leave_day, ask_leave_reason)
            mycursor.execute(sql, val)
            connection_object.commit()
            return jsonify({"ok": True}), 200
        else:
            return jsonify({"error": True, "message": "日期或原因不得為空!"}), 400
    except:
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
    finally:
        if connection_object.is_connected():
            mycursor.close()
            connection_object.close()
            print("MySQL connection is closed")


# UPDATE ask leave list
@staff_api.route("/api/staff/<int:ask_leave_id>", methods=["PUT"])
def update_leave_list(ask_leave_id):
    try:
        connection_object = connection_pool.get_connection()
        mycursor = connection_object.cursor(buffered=True)
        json_data = request.get_json()
        print("json_data:", json_data)
        phone_number = json_data["phone_number"]
        ask_leave_day = json_data["ask_leave_day"]
        ask_leave_reason = json_data["ask_leave_reason"]
        sql = "UPDATE hungfu.ask_leave SET phone_number = %s, ask_leave_day= %s, ask_leave_reason = %s WHERE id = %s"
        mycursor.execute(sql, (phone_number, ask_leave_day,
                         ask_leave_reason, ask_leave_id))
        connection_object.commit()
        return jsonify({"ok": True}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": True, "message": "伺服器內部錯誤"}, 500
    # except:
    #     return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
    finally:
        if connection_object.is_connected():
            mycursor.close()
            connection_object.close()
            print("MySQL connection is closed")


#  DELETE ask leave list
@staff_api.route("/api/staff/<int:ask_leave_id>", methods=["DELETE"])
def delete_ask_leave_list(ask_leave_id):
    try:
        connection_object = connection_pool.get_connection()
        mycursor = connection_object.cursor(buffered=True)

        sql = "DELETE FROM hungfu.ask_leave where id = %s"

        mycursor.execute(sql, (ask_leave_id,))
        rowcount = mycursor.rowcount
        if rowcount > 0:
            connection_object.commit()
            return jsonify({"ok": True}), 200
        else:
            connection_object.rollback()
            return jsonify({"error": True, "message": "資料不存在"}), 404

    except Exception as e:
        print(f"An error occurred: {e}")
        connection_object.rollback()
        return {"error": True, "message": "伺服器內部錯誤"}, 500
    # except:
    #     return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
    finally:
        if connection_object.is_connected():
            mycursor.close()
            connection_object.close()
            print("MySQL connection is closed")
