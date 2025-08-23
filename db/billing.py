from .connection import bills


def get_latest_bill_no():
    bill = bills.aggregate([{"$group": {"_id": None, "bill_no": {"$max": "$bill_no"}}}])
    for bill_no in bill:
        no = bill_no.get('bill_no', None)
    return no if no else 10001