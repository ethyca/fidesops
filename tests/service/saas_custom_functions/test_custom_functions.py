import importlib

def test_get_custom_functions():
    saas_connector = "mailchimp"
    custom_function_name = "read_messages"
    module = importlib.import_module(f"fidesops.service.saas_custom_functions.{saas_connector}")
    custom_function = getattr(module, custom_function_name)
    assert callable(custom_function)