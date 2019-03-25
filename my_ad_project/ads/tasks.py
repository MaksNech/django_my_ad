from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from celery.task.schedules import crontab
from django.utils import timezone
from .models import Ad

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_check_ad_inactivity",
    ignore_result=True
)
def task_check_ad_inactivity():
    ads = Ad.objects.filter(status=200)
    for ad in ads:
        if (ad.updated_on + timezone.timedelta(days=30)) <= timezone.now():
            ad.status = 100
            ad.save()
            logger.info('Ad marked as "INACTIVE"! ID: {0}, Title: {1}, Author: {2}.'.format(ad.id, ad.title,
                                                                                            ad.author))


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_update_report",
    ignore_result=True
)
def task_update_report():
    ads = Ad.objects.filter(created_on__gte=timezone.now() - timezone.timedelta(seconds=60))
    if ads:
        info = ''
        for ad in ads:
            info += 'New Ad! Created: {0}, ID: {1}, Title: {2}, Author: {3}.\n'.format(ad.created_on, ad.id,
                                                                                       ad.title, ad.author)
            logger.info('New Ad is added to report.txt! ID: {0}, Title: {1}, Author: {2}.\n'.format(ad.id, ad.title,
                                                                                                    ad.author))

        with open('celery_report.txt', 'a+') as f:
            f.write(info)
