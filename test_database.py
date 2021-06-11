import sqlite3
from time import time
from sqlite3.dbapi2 import DatabaseError

# Connect databae
conn = sqlite3.connect('TestCacheSystem.bd')

# Create a cursor
c = conn.cursor()
v = conn.cursor()

""" Create table """
c.execute("""
    CREATE TABLE IF NOT EXISTS resourcerecord(
        domain text,
        type integer,
        class integer,
        data text
    )
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS refresh(
        refresh_time integer,
        refresh_time_next integer
    )
""")

""" Insert table """

c.execute("INSERT INTO resourcerecord VALUES ('facebook.com.',1,1,'69.171.250.35')")

array_tupple = [
    ('youtube', 1, 1, 'abcd'),
    ('google', 1, 1, 'haha'),
    ('zingme', 1, 1, 'okok'),
    ('uit', 1, 1, 'kaka')
 ]

c.executemany("INSERT INTO resourcerecord VALUES (?,?,?,?)", array_tupple)

c.execute("INSERT INTO refresh VALUES (300, 1623200987)")


"""Query Database """
# c.execute("SELECT rowid, * FROM resourcerecord")

# data = c.fetchall()

# for dat  in data:
#     print(dat)


""" Update refresh """


# v.execute("SELECT strftime('%s','now')")

# data = v.fetchone()
# print(data[0])



# c.execute("""
#     UPDATE refresh SET refresh_time_next = (SELECT strftime('%s','now'))
# """)




# c.execute("SELECT * FROM refresh")

# data = c.fetchall()
# for dat in data:
#     print(dat)

# print(int(time()))

# rr = ('google', 1, 1)

# c.execute("""
#     CREATE TABLE IF NOT EXISTS _Variables(Name TEXT PRIMARY KEY, Class INTEGER, Type INTEGER)
#     """)
# c.execute("INSERT INTO _Variables VALUES (?,?,?)", rr
# )


# data = c.execute("""
#     SELECT * FROM resoucerecord
#     WHERE domain = 'youtube' AND type = 1
# """)
# print(data)



# c.execute("SELECT * FROM _Variables")

# data = c.fetchall()
# for dat in data:
#     print(dat)


# c.execute("""
#     SELECT RR.domain FROM resourcerecord RR
#     WHERE RR.domain = (SELECT Name FROM _Variables)
#         AND RR.type = (SELECT Type FROM _Variables)
#         AND RR.class = (SELECT Class FROM _Variables)
#     """)
# data = c.fetchone()

# print(data)

c.execute("""
    DELETE FROM resourcerecord
    WHERE domain = 'zingme'
""")

c.execute("""
    SELECT * FROM resourcerecord RR
""")

data = c.fetchall()
for dat in data:
    print(dat)

# c.execute("DROP TABLE _Variables")




# commit
conn.commit()

# close
conn.close()
