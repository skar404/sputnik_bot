from apscheduler.schedulers.asyncio import AsyncIOScheduler

from sputnik import settings
from sputnik.scheduler.send_new_post import send_new_post
from sputnik.scheduler.update_post import update_post
from sputnik.scheduler.utils import ping


def init_jobs(app):
    scheduler = AsyncIOScheduler({
        'apscheduler.timezone': 'UTC',
    })
    params = {'app': app}

    scheduler.add_job(ping, 'interval', seconds=10, kwargs=params)
    scheduler.add_job(update_post, 'interval', seconds=settings.UPDATE_POST_SECONDS, kwargs=params)
    scheduler.add_job(send_new_post, 'interval', seconds=settings.SEND_POST_SECONDS, kwargs=params)

    return scheduler
