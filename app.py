try:
    from install import inst
except ModuleNotFoundError:
    pass

from loginsys import loginsys
from send_news import send_news
from fetch_news import get_news, get_config
from flask import Flask, url_for, redirect, request, jsonify, render_template, session, abort
import json

app = Flask(__name__)
##################################################################
#  REPLACE THIS WITH THE TEXT ON THE INSTALL PAGE!
app.secret_key = 'REPLACE THIS WITH THE TEXT ON THE INSTALL PAGE'
#  REPLACE THIS WITH THE TEXT ON THE INSTALL PAGE!
##################################################################

@app.route("/api/<codepath>/", methods=["GET"])
def getdata(codepath):
    configcode = get_config()
    for (configkey, code) in configcode:
        if codepath != code:
            abort(404)
    result = get_news()
    return jsonify(result)


@app.route("/login/", methods=["POST", "GET"])
def login():
    if "username" in session:
        if session["username"] == "admin":
            return redirect(url_for("dashboard"))
    global failed
    failed = False
    if request.method == "POST":
        username = request.form.get("username")
        if not username == "admin":
            failed = True
        else:
            req_passwd = request.form.get("password")
            passwd = loginsys()
            if req_passwd == passwd:
                session["username"] = "admin"
                return redirect(url_for("dashboard"))
            else:
                failed = True
    return render_template("login.html", failed=failed)

@app.route("/logout/")
def logout():
    if "username" in session:
        session.pop("username")
        return redirect(url_for("login"))


@app.route("/dashboard/", methods=["POST", "GET"])
def dashboard():
    if "username" in session:
        if session["username"] == "admin":
            global news1, news2, done, error
            if request.method == "POST":
                default_value = "No Data available..."
                result = send_news(request.form.get("notd", default_value), request.form.get("notw", default_value), request.form.get("code"))
                if result == "done":
                    done = True
                    error = False
                elif result == "codeerror":
                    done = False
                    error = True
                else:
                    return result
            else:
                done = False
                error = False
            result = get_news()
            codeconfig = get_config()
            if not type(result) is tuple:
                if result.startswith("Error"):
                    return result   
            if not type(result) is tuple:
                if result.startswith("Error"):
                    return result  
            for (news) in result:
                for (id, txt) in news:
                    if id == str(1):
                        news1 = txt
                    elif id == str(2):
                        news2 = txt
            for (configkey, code) in codeconfig:
                code = code
            return render_template("dashboard.html", news1=news1, news2=news2, done=done, code=code, error=error)
        else:
            session.pop("username")
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


@app.route("/install/", methods=["POST", "GET"])
def install():
    try:
        lol = inst()
        return lol
    except NameError:
        return redirect(url_for("post"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True, debug=False)
