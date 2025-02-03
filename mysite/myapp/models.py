from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Food(models.Model):

    def __str__(self):
        return self.name 

    name = models.CharField(max_length=200)
    carbs = models.FloatField()
    protein = models.FloatField()
    fats = models.FloatField()
    calories = models.IntegerField()

class Consume(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_consumed = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1)  # Quantity in servings
    date_consumed = models.DateTimeField(auto_now_add=True)  # Track when food was consumed

   