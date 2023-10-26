import trino.dbapi
import threading

def test_connection(cursor, result):
    try:
        cursor.execute("SELECT 1")
        result.append(True)  # Append True to the result list if the query is successful
    except Exception as e:
        print(f"Error while executing query: {e}")

def connect_trino(host, port, protocol):
    # Connect to Trino
    conn = trino.dbapi.connect(
        http_scheme=protocol,
        user="test",
        host=host,
        port=int(port),
        catalog='storage',
        schema='txt',
        verify=False
    )
    cursor = conn.cursor()

    result = []  # This list will be used to store the result of the thread
    thread = threading.Thread(target=test_connection, args=(cursor, result))
    thread.start()

    thread.join(timeout=10)  # Wait for the thread to finish, with a timeout of 10 seconds

    if thread.is_alive():
        print("Query execution took too long, cancelling...")
        cursor.close()  # Close the cursor, which should also cancel the query
        conn.close()  # Close the connection
        return None
    elif result:
        return conn
    else:
        print("Query execution failed")
        return None

#def test_file_conn(connection, query, files, format):
def test_file_conn(connection,file,type):
    cursor = connection.cursor()
   # print(f"SELECT * FROM storage.{type}.\"file://{file}\"")
    cursor.execute(f"SELECT * FROM storage{type}.\"file://{file}\"")
    rows = cursor.fetchall()
    return rows
    # if files:
    #     if query=="SELECT * FROM storage.txt.\"file://{file}\"":
    #         final_query = query.
    # format(file=files[0])
    #     elif query=="SELECT * FROM storage.txt.\"file://{file}\" UNION ALL SELECT * FROM storage.txt.\"file://{file1}\"":
    #         if len(files)==2:
    #             final_query = query.format(file=files[0], file1=files[1])
    #         else:
    #             final_query = " UNION ALL ".join([f"SELECT * FROM storage.txt.\"file://{file}\"" for file in files])
    # cursor.execute(final_query)
    # rows = cursor.fetchall()

    # # Convert list of tuples to list of strings
    # rows = [row[0] for row in rows]
    # if format == "None":
    #     return rows
    # else:
    #     #return format_query_output(rows, format)
    #     return rows

def query_host(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        
    except Exception as e:
        print(f"Error while executing query: {e}")
    rows = cursor.fetchall()
    if rows:
        return rows
    else:
        return "No results found"
    