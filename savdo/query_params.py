
from drf_yasg import openapi


# Savdo query_params

def savdo_query_params():
    savdo_turi = openapi.Parameter(
        "savdo_turi", openapi.IN_QUERY, description="savdo_turi", type=openapi.TYPE_STRING)
    chegirma_turi = openapi.Parameter(
        "chegirma_turi", openapi.IN_QUERY, description="chegirma_turi", type=openapi.TYPE_STRING)
    mijoz = openapi.Parameter(
        "mijoz", openapi.IN_QUERY, description="mijoz", type=openapi.TYPE_STRING)
    vaqt = openapi.Parameter("savdo_vaqt", openapi.IN_QUERY,
                             description="savdo_vaqt format (yyyy-mm-dd)",type=openapi.TYPE_STRING)

    return [savdo_turi,chegirma_turi, vaqt, mijoz]


# Savdo Product query params

def savdopro_query_params():
    
    narx_turi = openapi.Parameter(
        "narx_turi", openapi.IN_QUERY, description="narx_turi", type=openapi.TYPE_STRING)

    mahsulot = openapi.Parameter(
        "mahsulot", openapi.IN_QUERY, description="mahsulot", type=openapi.TYPE_STRING)
    
    
    olchov = openapi.Parameter(
        "olchov", openapi.IN_QUERY, description="olchov", type=openapi.TYPE_STRING)
    
    miqdor = openapi.Parameter(
        "miqdor", openapi.IN_QUERY, description="miqdor", type=openapi.TYPE_STRING)

    narx = openapi.Parameter(
        "narx", openapi.IN_QUERY, description="narx", type=openapi.TYPE_STRING)
    
    sotish_olchov = openapi.Parameter(
        "sotish_olchov", openapi.IN_QUERY, description="sotish_olchov", type=openapi.TYPE_STRING)
   
    total_summa = openapi.Parameter(
        "total_summa", openapi.IN_QUERY, description="total_summa", type=openapi.TYPE_STRING)

    is_active = openapi.Parameter(
        "is_active", openapi.IN_QUERY, description="is_active", type=openapi.TYPE_STRING)

    return [narx_turi, mahsulot,sotish_olchov, olchov,  narx, miqdor, total_summa, is_active]

# Tranzaksiya query_params

def get_tranzaksiya_turi():
    turi = openapi.Parameter("turi ", openapi.IN_QUERY, description="turi", type=openapi.TYPE_STRING)
    return [turi]



# Tolovlar query_params



def tolovlar_query_params():
    savdo = openapi.Parameter(
        "savdo", openapi.IN_QUERY, description="savdo", type=openapi.TYPE_STRING)

    muddat = openapi.Parameter("muddat", openapi.IN_QUERY,
                             description="muddat format (yyyy-mm-dd)",type=openapi.TYPE_STRING)

    tranzaksiya_turi = openapi.Parameter(
        "tranzaksiya_turi", openapi.IN_QUERY, description="tranzaksiya_turi", type=openapi.TYPE_STRING)
    summa = openapi.Parameter(
        "summa", openapi.IN_QUERY, description="summa", type=openapi.TYPE_STRING)

    status = openapi.Parameter(
        "status", openapi.IN_QUERY, description="status", type=openapi.TYPE_STRING)

    yaralgan_sana = openapi.Parameter("yaralgan_sana", openapi.IN_QUERY,
                               description="yaralgan_sana format (yyyy-mm-dd)", type=openapi.TYPE_STRING)

    return [savdo, muddat, summa, status, yaralgan_sana, tranzaksiya_turi]

