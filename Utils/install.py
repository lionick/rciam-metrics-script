from Utils.pgConnector import destinationPgConnector

pgConn = destinationPgConnector()
pgConn.execute_and_commit(open("./config-templates/pgsql_tables.sql", "r").read())
pgConn.close()