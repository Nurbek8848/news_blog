from huey.djhuey import crontab, db_periodic_task, db_task

from articles.models import Article


@db_task()
def do_some_queries():
    print("do_some_queries")

@db_periodic_task(crontab(minute='*/1'))
def every_five_mins():
    count = Article.objects.count()
    print(f"{count} articles")