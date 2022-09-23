from utils import QuickstartBase


print("running the base")


class BasicConfig(QuickstartBase):
    def basic_config(self):
        self.configure_user()
        self.configure_email()
        self.configure_postgres_connector()
        self.configure_s3_storage()
        self.configure_mailchimp_connector()
        self.create_access_request()


# BasicConfig().basic_config()
BasicConfig().create_access_request(user_email="exampleuser@ethyca.com")

print("fin.")
