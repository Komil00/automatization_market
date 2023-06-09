from drf_yasg import openapi


# Moliya kirim query params
def moliya_kirim_query_params():
    query_params = {
        "tranzaksiya_turi": "tranzaksiya_turi uchun",
        "mijoz": "mijoz id si",
        "description": "description",
        "savdo": "savdo",
        "muddat": "muddat format (yyyy-mm-dd)",
        "summa": "summa",
        "status": "status",
        "yaralgan_sana": "yaralgan_sana format (yyyy-mm-dd)",
    }

    return [
        openapi.Parameter(name, openapi.IN_QUERY, description=desc, type=openapi.TYPE_STRING)
        for name, desc in query_params.items()
    ]


# Moliya chiqim query params
def moliya_chiqim_query_params():
    param_list = [
        ("nomi", "nomi uchun"),
        ("tranzaksiya_turi", "tranzaksiya_turi uchun"),
        ("mijoz", "mijoz id si"),
        ("hodim", "hodim uchun"),
        ("mahsulot", "mahsulot uchun"),
        ("olchov", "olchov uchun"),
        ("tolov_turi", "tolov_turi uchun"),
        ("summa", "summa"),
        ("vaqt", "vaqt"),
        ("description", "description"),
        ("ombor_id", "ombor_id")
    ]

    return [openapi.Parameter(name, openapi.IN_QUERY, description=desc, type=openapi.TYPE_STRING)
            for name, desc in param_list]

# Ombor Category query params

def ombor_category_query_params():
    query_params = [
        ("kategoriya", "kategoriya uchun"),
    ]

    return [openapi.Parameter(name, openapi.IN_QUERY, description=desc, type=openapi.TYPE_STRING)
            for name, desc in query_params]


# Omborxona query params
def omborxona_query_params():
    query_params = [
        ("savdo_turi", "ombor savdo_turi"),
        ("kategoriya_ombor", "kategoriya_ombor"),
        ("mahsulot_nomi", "ombor mahsulot_nomi"),
        ("olchov", "ombor olchov"),
        ("total_summa", "total_summa"),
        ("summa", "summa"),
        ("miqdor", "miqdor"),
        ("narx_turi", "narx_turi"),
        ("ombor_vaqt", "ombor_vaqt format (yyyy-mm-dd)")
    ]

    return [openapi.Parameter(name, openapi.IN_QUERY, description=desc, type=openapi.TYPE_STRING)
            for name, desc in query_params]


# Tranzaksiya turi
def get_tranzaksiya_turi():
    return [openapi.Parameter("turi", openapi.IN_QUERY, description="turi", type=openapi.TYPE_STRING)]
