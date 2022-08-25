from .report_query import make_query
from .send_report import send_report


def report_pipeline(email, cars_number):

    # make the query - get the data and some HTML
    try:
        query_data = make_query(cars_number)
    except Exception as e:
        print(e)
        print("Couldn't make the query")

    try:
        send_report(email=email, subject="FARM Cars Report", HTMLcontent=query_data)

    except Exception as e:
        print(e)
