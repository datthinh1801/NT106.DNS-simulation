import sqlite3
from ResourceRecord import ResourceRecord
from time import time


class Database:
    def __init__(self, name: str):
        """Init a aatabase to cache ResourceRecord."""
        # Connect databae
        self._name = name
        conn = sqlite3.connect(self._name)
        # Create a cursor
        c = conn.cursor()

        # Create table
        c.execute("""
            CREATE TABLE IF NOT EXISTS Cache(
                domain text,
                type integer,
                class integer,
                ttl integer,
                data text,
                ttd integer
            )
        """)

        # Commit connect
        conn.commit()
        # Close connect
        conn.close()

    def refresh(self):
        """ 
        Refresh the database to remove out-dated caches. 
        """
        # Connect database
        conn = sqlite3.connect(self._name)
        # Create cursor
        c = conn.cursor()

        c.execute("SELECT strftime('%s','now')")
        timestamp = (int(c.fetchone()[0]))
        time = (timestamp,)

        # sqlite3 doesn't support literal value comparision;
        # therefore an temporary _Variables table is necessary.
        c.execute("""
        CREATE TABLE IF NOT EXISTS _Variables(timestamp INTEGER)
        """)
        c.execute("INSERT INTO _Variables VALUES (?)", time)

        c.execute("""
            DELETE FROM Cache
            WHERE ttd < (SELECT timestamp FROM _Variables)
        """)

        c.execute("DROP TABLE _Variables")
        # Commit connect
        conn.commit()
        # Close connect
        conn.close()

    def add_to_database(self, rr: ResourceRecord):
        """
        Add an RR to database.
        """
        if rr.ttl > 0:
            # Connect database
            conn = sqlite3.connect(self._name)
            # Create cursor
            c = conn.cursor()

            ttd = int(time()) + rr.ttl

            data = (rr.name, rr.rr_type, rr.rr_class,
                    rr.ttl, rr.rdata, ttd)

            c.execute("INSERT INTO Cache VALUES (?,?,?,?,?,?)", data)

            # Commit connect
            conn.commit()
            # Close connect
            conn.close()

    def query_from_database(self, name: str, rr_type: int = 1,
                            rr_class: int = 1) -> ResourceRecord:
        """
        Query a tuple of (name, typr, class) from database for a match.
        """
        # Connect database
        conn = sqlite3.connect(self._name)

        # Create cursor
        c = conn.cursor()

        data = (name, rr_type, rr_class)

        # Create a temporary table for querying purposes
        c.execute("""
        CREATE TABLE IF NOT EXISTS _Variables(Name TEXT PRIMARY KEY, Class INTEGER, Type INTEGER)
        """)
        c.execute("INSERT INTO _Variables VALUES (?,?,?)", data)

        c.execute("""
        SELECT C.domain, C.type, C.class, C.ttd, C.data FROM Cache C
        WHERE C.domain = (SELECT Name FROM _Variables)
            AND C.type = (SELECT Type FROM _Variables)
            AND C.class = (SELECT Class FROM _Variables)
        """)

        ans = c.fetchone()
        c.execute("DROP TABLE _Variables")

        # Commit connect
        conn.commit()
        # Close connect
        conn.close()

        if ans is None:
            return ans
        else:
            return ResourceRecord(ans[0], ans[1], ans[2], ans[3], ans[4])

    """format use database sqlite3"""
    # def default():
    #     # Connect database
    #     conn = sqlite3.connect('CacheSystem.db')
    #     # Create cursor
    #     c = conn.cursor()

    """ code here """

    #     # Commit connect
    #     conn.commit()
    #     # Close connect
    #     conn.close()


if __name__ == '__main__':
    print("Resolver Database")
    # Connect database
    conn = sqlite3.connect('DatabaseResolver.db')
    # Create cursor
    c = conn.cursor()

    c.execute("SELECT * FROM Cache")
    data = c.fetchall()
    for dat in data:
        print(dat)

    # Commit connect
    conn.commit()
    # Close connect
    conn.close()

    print("NameServer Database")
    # Connect database
    conn = sqlite3.connect('DatabaseNS.db')
    # Create cursor
    c = conn.cursor()

    c.execute("SELECT * FROM Cache")
    data = c.fetchall()
    for dat in data:
        print(dat)

    # Commit connect
    conn.commit()
    # Close connect
    conn.close()
