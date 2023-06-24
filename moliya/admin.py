from django.contrib import admin

from moliya.models import Moliya_chiqim, Omborxona, Omborxona_Get


class MoliyaChiqimAdmin(admin.ModelAdmin):
    list_display = ['user','vaqt','ombor_savdo']
    list_per_page = 10
    class Meta:
        model = Moliya_chiqim
admin.site.register(Moliya_chiqim, MoliyaChiqimAdmin)


class OmborxonaAdmin(admin.ModelAdmin):
    list_display = ['mahsulot', 'miqdor', 'summa', 'vaqt']
    list_per_page = 10
    class Meta:
        model = Omborxona
admin.site.register(Omborxona, OmborxonaAdmin)
admin.site.register(Omborxona_Get)
