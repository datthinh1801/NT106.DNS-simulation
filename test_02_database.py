from Database import Database
from ResourceRecord import ResourceRecord
from time import sleep


def test_database():
    db = Database('test.db')
    rr = ResourceRecord('www.google.com', 1, 1, 1, '127.0.0.1')
    db.add_to_database(rr)
    assert rr == db.query_from_database('www.google.com', 1, 1)
