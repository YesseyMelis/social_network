from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.account.models import User


class CreatedChangedAbstract(models.Model):
    """
    Абстракный класс для хранения дата хранения даты создание и изменение записи
    """
    class Meta:
        abstract = True
        ordering = ["changed_at"]

    created_at = models.DateTimeField(_("created date"), auto_now_add=True)
    changed_at = models.DateTimeField(_("changed date"), auto_now=True)


class Post(CreatedChangedAbstract):
    name = models.CharField(_("name"), max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostRating(CreatedChangedAbstract):
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,
        null=True,
        related_name='ratings',
        verbose_name=_("post")
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='rated_posts',
        verbose_name=_("user")
    )

    class Meta:
        verbose_name = 'Оценка поста'
        verbose_name_plural = 'Оценки поста'
