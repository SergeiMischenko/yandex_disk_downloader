from django.shortcuts import render

from disk_app.api import get_public_files
from disk_app.forms import PublicKeyForm


# Create your views here.
def file_list_view(request):
    form = PublicKeyForm()
    files = None
    if request.method == 'POST':
        form = PublicKeyForm(request.POST)
        if form.is_valid():
            public_key = form.cleaned_data['public_key']
            data = get_public_files(public_key)
            #  Проверка на наличие файлов в публичной ссылке
            if data and '_embedded' in data:
                files = data['_embedded']['items']
    return render(request, 'disk_app/file_list.html', {'form': form, 'files': files})