from flask import Blueprint, make_response, request, render_template, jsonify, send_from_directory
from utils.captcha import Captcha
from io import BytesIO
from utils.sms import send_sms
from utils import restful
from exts import cache
from apps.front.forms import SendSMSForm
from werkzeug.utils import secure_filename
import string
import random
import config
import os

bp = Blueprint('common', __name__)


@bp.route('/captcha/')
def captcha():
    text, image = Captcha.gene_graph_captcha()
    text = text.lower()
    io = BytesIO()
    image.save(io, 'png')
    io.seek(0)
    resp = make_response(io.read())
    resp.content_type = 'image/png'
    cache.set(text, text, timeout=90)
    # print(text)
    return resp


@bp.route('/verify_captcha/<code>/')
def verify_captcha(code):
    # code = request.args.get('code')
    code = code.lower()
    flag = True if cache.get(code) else False
    return jsonify({'code': 200, 'verified': flag})


@bp.route('/sms_captcha/', methods=["POST"])
def sms_captcha():
    form = SendSMSForm(request.form)
    if form.validate():
        phone = form.phone.data
        captcha = "".join(random.sample(list(string.digits), 6))
        try:
            send_sms(phone, captcha)
            cache.set(phone, captcha)
            print(captcha)
            return restful.success('发送验证码成功')
        except:
            resp = send_sms(phone, captcha)
            print(captcha)
            return restful.server_error(resp['msg'])
    else:
        return restful.params_error(form.get_error())


@bp.route('/upload/', methods=['get', 'post'])
def upload():
    if request.method == 'GET':
        return render_template('common/upload.html')
    if not os.path.dirname(config.UPLOAD_FOLDER):
        os.mkdir(config.UPLOAD_FOLDER)
    f = request.files.get('myfile')
    if not f:
        return jsonify({'code': 400, 'message': 'no file'})
    filename = secure_filename(f.filename)
    filepath = os.path.join(config.UPLOAD_FOLDER, filename)
    f.save(filepath)
    return jsonify({'code': 200, 'message': 'upload successfully'})


@bp.route('/download/<path:filename>/')
def download(filename):
    filedir = config.UPLOAD_FOLDER
    return send_from_directory(filedir, filename, as_attachment=True)


@bp.route('/filelist/')
def filelist():
    files = {}
    for file in os.listdir(config.UPLOAD_FOLDER):
        fullpath = os.path.join(config.UPLOAD_FOLDER, file)
        size = round(os.path.getsize(fullpath)/1024/1024, 1) or 0.1
        files[file] = size
    return render_template('common/filelist.html', files=files)



