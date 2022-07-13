from fidesops.core.config import config
from fidesops.tasks import _create_celery


def test_create_task(celery_session_app, celery_session_worker):
    @celery_session_app.task
    def multiply(x, y):
        return x * y

    # Force `celery_app` to register our new task
    # See: https://github.com/celery/celery/issues/3642#issuecomment-369057682
    celery_session_worker.reload()
    assert multiply.run(4, 4) == 16
    assert multiply.delay(4, 4).get(timeout=10) == 16


def test_celery_default_config() -> None:
    celery_app = _create_celery()
    assert celery_app.conf["broker_url"] == config.redis.CONNECTION_URL
    assert celery_app.conf["result_backend"] == config.redis.CONNECTION_URL
    assert celery_app.conf["event_queue_prefix"] == None
    assert celery_app.conf["default_queue_name"] == None


def test_celery_config_override() -> None:
    celery_app = _create_celery(config_path="data/config/celery.toml")
    assert celery_app.conf["event_queue_prefix"] == "fidesops_worker"
    assert celery_app.conf["default_queue_name"] == "fidesops"
