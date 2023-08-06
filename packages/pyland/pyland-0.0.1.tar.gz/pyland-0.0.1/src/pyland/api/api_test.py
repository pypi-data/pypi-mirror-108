# src/api/routes/authors.py
from flask import Blueprint
from flask import request
import sys

sys.path.append('..')
from utils.responses import response_with
from utils import responses as resp
from cases_execute import run_plan

test_routes = Blueprint("test_routes", __name__)


@test_routes.route('/run', methods=['POST'])
def test_cases():
    try:
        data = request.get_json()
        result = run_plan(data)
        return response_with(resp.SUCCESS_201, value={"result":
                                                          result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)
