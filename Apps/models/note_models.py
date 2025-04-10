from datetime import date
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import now


class Note(models.Model):
    title = models.CharField(max_length=100)
    note = models.CharField(max_length=1000)
    mod_date = models.DateField(default=date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.note

    def is_deleted(self):
        return self.deleted_at is not None and self.deleted_at > now()

    def restore(self):
        """Khôi phục người dùng đã bị tạm xóa"""
        self.deleted_at = None
        self.save()

    def soft_delete(self):
        """Đánh dấu là đã xóa, cho phép khôi phục trong 5 phút"""
        self.deleted_at = now() + timedelta(minutes=5)
        self.save()
