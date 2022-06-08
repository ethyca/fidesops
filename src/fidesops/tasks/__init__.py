from celery import Celery

app = Celery("tasks")
app.config_from_object("fidesops.core.config", namespace="EXECUTION")
app.autodiscover_tasks(
    [
        "fidesops.tasks",
        "fidesops.tasks.scheduled",
        "fidesops.service.privacy_request.request_runner_service",
    ]
)


if __name__ == "__main__":
    app.worker_main()
