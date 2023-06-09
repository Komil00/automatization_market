from django.contrib import admin

from moliya.models import Moliya_chiqim, Omborxona, OmborCategory


class MoliyaChiqimAdmin(admin.ModelAdmin):
    list_display = ['user','vaqt','ombor_id']
    list_per_page = 10
    class Meta:
        model = Moliya_chiqim
admin.site.register(Moliya_chiqim, MoliyaChiqimAdmin)


class OmborxonaAdmin(admin.ModelAdmin):
    list_display = ['kategoriya','mahsulot_nomi', 'miqdor', 'summa', 'vaqt']
    list_per_page = 10
    class Meta:
        model = Omborxona
admin.site.register(Omborxona, OmborxonaAdmin)



class OmborCategoryAdmin(admin.ModelAdmin):
    list_display = ['kategoriya']
    list_per_page = 10
    class Meta:
        model = Omborxona
admin.site.register(OmborCategory, OmborCategoryAdmin)
