from celery import Celery
from celery.utils.log import get_task_logger

from fidesops.core.config import config

logger = get_task_logger(__name__)


def create_celery():
    logger.info("Creating Celery app...")
    celery_app = Celery(__name__)
    celery_app.conf.update(broker_url=config.execution.CELERY_BROKER_URL)
    celery_app.conf.update(result_backend=config.execution.CELERY_RESULT_BACKEND)
    logger.info("Autodiscovering tasks...")
    celery_app.autodiscover_tasks(
        [
            "fidesops.tasks",
            "fidesops.tasks.scheduled",
            "fidesops.service.privacy_request",
        ]
    )
    return celery_app


celery_app = create_celery()


if __name__ == "__main__":
    logger.info("Running Celery worker...")
    print("running celery worker")
    celery_app.worker_main()
