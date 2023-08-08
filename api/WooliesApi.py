"""
    Filename: WooliesApi.py
    Description: Contains callable Flask API functions
"""

# Initialization
import time
import pandas as pd
import json
import openai
import os
import re
import inflect
from collections import defaultdict
from decimal import Decimal
from typing import Dict, List, Tuple, Union
from flask import Flask, request, jsonify
from flask_cors import CORS
from woolies import *

# Setup
# GPT_MODEL = "gpt-4-0613"
GPT_MODEL = "gpt-3.5-turbo"
openai.api_key = os.getenv("OPENAI_API_KEY")
p = inflect.engine()
app = Flask(__name__)
CORS(app)

@app.route("/get_product", methods=["POST"])
def get_product_api():
    data = request.get_json()["requestBody"]
    prompt = data.get("prompt")
    filter = data.get("filter")
    top = data.get("top")
    bad_list = data.get("badList")
    if bad_list == [""]:
        bad_list = []
    print("Data: ", data)
    # Get the bad products that are not found
    if not filter:
        prompt = data["allItems"]
        bad_list = []
    all_res, buy_list, all_none = get_all_product(
        data=prompt, top=top, bad_list=bad_list
    )
    response = {
        "all_res": dict(all_res),
        "buy_list": buy_list,
        "all_none": dict(all_none),
        "filter": filter,
    }

    print(response)

    # Return the JSON response object
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)

# recipe = """
# 5 tbsp oil
# 2 eggs lightly beaten
# 3 tbsp cornflour/cornstarch
# 10 tbsp plain/all-purpose flour
# 2 tsp paprika
# 3 chicken breast fillets chopped into bite-size chunks
# """
# all_res, buy_list, all_none = get_all_product(data = recipe, top = 5, bad_list = bad_list)
# all_res_bad = get_bad_product(all_none)
# print(buy_list)
# print(len(buy_list))
# print(all_none)
