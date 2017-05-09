from django.db import models
import datetime
from django import utils

STATE_CHOICES = (('in_progress', 'in_progress'), ('ready', 'ready'),)


class RoadMap(models.Model):
    rd_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=100)
    state = models.CharField(max_length=11, choices=STATE_CHOICES, default='in_progress')
    estimate = models.DateField(default=utils.timezone.now)
    my_id = models.AutoField(primary_key=True)
    road_map = models.ForeignKey(RoadMap, related_name='tasks')
    create_date = models.DateField(default=utils.timezone.now)
    class Meta:
        ordering = ['state', 'estimate']



class Scores(models.Model):
    task = models.ForeignKey(Task)
    date = models.DateTimeField(default=utils.timezone.now())
    points = models.DecimalField(max_digits=5, decimal_places=2)
    class Meta:
        ordering = ['date']

