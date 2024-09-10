import os

import requests


# Функция получения списка файлов с Яндекс.Диска по API
def get_public_files(public_key: str) -> dict:
    yandex_disk_token: str = os.getenv("YANDEX_DISK_TOKEN")
    url: str = (
        f"https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_key}"
    )
    headers: dict = {"Authorization": f"OAuth {yandex_disk_token}"}
    response: requests = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
