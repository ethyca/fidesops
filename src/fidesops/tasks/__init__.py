from celery import Celery

from fidesops.core.config import config

app = Celery("tasks")
app.conf.update(broker_url=config.execution.CELERY_BROKER_URL)
app.conf.update(result_backend=config.execution.CELERY_RESULT_BACKEND)
app.autodiscover_tasks(
    [
        "fidesops.tasks",
        "fidesops.tasks.scheduled",
        "fidesops.service.privacy_request.request_runner_service",
    ]
)


if __name__ == "__main__":
    app.worker_main()
