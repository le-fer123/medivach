import os
import requests
from bs4 import BeautifulSoup
import tempfile
from django.core.files.base import ContentFile
from .models import Thread, Media


def parsethread(thread):
    soup = BeautifulSoup(requests.get(thread).text, 'html.parser')

    images = soup.find_all('img')
    imglife = []
    imghk = []
    print(images)

    for img in images:
        img_src = img.get('data-src')
        print('parsethread', img_src)
        if img_src:
            imglife.append('https://2ch.life' + img_src)
            imghk.append('https://2ch.hk' + img_src)

    print("Thread parsed successfully")

    return imglife, imghk


def set_media(name, thread, content):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(content)
    temp_file.close()

    with open(temp_file.name, 'rb') as f:
        media = Media.objects.create(
            thread=thread,
            title=name,
            file=ContentFile(f.read(), name=name)
        )

    os.unlink(temp_file.name)
    print("downloaded successfully")

    return True


def recursive_down(imgs, img, thread):
    attempts = 0
    while attempts <= 5:
        mhk = requests.get(imgs[img])
        if mhk.status_code == 200 and mhk.content:
            try:
                print(thread)
                if set_media(imgs[img].split('/')[-1], thread, mhk.content):
                    return True
            except Exception as e:
                print("Error in set media")
                print(e)
                attempts += 1
                continue
        else:
            print("Download Failed", attempts)
        attempts += 1
    print("Download failed")
    return False


def recursive(imgshk, imgslife, thread):
    lost = 0
    for img in range(len(imgshk)):
        if recursive_down(imgshk, img, thread) or recursive_down(imgslife, img, thread):
            continue
        else:
            lost += 1
    return lost


# def down_life(imglife, thread):
#     try:
#         print(imglife)
#         for img in imglife:
#             name = img.split('/')[-1]
#             dimg = requests.get(img).content
#
#             temp_file = tempfile.NamedTemporaryFile(delete=False)
#             temp_file.write(dimg)
#             temp_file.close()
#
#             with open(temp_file.name, 'rb') as f:
#                 media = Media.objects.create(
#                     thread=thread,
#                     title=name,
#                     file=ContentFile(f.read(), name=name)
#                 )
#
#             os.unlink(temp_file.name)
#             print("from life downloaded successfully")
#         else:
#             return True
#
#     except Exception as e:
#         print(f"Произошла ошибка: {e}")
#         return False
#
# def down_hk(imghk, thread):
#     try:
#         for img in imghk:
#             name = img.split('/')[-1]
#             dimg = requests.get(img).content
#
#             temp_file = tempfile.NamedTemporaryFile(delete=False)
#             temp_file.write(dimg)
#             temp_file.close()
#
#             with open(temp_file.name, 'rb') as f:
#                 media = Media.objects.create(
#                     thread=thread,
#                     title=name,
#                     file=ContentFile(f.read(), name=name)
#                 )
#
#             os.unlink(temp_file.name)
#             print("from hk downloaded successfully")
#
#             return True
#
#     except Exception as e:
#         print(f"Произошла ошибка: {e}")
#         return False




























































