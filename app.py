from flask import Flask, render_template, request, redirect, session, jsonify
import json
import requests
import mysql.connector
from mysql.connector import pooling
import traceback

# 建立 Application 物件
app = Flask(__name__)
# app = Flask(__name__, static_folder="static", static_url_path="/")

app.secret_key = "any string but secret"

#   Connection pool

connection_pool = pooling.MySQLConnectionPool(
    pool_name="pynative_pool", pool_size=1, pool_reset_session=True, host='localhost', database='hungfu', user='root', password='1234')


# 首頁
@app.route("/")
def index():
    return render_template("index.html")


#   REST API
#   GET USER LOGIN_INFO API
@app.route("/api/user", methods=["GET"])
def get_user():
    print("phone_number:", session["phone_number"])
    print("name: ", session["name"])
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
                                "TSMC_ID": results[5],
                                "LEVEL": results[6]
                            }
                            })
        finally:
            if connection_object.is_connected():
                mycursor.close()
                connection_object.close()
                print("MySQL connection is closed")
    else:
        return jsonify({"data": None}), 200


# Sign up a new user API
@app.route("/api/user", methods=["POST"])
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


#   USER LOGIN API
@app.route("/api/user", methods=["PATCH"])
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
            # return redirect("/member/"), 200
            return jsonify({"ok": True}), 200

            # return render_template("member.html", name=session["name"])
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
@app.route("/api/user", methods=["DELETE"])
def logout():
    # json_data = request.get_json()
    # print(json_data)
    session["name"] = ""
    session["phone_number"] = ""
    return jsonify({"ok": True}), 200


# STAFF API
@app.route("/staff")
def user():
    return render_template("staff.html")


#   SHOW All Ask Leave List API
@app.route("/api/staff", methods=["GET"])
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
@app.route("/api/staff/<int:ask_leave_id>", methods=["GET"])
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
@app.route("/api/staff", methods=["POST"])
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
@app.route("/api/staff/<int:ask_leave_id>", methods=["PUT"])
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
@app.route("/api/staff/<int:ask_leave_id>", methods=["DELETE"])
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


#######################   WEB API    ###########################
# 註冊頁面
@app.route("/signup", methods=["POST"])
def signup():
    try:
        connection_object = connection_pool.get_connection()
        mycursor = connection_object.cursor(buffered=True)
        name = request.form["name"]
        password = request.form["password"]
        phone_number = request.form["phone_number"]
        email = request.form["email"]
        tsmc_id = request.form["tsmc_id"]

        sql = "select * from member where phone_number = %s"
        print(phone_number)
        mycursor.execute(sql, (phone_number,))

        results = mycursor.fetchall()
        print(results)

        # 比對電話是否重複
        if len(results) == 0:

            sql = "insert into member (name, password, phone_number, email, tsmc_id) value (%s, %s, %s, %s, %s)"
            val = (request.form["name"], request.form["password"],
                   request.form["phone_number"], request.form["email"], request.form["tsmc_id"])
            mycursor.execute(sql, val)
            print(val)
            connection_object.commit()
            print(mycursor.rowcount, "record inserted.")
            return render_template("success.html")
        else:
            return redirect("http://127.0.0.1:3000/error/?message=fail")
    finally:
        if connection_object.is_connected():
            mycursor.close()
            connection_object.close()
            print("MySQL connection is closed")


# 登入頁面
@app.route("/signin", methods=["POST"])
def signin():
    try:
        connection_object = connection_pool.get_connection()
        mycursor = connection_object.cursor(buffered=True)

        password = request.form["password"]
        phone_number = request.form["phone_number"]
        print("password:", password)
        # 比對資料庫帳密
        sql = "select * from member where phone_number = %s and password = %s"
        mycursor.execute(sql, (phone_number, password))
        results = mycursor.fetchone()
        print(results)

        # print(len(results))
        if results != None:
            session["state"] = "login"
            sql_name = "select name from member where phone_number = %s"
            mycursor.execute(sql_name, (phone_number,))
            member_name = results[1]
            print(member_name)

            # 將姓名存到session
            session["name"] = member_name
            return redirect("/member/")
        else:
            return redirect("http://127.0.0.1:3000/error/?message=keyerror")
    finally:
        if connection_object.is_connected():
            mycursor.close()
            connection_object.close()
            print("MySQL connection is closed")


# 登出系統
@app.route("/signout")
def signout():
    session["state"] = ""
    return render_template("index.html")


# 會員頁面
@app.route("/member/")
def member():
    if session["state"] == "login":
        name = session["name"]
        return render_template("member.html", name=name)

    else:
        return render_template("index.html")


# 失敗頁面
@app.route("/error/")
def error():
    # 抓到要求字串
    message = request.args.get("message")
    # 如果要求字串 = error 回傳"帳號 密碼錯誤"
    if message == "keyerror":
        return render_template("keyerror.html")
    elif message == "keynone":
        return render_template("keynone.html")
    # return "登入失敗"
    elif message == "fail":
        return render_template("fail.html")


# 會員 API
@app.route('/api/members', methods=['get'])
def get_member():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="hungfu"
    )
    mycursor = mydb.cursor()
    sql = "select json_object('id', id, 'name', name ) from member "

    mycursor.execute(sql)
    members = mycursor.fetchall()
    # members = ",".join('%s' % id for id in members)
    print(members)
    print(type(members))
    return jsonify({"members": members})
    # return {"members": members}
    # dic = {"members": eval(members)}
    # return dic


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
