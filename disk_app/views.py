from django.shortcuts import render

from disk_app.api import get_public_files
from disk_app.forms import PublicKeyForm
from disk_app.utils import get_file_type


# Create your views here.
def file_list_view(request):
    form = PublicKeyForm()
    files = None
    file_type = request.POST.get('type')  # Получаем тип фильтра
    if request.method == 'POST':
        form = PublicKeyForm(request.POST)
        if form.is_valid():
            public_key = form.cleaned_data['public_key']
            data = get_public_files(public_key)
            #  Проверка на наличие файлов в публичной ссылке
            if data and '_embedded' in data:
                files = data['_embedded']['items']

                # Если выбран фильтр, фильтруем файлы по типу
                if file_type:
                    files = [f for f in files if get_file_type(f['name']) == file_type]
    return render(request, 'disk_app/file_list.html', {'form': form, 'files': files, 'file_type': file_type})
