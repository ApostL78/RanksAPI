from django.db import models


class DiscountChoices(models.TextChoices):
    ONCE = 'once', 'Одноразовый'
    FOREVER = 'forever', 'Безлимитный'


class Discount(models.Model):
    name = models.CharField("Название купона", max_length=255)
    percent_off = models.IntegerField("Скидка в процентах")
    duration = models.CharField("Продолжительность действия купона", max_length=10, choices=DiscountChoices.choices)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"


class Tax(models.Model):
    display_name = models.CharField("Название", max_length=255)
    inclusive = models.BooleanField("Процент или включенный в стоимость")
    percentage = models.DecimalField("Проценты", max_digits=6, decimal_places=2)
    description = models.TextField("Описание", blank=True, null=True)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"


class Item(models.Model):
    name = models.CharField("Название", max_length=120)
    description = models.TextField("Описание", blank=True, null=True)
    price = models.DecimalField("Цена", max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


class Order(models.Model):
    items = models.ManyToManyField(Item, verbose_name="Товары")
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, verbose_name="Скидка", null=True, blank=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, verbose_name="Налог", null=True, blank=True)

    def __str__(self):
        return "Заказ №" + str(self.id)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
