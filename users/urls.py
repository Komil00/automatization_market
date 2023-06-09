from rest_framework.routers import DefaultRouter
from django.urls import path,include
from moliya.views import *
from savdo.views import *
from products.views import *



router = DefaultRouter()

router.register('mijoz', MijozViewSet)
router.register('mahsulot', MahsulotlarViewSet)
router.register('mahsulot_olchov', MahsulotOlchovViewSet)
router.register('moliya_chiqim', MoliyaChiqimViewSet)
# router.register('ombor', OmborViewSet)
router.register('ishchi', IshchiViewSet)
router.register('savdo', SavdoViewSet)
router.register('analitika', AnalitikaViewSet)


urlpatterns = [ 
    path("", include(router.urls)),
]






