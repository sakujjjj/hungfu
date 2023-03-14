from flask import Flask, render_template, request, redirect, session, jsonify, Blueprint
import json
import requests
import mysql.connector
from mysql.connector import pooling
import traceback
from user import user_api
from staff import staff_api
from admin import admin_api


# 建立 Application 物件
app = Flask(__name__, static_folder="/", template_folder='templates')
# flask Blueprint
app.register_blueprint(user_api)
app.register_blueprint(staff_api)
app.register_blueprint(admin_api)


app.secret_key = "any string but secret"


#   Connection pool
connection_pool = pooling.MySQLConnectionPool(
    pool_name="pynative_pool", pool_size=5, pool_reset_session=True, host='localhost',port = '5000', database='hungfu', user='root', password='1234')


# Pages
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/user/")
def user():
    return render_template("user.html")



@app.route("/user/admin/")
def admin():
    return render_template("admin.html")

@app.route("/user/staff/")
def staff():
    return render_template("staff.html")


@app.route("/contact/")
def contact():
    return render_template("contact.html")


@app.route("/faq/")
def faq():
    return render_template("faq.html")



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
