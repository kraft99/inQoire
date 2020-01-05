import string

from celery import shared_task


@shared_task
def test_count(total):
    for i in range(total):
    	print(i)