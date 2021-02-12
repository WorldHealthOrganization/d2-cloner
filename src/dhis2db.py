import psycopg2

con = ""


def init_db(database, user, password, host, port):
    return psycopg2.connect(database=database, user=user, password=password, host=host, port=port)


def close(con):
    con.close()


def execute_query(con, query):
    cur = con.cursor()

    cur.execute(query)

    rows = cur.fetchall()
    for row in rows:
        print(row[1])

#con = init_db("dhis2", "dhis", "dhis", "192.168.160.3", "5432")
#executeQuery(con, "select * from users limit 1;")
#close(con)

def checkDuplicates():
    print("Database opened successfully")

    cur = con.cursor()

    cur.execute("select t.table_schema, t.table_name from information_schema.tables t inner join information_schema.columns c on c.table_name = t.table_name and c.table_schema = t.table_schema where c.column_name = 'uid' and t.table_schema not in ('information_schema', 'pg_catalog') and t.table_type = 'BASE TABLE' order by t.table_schema;");

    rows = cur.fetchall()
    tables = []

    for row in rows:
        tables.append(row[1])
    for table in tables:
        if table in ["audit", "deletedobject", "visualization"]:
            continue
        print(table)
        cur.execute("select uid from "+table+";");
        rows = cur.fetchall()
        active_uid = []
        for row in rows:
            active_uid.append(row[0])
        for tableB in tables:
            if tableB in ["audit", "deletedobject", "visualization"]:
                continue
            if tableB != table:
                cur.execute("select uid from "+tableB+";");
                rows = cur.fetchall()
                for row in rows:
                    if row[0] in active_uid:
                            print ({"id": row[0], "typeA": table, "typeB": tableB},)

    con.close()