from django.db.models import Manager


class ArticleManager(Manager):
    def moderated(self):
        return self.filter(status='moderated')

    def new(self):
        return self.filter(status='new')