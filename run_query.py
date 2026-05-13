import oracledb
import os
import re

USERNAME = "sys"
PASSWORD = "secret"
HOSTNAME = "localhost"
PORT = 21522
SERVICE_NAME = "XEPDB1"

SQL_FILE = os.path.join(os.path.dirname(__file__), "test.sql")


def main():
    dsn = oracledb.makedsn(HOSTNAME, PORT, service_name=SERVICE_NAME)

    with oracledb.connect(
        user=USERNAME,
        password=PASSWORD,
        dsn=dsn,
        mode=oracledb.AUTH_MODE_SYSDBA,
    ) as conn:
        with open(SQL_FILE, "r", encoding="utf-8-sig") as f:
            sql = f.read()

        # Replace curly/smart quotes with straight ASCII quotes
        sql = sql.replace('‘', "'").replace('’', "'")
        sql = sql.replace('“', '"').replace('”', '"')
        # Strip trailing semicolons and whitespace
        sql = re.sub(r'[\s;]+$', '', sql)

        # Report any remaining non-ASCII characters before sending to Oracle
        bad_chars = [(i, char, ord(char)) for i, char in enumerate(sql) if ord(char) > 127]
        if bad_chars:
            for pos, char, code in bad_chars:
                print(f"Non-ASCII character at position {pos}: U+{code:04X} {repr(char)}")

        with conn.cursor() as cursor:
            try:
                cursor.execute(sql)
                rows = cursor.fetchall()
                print(f"{len(rows)} row(s) returned.")
            except oracledb.DatabaseError as e:
                print(f"Oracle error: {e}")


if __name__ == "__main__":
    main()
