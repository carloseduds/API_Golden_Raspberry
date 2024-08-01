from django.urls import path

from .views import ler_filmes, ler_intervalos_premios, upload_arquivo

urlpatterns = [
    path("uploadarquivo/", upload_arquivo, name="upload-arquivo"),
    path("filmes/", ler_filmes, name="ler-filmes"),
    path("vencedores/intervalos/", ler_intervalos_premios,
         name="ler-intervalos-premios"),
]
