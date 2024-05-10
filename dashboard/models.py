from django.db import models


# Create your models here.
class Game(models.Model):
    Away_Score = models.IntegerField()
    Home_Score = models.IntegerField()
    Away_Goalie = models.CharField(max_length=255)
    Home_Goalie = models.CharField(max_length=255)
    Event = models.CharField(max_length=255)
    Period = models.IntegerField()
    Ev_Zone = models.CharField(max_length=255)
    Strength = models.CharField(max_length=255)
    Type = models.CharField(max_length=255)
    Date = models.DateField()
    Ev_Team = models.CharField(max_length=255)
    Away_Team = models.CharField(max_length=255)
    Home_Team = models.CharField(max_length=255)

    def __str__(self):
        return self.Away_Team + " vs. " + self.Home_Team + ", " + str(self.Date.year) + "/" + str(self.Date.month) + "/" + str(self.Date.day)

