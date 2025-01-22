from django.db import models

class Thread(models.Model):
    title = models.CharField(max_length=282)
    created = models.DateTimeField(auto_now_add=True)

class Media(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

    title = models.CharField(max_length=1000)
    file = models.FileField()
    created = models.DateTimeField(auto_now_add=True)
