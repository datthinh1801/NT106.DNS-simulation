import sqlite3
from sqlite3.dbapi2 import connect
from time import time
from CacheSystem import CacheSystem
from Cache import Cache
from ResourceRecord import ResourceRecord

def create_dtb():
    # Connect databae
    conn = sqlite3.connect('CacheSystem.db')

    # Create a cursor
    c = conn.cursor()

    # Create table 
    c.execute("""
        CREATE TABLE IF NOT EXISTS Refresh(
            refresh_time integer,
            next_refresh_time integer
        )
    """)

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

    data = (300, int(time()))
    c.execute("INSERT INTO Refresh VALUES (?,?)", data)

    # Commit connect 
    conn.commit()

    # Close connect 
    conn.close()



def add_to_dtb(rr: ResourceRecord):
    # Connect database
    conn = sqlite3.connect('CacheSystem.db')
    # Create cursor
    c = conn.cursor()

    ttd = int(time()) + rr._ttl

    data = (rr._name, rr._type, rr._class,
            rr._ttl, rr._rdata, ttd)

    c.execute("INSERT INTO Cache VALUES (?,?,?,?,?,?)", data)

    # Commit connect 
    conn.commit()
    # Close connect 
    conn.close()


def refresh_dtb():

    # Connect database
    conn = sqlite3.connect('CacheSystem.db')
    # Create cursor
    c = conn.cursor()

    c.execute("SELECT strftime('%s','now')")
    timestamp = (int(c.fetchone()[0]))

    c.execute("SELECT R.next_refresh_time FROM Refresh R")
    next_fresh_time = int(c.fetchone()[0])

    # print('time st: ', timestamp)
    # print('next : ', next_fresh_time)

    if next_fresh_time <= timestamp:
        time = (timestamp,)
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


def query_from_dtb(name: str, rr_type: int = 1, rr_class: int = 1) -> ResourceRecord:
    # Connect database
    conn = sqlite3.connect('CacheSystem.db')

    # Create cursor
    c = conn.cursor()

    data = (name, rr_type, rr_class)

    c.execute("""
    CREATE TABLE IF NOT EXISTS _Variables(Name TEXT PRIMARY KEY, Class INTEGER, Type INTEGER)
    """)
    c.execute("INSERT INTO _Variables VALUES (?,?,?)", data)

    c.execute("""
    SELECT C.domain, C.type, C.class, C.ttd, C.data FROM Cache C
    WHERE C.domain = (SELECT Name FROM _Variables)
        AND C.type = (SELECT Type FROM _Variables)
        AND C.class = (SELECT Class FROM _Variables)
        AND C.ttd > (SELECT strftime('%s','now'))
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




def default():
    # Connect database
    conn = sqlite3.connect('CacheSystem.db')
    # Create cursor
    c = conn.cursor()

    """ code here """

    # Commit connect 
    conn.commit()
    # Close connect 
    conn.close()

if __name__ == '__main__':
    # timest = time()
    # print(timest)
    create_dtb()
    a = query_from_dtb('fb.com', 1, 1)
    if a is None:
        print(a)
    rr = ResourceRecord('fb.com', 1, 1, 300, '1.2.3')
    add_to_dtb(rr)

    a = query_from_dtb('fb.com', 1, 1)
    if a is None:
        print(a)
    else:
        print(a.to_string())

    conn = sqlite3.connect('CacheSystem.db')
    # Create cursor
    c = conn.cursor()

    c.execute("SELECT * FROM Refresh")
    data = c.fetchall()
    print(data)

    c.execute("SELECT * FROM Cache")
    data = c.fetchall()
    for dat in data:
        print(dat)
    # Commit connect 
    conn.commit()
    # Close connect 
    conn.close()