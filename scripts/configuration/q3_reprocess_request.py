from utils import QuickstartBase


base = QuickstartBase()

base.POSTGRES_SERVER = "not-a-db"
base.configure_postgres_connector()
base.create_access_request()
