from django.core.management.base import BaseCommand, CommandError

from articles.models import Article


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         '--date',
    #         type=str,
    #         help="Filter articles by date"
    #     )
    #
    #
    # def handle(self, *args, **options):
    #     required_date = options.get('date')
    #
    #     if required_date:
    #         articles = Article.objects.filter(created_at__date__lt=required_date)
    #
    #         for article in articles:
    #             article.status = 'moderated'
    #             article.save()


    def handle(self, *args, **options):
        Article.objects.filter(status="moderated").update(status="new")
