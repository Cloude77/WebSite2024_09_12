from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'DRAFT'
        PUBLISHED = 'PB', 'PUBLISHED'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='published', blank=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')  # связь user.blog_posts

    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)  # Тип
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    objects = models.Manager()  # менеджер, по умолчанию
    publish =  PublishedManager()  # конкретноприкладной менеджер

    class Meta:
        ordering = ['-published']
        indexes = [
            models.Index(fields=['-published']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Метод save вызывается при сохранении объекта в базу данных.
        Мы переопределяем этот метод, чтобы добавить логику перед сохранением данных.
        При этом сохраняется базовая функциональность метода благодаря вызову super().save().

        *args и **kwargs позволяют передавать дополнительные позиционные и именованные
        аргументы (например, force_insert, force_update, using и т. д.),
        чтобы не нарушать работу стандартного метода save.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.published.year,
                             self.published.month,
                             self.published.day,
                             self.slug])
