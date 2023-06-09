from drf_yasg import openapi

def mahsulot_olchov_query_params():
    olchov = openapi.Parameter("olchov", openapi.IN_QUERY, description="olchov", type=openapi.TYPE_STRING)
    narx = openapi.Parameter("narx", openapi.IN_QUERY, description="narx", type=openapi.TYPE_STRING)
    mahsulot_number = openapi.Parameter("mahsulot_number", openapi.IN_QUERY,
                                        description="mahsulot_number", type=openapi.TYPE_INTEGER)

    return [olchov, narx, mahsulot_number]


def mahsulot_query_params():

    mahsulot_nomi = openapi.Parameter(
        "mahsulot_nomi", openapi.IN_QUERY, description="mahsulot_nomi", type=openapi.TYPE_STRING)
    mahsulot_format = openapi.Parameter(
        "mahsulot_format", openapi.IN_QUERY, description="mahsulot_format", type=openapi.TYPE_STRING)

    return [mahsulot_nomi, mahsulot_format]


def mijoz_query_params():
    mijoz = openapi.Parameter("mijoz", openapi.IN_QUERY,
                             description="nomi", type=openapi.TYPE_STRING)
    ism_sharif = openapi.Parameter(
        "ism_sharif", openapi.IN_QUERY, description="ism_sharif", type=openapi.TYPE_STRING)

    telefon = openapi.Parameter(
        "telefon", openapi.IN_QUERY, description="telefon", type=openapi.TYPE_STRING)
    is_con = openapi.Parameter(
        "is_con", openapi.IN_QUERY, description="is_con", type=openapi.TYPE_STRING)
    vaqt = openapi.Parameter("mijoz_sana", openapi.IN_QUERY,
                                      description="mijoz_sana format (yyyy-mm-dd)",
                                      type=openapi.TYPE_STRING)
    return [mijoz, ism_sharif, telefon,is_con, vaqt]




def ishchi_query_params():
    lavozim = openapi.Parameter(
        "lavozim", openapi.IN_QUERY, description="lavozim", type=openapi.TYPE_STRING)
    ism_sharif = openapi.Parameter(
        "ism_sharif", openapi.IN_QUERY, description="ism_sharif", type=openapi.TYPE_STRING)

    telefon = openapi.Parameter(
        "telefon", openapi.IN_QUERY, description="telefon", type=openapi.TYPE_STRING)


    return [ism_sharif, lavozim, telefon]




def analitika_query_params():
    count = openapi.Parameter(
        "count", openapi.IN_QUERY, description="count", type=openapi.TYPE_STRING)
    nom = openapi.Parameter(
        "nom", openapi.IN_QUERY, description="nom", type=openapi.TYPE_STRING)
    return [count,nom]