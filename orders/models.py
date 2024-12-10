from django.db import models
from datetime import datetime

# Create your models here.

class Category(models.Model):
    category_title = models.CharField(max_length=200)
    category_gif = models.ImageField(upload_to="media")
    category_description = models.Field(max_length=200, null=True, blank=True) #make this the wysiwyg text field
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"{self.category_title}"

    def has_add_permission(self):
        return False

class RegularPizza(models.Model):
    #example row :: 1 topping , 5.00 , 7.00
    pizza_choice = models.CharField(max_length=200)
    small_price = models.DecimalField(max_digits=6, decimal_places=2)
    large_price = models.DecimalField(max_digits=6, decimal_places=2)
    category_description = models.Field(null=True, blank=True) #make this the wysiwyg text field

    class Meta:
        verbose_name = "List of Regular Pizza"
        verbose_name_plural = "List of Regular Pizza"

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Regular Pizza : {self.pizza_choice}"

class SicilianPizza(models.Model):
    #example row :: 1 topping , 5.00 , 7.00
    pizza_choice = models.CharField(max_length=200)
    small_price = models.DecimalField(max_digits=6, decimal_places=2)
    large_price = models.DecimalField(max_digits=6, decimal_places=2)
    category_description = models.Field(null=True, blank=True) #make this the wysiwyg text field

    class Meta:
        verbose_name = "List of Sicilian Pizza"
        verbose_name_plural = "List of Sicilian Pizza"
    
    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Sicilian Pizza : {self.pizza_choice}"

class Toppings(models.Model):
    #example row :: Pepperoni
    topping_name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "List of Pizza Toppings"
        verbose_name_plural = "List of Pizza Toppings"
    

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"{self.topping_name}"


class Sub(models.Model):
    #example row :: meatball , 5.00 , 6.50
    sub_filling = models.CharField(max_length=200)
    small_price = models.DecimalField(max_digits=6, decimal_places=2)
    large_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = "List of Subway Food"
        verbose_name_plural = "List of Subway Food"
    

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Sub : {self.sub_filling}"

class Pasta(models.Model):
    dish_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = "List of Pasta"
        verbose_name_plural = "List of Pasta"


    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"{self.dish_name}"


class Salad(models.Model):
    dish_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = "List of Salad"
        verbose_name_plural = "List of Salad"


    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Salad : {self.dish_name}"



class DinnerPlatters(models.Model):
    dish_name = models.CharField(max_length=200)
    small_price = models.DecimalField(max_digits=6, decimal_places=2)
    large_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = "List of Diner Platters"
        verbose_name_plural = "List of Diner Platters"


    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Platter : {self.dish_name}"

class Chapati(models.Model):
    chapati_choice = models.CharField(max_length=200)
    chapati_description = models.Field(null=True, blank=True)
    chapati_price = models.DecimalField(max_digits=5, decimal_places=2)  # You can adjust the price format based on your needs
    # Optionally add an image for the Chapati
    image = models.ImageField(upload_to='chapati_images/', null=True, blank=True)

    class Meta:
        verbose_name = "List of Chapati"
        verbose_name_plural = "List of Chapati"

    def __str__(self):
        return f"Chapati : {self.chapati_choice}"


class UserOrder(models.Model):
    username = models.CharField(max_length=200) #who placed the order
    order = models.TextField() #this will be a string representation of the cart from localStorage
    price = models.DecimalField(max_digits=6, decimal_places=2) #how much was the order
    time_of_order  = models.DateTimeField(default=datetime.now, blank=True)
    delivered = models.BooleanField()

    class Meta:
        verbose_name = "User Order List"
        verbose_name_plural = "User Order List"

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Order placed by  : {self.username} on {self.time_of_order.date()} at {self.time_of_order.time().strftime('%H:%M:%S')}"

class SavedCarts(models.Model):
    username = models.CharField(max_length=200, primary_key=True)
    cart = models.TextField() #this will be a string representation of the cart from localStorage

    class Meta:
        verbose_name = "Saved Users Cart"
        verbose_name_plural = "Saved Users Cart"


    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Saved cart for {self.username}"

