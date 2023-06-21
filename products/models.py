from django.db import models

from users.models import User

FORMAT = [
    ('metr', 'metr'),
    ('kg', 'kg'),
    ('dona', 'dona'),
    ('litr', 'litr'),
    ('tonna', 'tonna'),
    ('mm', 'mm'),
    ('sm', 'santimetr'),
    ('diametr', 'diametr'),
    ('metr kvadrat', 'metr kvadrat'),
    ('metr kub', 'metr kub'),
]


class Mahsulotlar(models.Model):
    mahsulot_nomi = models.CharField(max_length=200)
    mahsulot_format = models.CharField(choices=FORMAT, max_length=30)

    def __str__(self):
        return f"{self.mahsulot_nomi} | {self.mahsulot_format}"

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'


class Mahsulot_olchov(models.Model):
    mahsulot_number = models.ForeignKey(Mahsulotlar, related_name='number', on_delete=models.CASCADE)
    olchov_nomi = models.CharField(max_length=100)
    olchov_format = models.CharField(choices=FORMAT, max_length=30)
    olchov = models.FloatField(help_text="(kg lik, litrlik ...)")
    narx = models.FloatField()

    def __str__(self):
        return f"{self.mahsulot_number} | O'chovi:  {self.olchov} lik  |  Narxi:  {self.narx} so'm"

    class Meta:
        verbose_name = "Mahsulot o'lchovi"
        verbose_name_plural = "Mahsulot o'lchovlari"


class OrderHistory(models.Model):
    user = models.OneToOneField(User, related_name='history_order', on_delete=models.DO_NOTHING)
    products = models.ManyToManyField('Mahsulot_olchov', blank=True, related_name='history_products')


class Analitika(models.Model):
    nom = models.CharField(max_length=200, null=True, blank=True)
    count = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.count} | {self.nom} "

    class Meta:
        verbose_name = 'Analitika'
        verbose_name_plural = 'Analitikalar'