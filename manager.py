
from re import sub
from decimal import Decimal
from datetime import datetime
from collections import defaultdict

from database import db_session
from models import Expense, ExpenseFile

class ExpenseManager(object):

    @staticmethod
    def save_expenses(expense_file, expenses):

        try:
            db_session.add(expense_file)
            db_session.flush()
            for expense in expenses:
                expense.expense_file_id = expense_file.id
                db_session.add(expense)

            db_session.commit()
        except:
            db_session.rollback()

    @staticmethod
    def parse_csv_input(csv_input, filename):
        """
        This will parse the csv_input file, to create a list of Expense objects
        from each row of the csv. It will also use the filename to create a
        ExpenseFile object. And it will return both the list of Expense objects
        and the ExpenseFile object. There are still in memory objects, nothing
        has been saved yet
        """

        _ = csv_input.next()  # We don't really need the first row??
        expenses = map(
            lambda row: ExpenseManager.get_expense_from_csv_row(row), csv_input
        )
        expense_file = ExpenseFile(filename=filename)
        return expense_file, expenses

    @staticmethod
    def get_expense_from_csv_row(csv_row):
        """
        Reads a csv row to generate an Expense object and returns it
        """
        expense_date = datetime.strptime(csv_row[0].strip(), "%m/%d/%Y").date()
        category = csv_row[1].strip()
        employee_name = csv_row[2].strip()
        employee_address = csv_row[3].strip()
        expense_description = csv_row[4].strip()
        pre_tax_amount = Utils.convert_currency_string_to_Decimal(csv_row[5])
        tax_name = csv_row[6].strip()
        tax_amount = Utils.convert_currency_string_to_Decimal(csv_row[7])

        from models import Expense

        e = Expense(
            expense_date=expense_date, category=category,
            employee_name=employee_name, employee_address=employee_address,
            expense_description=expense_description,
            pre_tax_amount=pre_tax_amount, tax_name=tax_name, tax_amount=tax_amount
        )
        return e

    @staticmethod
    def expense_files():
        return db_session.query(ExpenseFile).all()

    @staticmethod
    def expense_file_with_id(id):
        return db_session.query(ExpenseFile).filter(ExpenseFile.id==id).first()

    @staticmethod
    def expenses_for_file(expense_file_id):
        return db_session.query(Expense).filter(
            Expense.expense_file_id == expense_file_id
        ).all()

    @staticmethod
    def monthly_expense_dict(expense_file_id):

        expenses = ExpenseManager.expenses_for_file(expense_file_id)

        d = defaultdict(Decimal)
        for e in expenses:

            start_of_month = e.expense_date.replace(day=1)
            start_of_month = str(start_of_month)

            d[start_of_month] += e.tax_amount + e.pre_tax_amount

        return d

class Utils(object):

    @staticmethod
    def convert_currency_string_to_Decimal(amount):

        two_places = Decimal(10) ** -2
        amount = amount.strip()
        amount = sub(r'[^\d.]', '', amount)  # remove commas in the string
        amount = Decimal(amount).quantize(two_places)
        return amount
