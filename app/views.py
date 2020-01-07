# -*- coding: utf-8 -*
import json

from flask import make_response

from app import app
import app.service.kof as KOF


@app.route('/eos/get_seed', methods=['GET'])
def get_seed():
    data = KOF.get_seed()
    result = make_response(json.dumps(data, ensure_ascii=False))
    return result
