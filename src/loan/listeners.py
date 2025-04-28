from sqlalchemy import event
from src import database
from src.client.models import Client
from src.loan.models import Loan
from src.loan.schemas import Loan_Status
from sqlalchemy import inspect                                          

@event.listens_for(database.Session, 'before_flush')
def increment_number_of_loans(session, flush_context, instances):
    """
    Increment the number of loans for a client when a new loan is added.
    """
    for obj in session.new:
        if isinstance(obj, Loan):
            client = session.get(Client, obj.client_id)
            if client:
                client.number_of_loans += 1
                client.total_loan_amount += obj.loan_amount


@event.listens_for(database.Session, 'before_flush')
def remove_number_of_loans(session, flush_context, instances):
    """
    Decrement the number of loans for a client when a loan is marked as paid.
    """
    for obj in session.dirty:
        if isinstance(obj, Loan) and obj.status == Loan_Status.PAID:
            client = session.get(Client, obj.client_id)
            if client:
                client.number_of_loans -= 1
                client.total_loan_amount -= obj.loan_amount