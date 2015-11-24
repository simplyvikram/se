import io
import csv
import json

import flask
from flask import request, render_template
from flask.blueprints import Blueprint

from werkzeug.utils import secure_filename

from manager import ExpenseManager

blueprint = Blueprint('basic_endoints', __name__, url_prefix='')

def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ['csv']

@blueprint.route('/upload', methods=['GET', 'POST'])
def upload_csv():

    if request.method == 'POST':\

        f = request.files['file']
        if not f or not _allowed_file(f.filename):
            return 'Bad File'

        filename = secure_filename(f.filename)
        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)

        expense_file, expenses = ExpenseManager.parse_csv_input(
            csv_input, filename
        )

        ExpenseManager.save_expenses(expense_file, expenses)

        expenses = map(lambda e: str(e), expenses)
        return format_json(expenses)

    return render_template('upload.html')


@blueprint.route('/all', methods=['GET'])
def all():
    return render_template('expense_files.html')


@blueprint.route('/expense_files/all', methods=['GET'])
def all_expense_files():

    expense_files = ExpenseManager.expense_files()

    resp = []
    for ef in expense_files:
        resp.append({
            'filename': ef.filename,
            'id': ef.id,
            'creation_timestamp': str(ef.utc_datetime)
        })

    return format_json(resp)

@blueprint.route('/expenses/calculage/<int:expense_file_id>', methods=['GET'])
def calculate_expenses(expense_file_id):

    monthly_expense_dict = ExpenseManager.monthly_expense_dict(expense_file_id)

    # This contains the monthly expense in decimal, convert to float'
    monthly_default_dict = {
        k: float(v) for k,v in monthly_expense_dict.iteritems()
    }

    return format_json(monthly_default_dict)

# class CustomJSONEncoder(flask.json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, Expense) or isinstance(o, ExpenseFile):
#             return o.__dict__
#         else:
#             return flask.json.JSONEncoder.default(self, o)


def format_json(resp):
    return flask.Response(json.dumps(resp), mimetype='application/json')











