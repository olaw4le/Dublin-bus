"""define functions for querying a postgreSQL database"""

# replaced due to issues with psycopg2 and MacOS
# import psycopg2 as ps
import pg8000 as ps


def construct_sql(**kwargs):

    if "table_name" in kwargs:
        table_name = kwargs["table_name"]
    else:
        print("Error: No table name supplied")
        return False

    if "query_type" in kwargs:
        query_type = kwargs["query_type"]
    else:
        print("Error: No query type supplied")
        return False

    if "column_names" in kwargs:
        cols = ", ".join(kwargs["column_names"])
    else:
        cols = "*"

    # define template structures for sql queries
    templates = {
        "delete_all": "DELETE * FROM %s",
        "select_all": "SELECT * FROM %s",
        "select_where": "SELECT %s FROM %s WHERE %s",
        "insert": "INSERT INTO %s (%s) VALUES (%s)",
        "attr_names": """SELECT column_name FROM information_schema.columns WHERE table_name = '%s' ORDER BY ordinal_position"""
    }

    # if inserting data
    if query_type == "insert":

        # check that data passed as kwarg
        if "data" not in kwargs:
            print("Error: No data supplied for insert query")
            return False

        attr_names = ""
        attr_values = ""

        # for item in data to be inserted;
        # build a string containing the attribute names and attributes values
        for key in kwargs["data"].keys():

            attr_names += "%s, " % key
            val = kwargs["data"][key]

            # place string values in single quotes
            if type(val) not in [int, float]:
                val = "'%s'" % val
            else:
                val = str(val)

            attr_values += "%s, " % val

        # remove ", " from the end of attr_names & attr_Values
        attr_names = attr_names[:-2]
        attr_values = attr_values[:-2]

        # combine the query template, table name, attribute names & attribute values
        sql_query = templates[query_type] % (table_name, attr_names, attr_values)
    
        return sql_query

    # if selecting with predicate
    if query_type == "select_where":

        # check that data passed as kwarg
        if "data" not in kwargs:
            print("Error: No data supplied for insert query")
            return False

        predicates = ""

        # for item in data to be inserted;
        # build a string containing the attribute names and attributes values
        for key in kwargs["data"].keys():

            val = kwargs["data"][key]

            # place string values in single quotes
            if type(val) is str:
                val = "'%s'" % val
            else:
                val = str(val)

            predicates += " %s = %s AND" % (key, val)

        # remove "AND" from the end of attr_names & attr_Values
        predicates = predicates[:-3]

        # combine the query template, table name, attribute names & attribute values
        sql_query = templates[query_type] % (cols, table_name, predicates)
       
        return sql_query

    # if deleting/selecting *all* data from a table
    elif query_type in ["delete_all", "select_all", "attr_names"]:
        sql_query = templates[query_type] % table_name
        
        return sql_query

    else:
        print("Error: Unsupported query type entered")
        return False


def execute_sql(sql_query, database, user, password, host, port, **kwargs):
    
    # is function expected to produce output or not - depends on query type
    if ("retrieving_data" in kwargs) and type(kwargs["retrieving_data"] == bool):
        retrieving_data = kwargs["retrieving_data"]
    else:
        retrieving_data = False

    # try to establish a connection to the database
    try:
        connection = ps.connect(database=database, user=user, password=password, host=host, port=port)
    except Exception as e:
        return e

    cursor = connection.cursor()

    # try to execute the sql query
    try:
        cursor.execute(sql_query)
        connection.commit()
    except Exception as e:
        connection.close()
        print(e)
        return e

    # if retrieving data / expecting some kind of response...
    if retrieving_data:
        
        response = cursor.fetchall()
        
        connection.close()
        return response

    else:
        connection.close()

