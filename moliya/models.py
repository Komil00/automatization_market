from django.db import IntegrityError, models
from django.db.models import Sum
from django.forms import ValidationError
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
    mahsulot = models.ForeignKey(Mahsulotlar, related_name='ombor_mahsulot', on_delete=models.CASCADE)
    olchov = models.ForeignKey(Mahsulot_olchov, related_name='ombor_olchovi', on_delete=models.CASCADE)
    miqdor = models.FloatField()
    narx_turi = models.CharField(max_length=223, default="Narxli", choices=NarxTuri, null=True)
    narx = models.FloatField(default=0, null=True, blank=True)
    summa = models.FloatField(default=0)
    total_summa = models.PositiveIntegerField(default=0)
    vaqt = models.DateTimeField()
    @property
    def summa(self):
        return self.narx * self.miqdor
    def __str__(self):
        return f"{self.mahsulot}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            bor_edi = Omborxona.objects.filter(mahsulot=self.mahsulot, olchov=self.olchov).first()
            if bor_edi:
                bor_edi.miqdor += self.miqdor
                bor_edi.save()
                return
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Omborxona'
        verbose_name_plural = 'Omborxona'

class Omborxona_Get(models.Model):
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
    mahsulot = models.ForeignKey(Mahsulotlar, related_name='ombor_mahsulotlar', on_delete=models.CASCADE)
    olchov = models.ForeignKey(Mahsulot_olchov, related_name='ombor_olchovilar', on_delete=models.CASCADE)
    miqdor = models.FloatField()
    narx_turi = models.CharField(max_length=223, default="Narxli", choices=NarxTuri, null=True)
    narx = models.FloatField(default=0, null=True, blank=True)
    summa = models.FloatField(default=0)
    total_summa = models.PositiveIntegerField(default=0)
    vaqt = models.DateTimeField()
    @property
    def summa(self):
        try:
            narx = float(self.narx)
            miqdor = float(self.miqdor)
            return narx * miqdor
        except (ValueError, TypeError):
            return 0
    def __str__(self):
        return f"{self.mahsulot}"

    class Meta:
        verbose_name = 'Omborxona_Get'
        verbose_name_plural = 'Omborxona_Get'

# Moliya chiqim (Pul chiqishi)
# Moliya chiqim - Omborga kelgan Mahsulot mabodo qarzga bo'lsa, uni to'lashda foydalaniladi
class Moliya_chiqim(models.Model):
    TolovStatus = (
        ("Davom ettirish", "Davom ettirish"),
        ("Yopish", "Yopish"),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Sotgan", help_text="Sotuvchi",
                             null=True)
    nomi = models.CharField(max_length=200, null=True, blank=True, default=None, help_text='svetga,arendaga ...')
    tranzaksiya_turi = models.ForeignKey(Tranzaksiya, on_delete=models.CASCADE)
    mijoz = models.ForeignKey(Mijoz, on_delete=models.CASCADE, null=True, blank=True)
    ishchi = models.ForeignKey(Ishchi, on_delete=models.CASCADE, null=True, blank=True)
    tolov_turi = models.CharField(max_length=200, choices=PAY_STATUS, null=True, blank=True)
    vaqt = models.DateTimeField()
    # mahsulot_nomi = models.ForeignKey(Mahsulotlar, related_name='mahsulot_nom', on_delete=models.SET_NULL, null=True,blank=True)
    # olchov = models.ForeignKey(Mahsulot_olchov, related_name='olchovi', on_delete=models.SET_NULL, null=True, blank=True)
    summa = models.PositiveIntegerField(null=True, blank=True)
    ombor_savdo = models.ForeignKey(Omborxona, on_delete=models.SET_NULL,related_name='ombor_moliya_chiqim',null=True, blank=True)
    tulov_status = models.CharField(max_length=200, choices=TolovStatus, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.nomi} | {self.vaqt} {self.ombor_savdo}"

    class Meta:
        verbose_name = "Moliya chiqim"
        verbose_name_plural = "Moliya chiqim"




