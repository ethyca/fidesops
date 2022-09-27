from utils import QuickstartBase


print("running the base")


class BasicConfig(QuickstartBase):
    def basic_config(self):
        self.configure_user()
        self.configure_email()
        self.configure_postgres_connector()
        self.configure_s3_storage()
        self.configure_mailchimp_connector()


conf = BasicConfig()
# conf.basic_config()
# conf.get_policy(policy_key="download")

request_id = conf.create_access_request()
# verification_code = input("Insert verification code and press [enter] to continue...")
# conf.verify_subject_identity(
#     privacy_request_id=request_id,
#     code=verification_code,
# )
# BasicConfig().create_access_request(user_email="exampleuser@ethyca.com")

print("fin.")
