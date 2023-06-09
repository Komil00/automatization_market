from django.db import models

from products.models import Mahsulot_olchov, Mahsulotlar
from users.models import Mijoz, User

# TYPE_STATUS - Moliya uchun Kirim(pul kirishi), Chiqim(pul chiqishi) uchun choice
TYPE_STATUS = (
    ('kirim', "kirim"),
    ('chiqim', "chiqim"),
)

# TRANZ_TUR - Moliyada nima maqsad uchun Kirim yoki Chiqim qilish choicelar
TRANZ_TUR = (
    ('mijoz', "mijoz"),
    ('mahsulot', "mahsulot"),
    ('hodim', "hodim"),
    ('boshqa', "Boshqa")
)
FORMAT = [
    ('metr', 'metr'),
    ('kg', 'kg'),
    ('dona', 'dona'),
    ('litr', 'litr'),
    ('tonna', 'tonna'),
    ('mm', 'mm'),
    ('sm', 'santimetr'),
    ('metr kvadrat', 'metr kvadrat'),
    ('metr kub', 'metr kub'),
]
PAY_STATUS = (
    ('naqt', "Naqt"),
    ('plastik', "Plastik"),
    ('kochirma', "Ko'chirma"),
    ('boshqa', "Boshqa")
)


# Tranzaksiya Models - Moliya bo'limidagi Qanday turdagi kirim va chiqim uchun
class Tranzaksiya(models.Model):
    title = models.CharField(max_length=200)
    turi = models.CharField(max_length=200, choices=TYPE_STATUS)
    status = models.CharField(max_length=200, choices=TRANZ_TUR)

    def __str__(self):
        return f"{self.title} | {self.turi}"

    class Meta:
        verbose_name = "Tranzaksiya turi"
        verbose_name_plural = "Tranzaksiya turi"


# Savdo Models - Mijozning qilgan savdolari va barcha ma'lumotlari
class Savdo(models.Model):
    SavdoTuri = (
        ("Naqtga", "Naqtga"),
        ("Qarzga", "Qarzga"),
    )
    Chegirma_turi = (
        ("Chegirmaviy_summa", "Chegirmaviy_summa"),
        ("Chegirma_narx", "Chegirma_narx"),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Sotgan", help_text="Sotuvchi",
                             null=True)
    savdo_turi = models.CharField(max_length=223, default='Naqtga', choices=SavdoTuri, null=True)
    chegirma_turi = models.CharField(max_length=223, default='Chegirmaviy_summa', choices=Chegirma_turi, null=True)
    vaqt = models.DateTimeField()
    mijoz = models.ForeignKey(Mijoz, on_delete=models.CASCADE, related_name='savdolar')
    chegirma = models.PositiveIntegerField(default=0)

    @property
    def get_mijoz_total_sum(self):
        summa = sum([product.summa for product in self.tolovlar_mijozlar.all()])
        return summa

    def get_mahsulot_total_sum(self):
        mahsulot_summa = sum([product.umumiy for product in self.savdo_products.all()])
        return mahsulot_summa

    def total_summa(self):
        return sum([product.umumiy for product in self.savdo_products.all()]) - self.chegirma
    
    
    # def ombor_farq(self):
    #     return self.sum([ombor.summa for ombor in self.ombor_olchovi.all()]) - self.miqdor

    class Meta:
        verbose_name = "Savdo"
        verbose_name_plural = "Savdolar"


# SavdoProduct - Savdoni ichiga beriladigan bir qancha mahsulotlar
class SavdoProduct(models.Model):
    NarxTuri = (
        ("Narxida", "Narxida"),
        ("Chegirma", "Chegirma"),
    )
    Sotish_turi = (
        ("O'lchovli", "O'lchovli"),
        ("O'lchovsiz", "O'lchovsiz"),
    )
    savdo = models.ForeignKey(Savdo, on_delete=models.SET_NULL, related_name='savdo_products', null=True, blank=True)
    mahsulot = models.ForeignKey(Mahsulotlar, on_delete=models.SET_NULL, null=True, related_name='mahsulotlar')
    olchov = models.ForeignKey(Mahsulot_olchov, on_delete=models.CASCADE)
    miqdor = models.FloatField(default=0)
    narx_turi = models.CharField(max_length=223, default="Chegirma", choices=NarxTuri, null=True)
    narx = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    sotish_turi = models.CharField(max_length=223, default="O'lchovli Savdo", choices=Sotish_turi, null=True)
    sotish_olchov = models.CharField(max_length=9000, null=True, blank=True)
    
    total_summa = models.PositiveBigIntegerField(default=0)

    @property
    def umumiy(self):
        if self.narx > 0:
            return self.narx * self.miqdor
        return self.olchov.narx * self.miqdor
    
    

    def str(self):
        return f"{self.mahsulot} - {self.savdo.mijoz}"


# Tolovlar Models - Moliya kirim uchun - Mijoz Savdo qilganda to'lov qilish uchun
class Tolovlar(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Sotgan", help_text="Sotuvchi",
                             null=True, blank=True)
    savdo = models.ForeignKey(Savdo, on_delete=models.CASCADE, related_name="tolovlar_mijozlar")
    tranzaksiya_turi = models.ForeignKey(Tranzaksiya, on_delete=models.CASCADE)
    tolov_turi = models.CharField(max_length=200, choices=PAY_STATUS)
    muddat = models.DateTimeField(null=True, blank=True)
    summa = models.FloatField(default=0)
    status = models.BooleanField(default=True)
    yaralgan_sana = models.DateTimeField(null=True)
    chek_id = models.IntegerField(null=True, blank=True, unique=True)
    izoh = models.TextField(null=True, blank=True)

    def mijoz(self):
        return Mijoz.objects.all()

    def __str__(self):
        return f"Mahsulot : {self.savdo} | Qarz muddat :  {self.muddat}"

    @property
    def chek_id(self):  # noqa
        return 100000 + self.id

    class Meta:
        unique_together = ['savdo', 'summa']
        ordering = ['summa']
        verbose_name = "To'lov"
        verbose_name_plural = "To'lovlar"