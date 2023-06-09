from django.db import models
from django.db.models import Sum
from products.models import Mahsulot_olchov, Mahsulotlar
from savdo.models import Mijoz, Savdo, Tranzaksiya
from users.models import Ishchi, User

PAY_STATUS = (
    ('naqt', "Naqt"),
    ('plastik', "Plastik"),
    ('kochirma', "Ko'chirma"),
    ('boshqa', "Boshqa")
)

FORMAT = [
    ('metr', 'metr'),
    ('kg', 'kg'),
    ('dona', 'dona'),
    ('litr', 'litr'),
    ('tonna', 'tonna'),
    ('mm', 'mm'),
    ('sm', 'sm'),
]


# Moliya chiqim (Pul chiqishi)
# Moliya chiqim - Omborga kelgan Mahsulot mabodo qarzga bo'lsa, uni to'lashda foydalaniladi
class Moliya_chiqim(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Sotgan", help_text="Sotuvchi",
                             null=True)
    nomi = models.CharField(max_length=200, null=True, blank=True, default=None, help_text='svetga,arendaga ...')
    tranzaksiya_turi = models.ForeignKey(Tranzaksiya, on_delete=models.CASCADE)
    mijoz = models.ForeignKey(Mijoz, on_delete=models.CASCADE, null=True, blank=True)
    ishchi = models.ForeignKey(Ishchi, on_delete=models.CASCADE, null=True, blank=True)
    tolov_turi = models.CharField(max_length=200, choices=PAY_STATUS, null=True, blank=True)
    vaqt = models.DateTimeField()
    mahsulot_nomi = models.ForeignKey(Mahsulotlar, related_name='mahsulot_nom', on_delete=models.SET_NULL, null=True,blank=True)
    olchov = models.ForeignKey(Mahsulot_olchov, related_name='olchovi', on_delete=models.SET_NULL, null=True, blank=True)
    summa = models.PositiveIntegerField(null=True, blank=True)
    ombor_id = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.nomi} | {self.vaqt} {self.ombor_id}"

    class Meta:
        verbose_name = "Moliya chiqim"
        verbose_name_plural = "Moliya chiqim"



# Ombor Categoriya - ya'ni - Qanaqa turga kirishi. Masalan Truba - 32lik, 40lik, 100lik tartibi bilan
class OmborCategory(models.Model):
    kategoriya = models.CharField(max_length=223)
    def __str__(self):
        return f"{self.kategoriya}"
    class Meta:
        verbose_name = 'Ombor Kategoriyasi'
        verbose_name_plural = 'Ombor Kategoriyalari'


# Omborxona - Sotib olinayotgan mahsulotlar shu bo'limda yaratiladi. Ularning qarzga olinganini to'lashda esa Moliya chiqimda amalga oshiriladi

class Omborxona(models.Model):
    SavdoTuri = (
        ("Naqtga", "Naqtga"),
        ("Qarzga", "Qarzga"),
    )
    NarxTuri = (
        ("Narxli", "Narxli"),
        ("Umumiy narx", "Umumiy narx"),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Sotgan", help_text="Sotuvchi",null=True)
    savdo_turi = models.CharField(max_length=223, default='Naqtga', choices=SavdoTuri, null=True)
    kategoriya = models.ForeignKey(OmborCategory, related_name='kategoriya_ombor', on_delete=models.CASCADE)
    mahsulot_nomi = models.ForeignKey(Mahsulotlar, related_name='ombor_mahsulot', on_delete=models.CASCADE)
    olchov = models.ForeignKey(Mahsulot_olchov, related_name='ombor_olchovi', on_delete=models.CASCADE)
    miqdor = models.FloatField()
    narx_turi = models.CharField(max_length=223, default="Narxli", choices=NarxTuri, null=True)
    narx = models.FloatField(default=0, null=True, blank=True)
    summa = models.FloatField(default=0)
    total_summa = models.PositiveIntegerField(default=0)
    vaqt = models.DateTimeField()

    description = models.TextField(null=True, blank=True)
    chiqim_id = models.FloatField(null=True, blank=True)

    @property
    def summa(self):
        return self.narx * self.miqdor

    def __str__(self):
        return f"{self.kategoriya}"

    class Meta:
        verbose_name = 'Omborxona'
        verbose_name_plural = 'Omborxona'
