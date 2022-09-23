from utils import QuickstartBase


base = QuickstartBase()

old_postgres = base.POSTGRES_SERVER
base.POSTGRES_SERVER = "not-a-db"
base.configure_postgres_connector(verify=False)
base.create_access_request()

# Go to UI show request fail

print("Press [enter] to continue...")
input()
base.POSTGRES_SERVER = old_postgres
base.configure_postgres_connector()
# Reprocess requests via UI
print("Press [enter] to continue...")
input()
