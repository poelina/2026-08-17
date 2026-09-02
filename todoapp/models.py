from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):

    name = models.CharField(
        max_length = 60,
        verbose_name = "Название",
        help_text = "Введите название категории:"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("todo:category", kwargs={"category_id": self.pk})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']


class Task(models.Model):

    title = models.CharField(
        max_length=200,
        verbose_name="Задача",
        help_text="Введите название задачи:"
    )

    description = models.TextField(
        max_length=500,
        verbose_name="Описание",
        help_text="Введите описание задачи:"
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания задачи:",
        help_text="Введите дату создания задачи:"
    )

    due_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Срок выполнения задачи:",
        help_text="Введите срок выполнения задачи:"
    )

    is_completed = models.BooleanField(
        default=False,
        verbose_name="Выполнено",
    )

    category_task = models.ForeignKey(
        Category,
        on_delete = models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Название",
        related_name="tasks", #category.tasks.all
    )

    @property
    def is_past_due(self):
        if self.due_date and not self.is_completed:
            return timezone.now() > self.due_date
        return False

    def toggle_completed(self):
        self.is_completed = not self.is_completed
        self.save()
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("todo:task_detail", kwargs={"pk": self.pk})

    def toggle_completed(self):
        self.is_completed = not self.is_completed
        self.save()

    class Meta:
        verbose_name="Задача"
        verbose_name_plural="Задачи"
        ordering=['is_completed', '-created_date']