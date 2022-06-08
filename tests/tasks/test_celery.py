def test_create_task(celery_app, celery_worker):
    @celery_app.task
    def multiply(x, y):
        return x * y

    celery_worker.reload()  # Force `celery_app` to register our new task
    assert multiply.run(4, 4) == 16
    assert multiply.delay(4, 4).get(timeout=10) == 16
