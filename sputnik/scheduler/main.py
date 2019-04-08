from apscheduler.schedulers.asyncio import AsyncIOScheduler

from sputnik.scheduler.update_post import update_post
from sputnik.scheduler.utils import ping


def init_jobs(app):
    scheduler = AsyncIOScheduler({
        'apscheduler.timezone': 'UTC',
    })
    params = {'app': app}

    scheduler.add_job(ping, 'interval', seconds=10, kwargs=params)
    scheduler.add_job(update_post, 'interval', seconds=1, kwargs=params)

    return scheduler
