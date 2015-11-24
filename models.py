from datetime import datetime

from database import Base

import sqlalchemy.types as sa_types
from sqlalchemy import Column, ForeignKey

class ExpenseFile(Base):
    __tablename__ = 'expense_files'

    id = Column(sa_types.Integer, primary_key=True)
    filename = Column(sa_types.String(50), nullable=False)
    utc_datetime = Column(sa_types.DateTime(timezone=False), nullable=False)

    def __init__(self, filename):
        self.filename = filename
        self.utc_datetime = datetime.utcnow()

    def __str__(self):
        s = 'FileExpense - ' + \
            ', id: ' + str(self.id) + \
            ', filename: ' + str(self.filename) + \
            ', utc_datetime: ' + str(self.utc_datetime)
        return s

class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(sa_types.Integer, primary_key=True)

    expense_file_id = Column(sa_types.Integer, ForeignKey('expense_files.id'))
    expense_date = Column(sa_types.Date, nullable=False)
    category = Column(sa_types.String(50), nullable=False)
    employee_name = Column(sa_types.String(50), nullable=False)
    employee_address = Column(sa_types.String(100), nullable=False)
    expense_description = Column(sa_types.String(100), nullable=False)
    pre_tax_amount = Column(
        sa_types.NUMERIC(precision=10, scale=2), nullable=False
    )
    tax_name = Column(sa_types.String(50), nullable=False)
    tax_amount = Column(
        sa_types.NUMERIC(precision=10, scale=2), nullable=False
    )

    def __init__(
            self, expense_date, category,
            employee_name, employee_address,
            expense_description,
            pre_tax_amount, tax_name, tax_amount
    ):
        # self.expense_file_id = expense_file_id
        self.expense_date = expense_date
        self.category = category

        self.employee_name = employee_name
        self.employee_address = employee_address

        self.expense_description = expense_description
        self.pre_tax_amount = pre_tax_amount
        self.tax_name = tax_name
        self.tax_amount = tax_amount

    def __str__(self):

        s = 'Expense - ' + \
            ', id: ' + str(self.id) + \
            ', expense_file_id: ' + str(self.expense_file_id) + \
            ', expense_date: ' + str(self.expense_date) + \
            ', category: ' + str(self.category) + \
            ', employee_name: ' + str(self.employee_name) + \
            ', employee address: ' + str(self.employee_address) + \
            ', expense_description: ' + str(self.expense_description) + \
            ', pre_tax_amount: ' + str(self.pre_tax_amount) + \
            ', tax_name: ' + str(self.tax_name) + \
            ', tax_amount: ' + str(self.tax_amount)
        return s


