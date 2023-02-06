from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector

# 建立 Application 物件
app = Flask(__name__)
# app = Flask(__name__, static_folder="static", static_url_path="/")

app.secret_key = "any string but secret"

# 首頁


@app.route("/")
def index():
    return render_template("index.html")


# 註冊頁面


@app.route("/signup", methods=["POST"])
def signup():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="hungfu"
    )

    name = request.form["name"]
    password = request.form["password"]
    phone_number = request.form["phone_number"]
    email = request.form["email"]
    tsmc_id = request.form["tsmc_id"]

    mycursor = mydb.cursor()

    sql = "select * from member where phone_number = %s"
    print(phone_number)
    mycursor.execute(sql, (phone_number,))

    # mycursor.execute(sql, (phone_number,))
    results = mycursor.fetchall()
    print(results)

    # 比對電話是否重複
    if len(results) == 0:
        # member_cursor = mydb.cursor()
        sql = "insert into member (name, password, phone_number, email, tsmc_id) value (%s, %s, %s, %s, %s)"
        val = (request.form["name"], request.form["password"],
               request.form["phone_number"], request.form["email"], request.form["tsmc_id"])
        mycursor.execute(sql, val)
        print(val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        return render_template("success.html")
    else:
        return redirect("http://127.0.0.1:3000/error/?message=fail")


# 登入頁面


@app.route("/signin", methods=["POST"])
def signin():

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="hungfu"
    )

    # name = request.form["name"]
    password = request.form["password"]
    phone_number = request.form["phone_number"]
    # email = request.form["email"]
    # tsmc_id = request.form["tsmc_id"]

    mycursor = mydb.cursor()

    # 比對資料庫帳密
    sql = "select * from member where phone_number='" + \
        phone_number+"' and password='"+password+"'"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    print(results)

    print(len(results))
    if len(results) == 1:
        session["state"] = "login"

        mycursor = mydb.cursor()
        sql_name = "select name from member where phone_number='"+phone_number+"'"
        mycursor.execute(sql_name)
        member_name = mycursor.fetchall()
        print(member_name)
        # 將陣列轉字串
        member_name = "".join('%s' % id for id in member_name)

        # 將姓名存到session
        session["value"] = member_name
        return redirect("/member/")
    else:
        return redirect("http://127.0.0.1:3000/error/?message=keyerror")

# 登出系統


@app.route("/signout")
def signout():
    session["state"] = ""
    return render_template("index.html")

# 會員頁面


@app.route("/member/")
def member():
    if session["state"] == "login":
        value = session["value"]
        return render_template("member.html", value=value)

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

    # name = request.form["name"]
    # password = request.form["password"]
    # phone_number = request.form["phone_number"]
    # email = request.form["email"]
    # tsmc_id = request.form["tsmc_id"]

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


@app.route("/api/user", methods=["POST"])
def create_user():
    User_db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="hungfu"
    )
    return "ok"


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
