from apscheduler.schedulers.background import BackgroundScheduler

_scheduler = None


def get_scheduler() -> BackgroundScheduler:
    """Returns a BackgroundScheduler as a singleton"""
    global _scheduler  # pylint: disable=W0603
    if _scheduler is None:
        _scheduler = BackgroundScheduler()
        _scheduler.start()
    return _scheduler
