from django.core.cache import cache
from django.shortcuts import render

from disk_app.api import get_public_files
from disk_app.forms import PublicKeyForm
from disk_app.utils import get_file_type


# Функция получения списка файлов с Яндекс.Диска
def file_list_view(request):
    form = PublicKeyForm()
    files = None
    file_type = request.POST.get("type")  # Получаем тип фильтра
    if request.method == "POST":
        form = PublicKeyForm(request.POST)
        if form.is_valid():
            public_key = form.cleaned_data["public_key"]
            cache_key = f"yandex_disk_files_{public_key}"
            # Попробуем получить данные из кэша
            files = cache.get(cache_key)
            if not files:
                data = get_public_files(public_key)
                #  Проверка на наличие файлов в публичной ссылке
                if data and "_embedded" in data:
                    files = data["_embedded"]["items"]
                    # Сохраняем список файлов в кэш на 10 минут
                    cache.set(cache_key, files, timeout=600)
            # Если выбран фильтр, фильтруем файлы по типу
            if file_type:
                files = [f for f in files if get_file_type(f["name"]) == file_type]
    return render(
        request,
        "disk_app/file_list.html",
        {"form": form, "files": files, "file_type": file_type},
    )
