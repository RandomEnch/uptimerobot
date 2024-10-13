import httpx

from loguru import logger
from flask import Flask, request, jsonify

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7',
    'Cache-Control': 'no-cache',
}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response


@app.route('/', methods=['GET', 'POST'])
def index():
    logger.info(f"{request.method} {request.path}")
    return jsonify({"message": "Method Not Allowed"})


@app.route('/v2/<path:endpoint>', methods=['GET', 'POST'])
def post_api(endpoint):
    url = f"https://api.uptimerobot.com/v2/{endpoint}"
    if request.method == 'GET':
        resp = httpx.get(url, params=request.args, headers=headers, timeout=10)
    else:
        resp = httpx.post(url, data=request.json, headers=headers, timeout=10)

    if resp.status_code == 200:
        return jsonify(resp.json())
    else:
        return jsonify({"message": "Error", "status_code": resp.status_code})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
