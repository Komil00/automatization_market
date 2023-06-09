from django.contrib import admin

from savdo.models import Savdo, SavdoProduct, Tolovlar, Tranzaksiya


class TolovlarInline(admin.TabularInline):  # noqa
    model = Tolovlar
    extra = 1
    readonly_fields = ('yaralgan_sana',)  # noqa


admin.site.register(Tolovlar)


class SavdoProductInline(admin.TabularInline):  # noqa
    model = SavdoProduct
    extra = 1
    readonly_fields = ('total_summa',)


class SavdoAdmin(admin.ModelAdmin):  # noqa
    inlines = [TolovlarInline, SavdoProductInline, ]
    list_display = ['savdo_turi', 'user', 'mijoz', 'vaqt']  # noqa
    readonly_fields = ('savdo_turi', 'user')  # noqa

    class Meta:
        model = Savdo


admin.site.register(Savdo, SavdoAdmin)


# Savdo Many Admin
class SavdoProductAdmin(admin.ModelAdmin):  # noqa
    list_display = ['mahsulot', 'miqdor', 'narx_turi', 'umumiy']  # noqa

    class Meta:
        model = SavdoProduct


admin.site.register(SavdoProduct, SavdoProductAdmin)


# Tranzaksiya admin
class TranzaksiyaInline(admin.TabularInline):  # noqa
    model = Tranzaksiya
    extra = 1
    readonly_fields = ('yaralgan_sana',)  # noqa

    class Meta:
        model = Tranzaksiya


admin.site.register(Tranzaksiya)