from flask import session, redirect, url_for, request, render_template, jsonify
from controller.modules.user import user_blu
from controller.utils.camera import VideoCamera
from controller.utils.Mysql import Mysql
from controller.utils.controlmp import ControlMotor
from controller.utils.Face import Face
import time
import os

# 登录
@user_blu.route("/login", methods=["GET", "POST"])
def login():
    username = session.get("username")

    if username:
        return redirect(url_for("home.index"))
    if request.method == "GET":
        return render_template("login.html")
    # 获取参数
    username = request.form.get("username")
    password = request.form.get("password")
    # 校验参数
    if not all([username, password]):
        return render_template("login.html", errmsg="请完整填写账号和密码")

    # 校验对应的管理员用户数据
    if username == "admin" and password == "admin":
        # 验证通过
        session["username"] = username
        return redirect(url_for("home.index"))

    return render_template("login.html", errmsg="用户名或密码错误")

# 退出登录
@user_blu.route("/logout")
def logout():
    # 删除session数据
    session.pop("username", None)
    # 返回登录页面
    return redirect(url_for("user.login"))

# 门禁记录
@user_blu.route('/record')
def get_record():
    username = session.get("username")
    if username:
        db = Mysql()
        data = db.query()
        return render_template('record.html',recordlist=data)
    return redirect(url_for("user.login"))
    
#开关门
@user_blu.route('/ocdoor')
def ocdoor():
    username = session.get("username")
    if username:
        control = ControlMotor()
        control.forward(0.002,300)
        time.sleep(3)
        control.backward(0.002,300)
        return jsonify({"msg": "开门成功"}) 
    return redirect(url_for("user.login"))

#人员管理
@user_blu.route ('/permang')
def permang():
    username = session.get("username")
    if username:
        facelist = []
        facedict = dict()
        face = Face()
        face_tokens = face.detfaceset()
        for facetoken in face_tokens:
            user_id = face.detface(facetoken)
            facedict['facetoken'] = facetoken
            facedict['user_id'] = user_id
            facelist.append(facedict.copy())
        return render_template('permang.html',facelist=facelist)
    return redirect(url_for("user.login"))

#删除人脸信息
@user_blu.route ('/removeface')
def removeface():
    username = session.get("username")
    if username:
        face = Face()
        facetoken = request.args.get("facetoken")
        face_removed = face.removeface(facetoken)
        if face_removed == 1:
            return '<script>alert("删除成功");location.href="/permang";</script>'
        else:
            return '<script>alert("删除失败");location.href="/permang";</script>'
    return redirect(url_for("user.login"))
    
#添加成员
@user_blu.route ('/addface',methods=['GET', 'POST'])
def addface():
    username = session.get("username")
    if username:
        if request.method == 'POST':
            user_id = request.form.get("user")
            image_file = request.files.get('image')
            if not all([user_id, image_file]):
                return '<script>alert("添加失败，请完整填写姓名和上传照片！");location.href="/permang";</script>'
            image_name = image_file.filename
            mt_path = '/home/pi/monitors/faces/'
            facepath = os.path.join(mt_path,image_name)
            image_file.save(facepath)
            face = Face()
            facetoken = face.detect(facepath)
            if facetoken:
                userid = face.addface(facetoken,user_id)
                if userid == user_id:
                    return '<script>alert("添加成功！");location.href="/permang";</script>'
                return '<script>alert("添加失败，请重新添加！");location.href="/permang";</script>'
            return '<script>alert("添加失败，未检测到人脸，请重新添加！");location.href="/permang";</script>'
        return redirect(url_for("user.permang"))
    return redirect(url_for("user.login"))
    

