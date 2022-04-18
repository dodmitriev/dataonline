from django.shortcuts import render
from django.db import models
from django.http import *
import pymysql
import os
import urllib.request
import xml.dom.minidom
from .forms import cpEditForm
from .forms import cpSearchForm
from .forms import cpLoadFile
from django.contrib import auth
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from pytils import translit
from django.http import JsonResponse
from django.core.serializers import serialize
from .models import CodesDirectory
from .models import Phonebook
import requests
import json
from urllib.parse import parse_qs
from django.db.models import Q
import urllib.parse
from django.db.models import Count
from . import common

def testjs(request):
    return  HttpResponse("Hello, World")
    # return render(request, 'testjs.html')

# def parseRequest(request):
#
#     # было изначально так
#     # dt2 = request.body
#     # dt = str(dt2)[2:][:-1]
#     # data = parse_qs(dt)
#
#     # dt2 = request.body
#     # dt3 = dt2.decode()
#     # data = parse_qs(dt3)
#
#     # dt2 = request.body
#     # dt3 = dt2.decode()
#
#     # т.к. request.body возвращается в формате b'request.body' то методом decode() отсекаем b
#
#     data = parse_qs((request.body).decode())
#
#     # упростил так
#     # data = parse_qs(str(request.body)[2:][:-1])
#     #
#     # после разбора data получается в таком виде
#     # {'cgroup': ['DJANGO389'], 'header': ['test POST REST API389'], 'description': ['\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435389'], 'link': ['0'], 'csrfmiddlewaretoken': ['3blhZ0jxMujkfKCbhsIIctSGi9OMkilNZ27Xn7JfddhSt5ui4d4kVIk9vmFH59mD']}
#     # т.е. parse_qs возвращает словарь, где ключи - это уникальные имена переменных запроса, а значения - это списки значений для каждого имени
#     # есть еще функция parse_qsl - возвращает писок кортежей типа [(key, value), (key, value), ...]. Например [('product', 'смартфоны'), ('s', '9'), ('v', '5'), ('v', '15'), ('t', '')]
#
#     # data = parse_qs(str(request.body)[2:][:-1])
#     # data = parse_qs(str(request.body).decode())
#     return data

# REST API
# ********************
# PUT       - обновить
# DELETE    - удалить
# POST      - вставить
# GET       - получить
# HEAD
# PATCH
# OPTIONS


# ОБНОВИТЬ
def put(request):
    # CSRF защита отключена

    #отладочнй проект - testput
    #исходник проекта:

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # это адрес по которому DJANGO отработает put
    # URL = 'http://a91391d8.beget.tech/put/'
    # client = requests.session()
    # changedata = {'id_codesdir': 819, 'cgroup': 'DJANGO39', 'header': 'test POST REST API 876',
    #               'description': 'qwertyui'}
    # r = client.put(URL, data=changedata)
    #
    # print(r.status_code)
    # print(r.request.body)
    # print(r.text)  # это возвращает сервер - return JsonResponse...
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    try:
        data = common.parseRequest(request)
    except:
        return JsonResponse({'message': f'Error data loading', 'requestbody': str(dt2)}, status = 201)


    try:
        id_codesdir2 = int(data['id_codesdir'][0])
        cgroup2 = data['cgroup'][0]
        header2 = data['header'][0]
        description2 = data['description'][0]


    except:
        return JsonResponse({'message': f'Error data parsing'}, status=201)


    forupdate = CodesDirectory.objects.get(id_codesdir=id_codesdir2)
    forupdate.cgroup = cgroup2
    forupdate.header = header2
    forupdate.description = description2
    forupdate.save()

    data2 = {'test': id_codesdir2}
    return JsonResponse(data2, status=201)

# УДАЛИТЬ
def delete(request):
    # CSRF защита отключена

    #отладочнй проект - testdel
    #исходник проекта:

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # это адрес по которому DJANGO отработает delete
    # URL = 'http://a91391d8.beget.tech/delete/'
    # client = requests.session()
    # condition = dict(id_codesdir=820)
    # r = client.delete(URL, data=condition)
    #
    # print(r.status_code)
    # print(r.request.body)
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    try:
        data = common.parseRequest(request)
    except:
        return JsonResponse({'message': f'Error data loading', 'requestbody': str(dt2)}, status = 201)


    try:
        id_codesdirdict = data['id_codesdir']
        id_codesdir2 = int(id_codesdirdict[0])

    except:
        return JsonResponse({'message': f'Error data parsing'}, status=201)

    fordel = CodesDirectory.objects.get(id_codesdir = id_codesdir2)
    fordel.delete()

    data = {'message': f'Data deleted', 'requestbody': str(dt2)}

    return JsonResponse(data, status = 201)

# ДОБАВИТЬ
def post(request):

    #отладочнй проект - testpost
    #исходник проекта:

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # с токеном
    # # это login страница моего сайта, с нее будет получен CSRF токен
    # URL_LOGIN = 'http://a91391d8.beget.tech/accounts/login//'
    # # это адрес по которому DJANGO отработает post
    # URL = 'http://a91391d8.beget.tech/post/'
    #
    # client = requests.session()
    # client.get(URL_LOGIN)
    # csrftoken = client.cookies['csrftoken']
    # print(csrftoken)
    #
    # insdata = dict(cgroup='DJANGO777', header='test POST REST API77', description='Описание777', link='0',
    #                csrfmiddlewaretoken=csrftoken)
    # r = client.post(URL, data=insdata, headers=dict(Referer=URL))
    #
    # print(r.status_code)
    # print(r.request.body)
    # print(r.text)  # это возвращает сервер - return JsonResponse...

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # без токена
    # URL = 'http://a91391d8.beget.tech/post/'
    #
    # client = requests.session()
    #
    # insdata = dict(cgroup='DJANGO777', header='test POST REST API77', description='Описание777', link='0')
    # r = client.post(URL, data=insdata, headers=dict(Referer=URL))
    #
    # print(r.status_code)
    # print(r.request.body)
    # print(r.text)  # это возвращает сервер - return JsonResponse...

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    try:
        data = common.parseRequest(request)

    except:
        return JsonResponse({'message': f'Error data loading', 'requestbody': request.body}, status = 201)


    try:
        dataforload = {
            'cgroup': data['cgroup'][0],
            'header': data['header'][0],
            'description': data['description'][0],
            'link': data['link'][0],
        }

    except:
        return JsonResponse({'message': f'Error data parsing'}, status=201)


    codes_obj = CodesDirectory.objects.create(**dataforload)

    data2 = {
         'message': f'New record add with id {codes_obj.id_codesdir}'
    }

    return JsonResponse(data2, status = 201)


# это образец загрузки одного файла
def post_file(request):

    myfile = request.FILES['file']

    with open('/home/a/a91391d8/dataonline/public_html/static/images/' + myfile.name, 'wb') as dest:
        for chunk in myfile.chunks():
            dest.write(chunk)

    data = {'byfilter': '111222333'}
    return JsonResponse(data, status=201)


# ПОЛУЧИТЬ
# get - это эталон, реально не использется, на его основе можно создавать дальнейшие gat_
def get(request):

    # substr = request.GET.get('search')
    substr = 'открыть222222'
    counter = -1

    fl = Q(link=0) & (Q(header__icontains=substr) | Q(description__icontains=substr))
    dataforedit = CodesDirectory.objects.filter(fl)  # __incontains - аналог LIKE без учета регистра
    cnt = dataforedit.count()
    # dataforedit = CodesDirectory.objects.filter(Q(link=0) & (Q(header__icontains = substr) | Q(description__icontains = substr)))  # __incontains - аналог LIKE без учета регистра

    data_serialized = serialize('python', dataforedit)

    selecteddata = list()
    onerecord = {}

    for item in data_serialized:

        onerecord = {}

        modelfields = item['fields']

        onerecord['id_codesdir'] = item['pk']
        onerecord['cgroup'] = modelfields['cgroup']
        onerecord['header'] = modelfields['header']
        onerecord['description'] = modelfields['description']
        onerecord['link'] = modelfields['link']
        onerecord['filename'] = modelfields['filename']

        selecteddata.append(onerecord)

    data = {'cnt' : cnt, 'byfilter': selecteddata}

    return JsonResponse(data, status=201)


# выбрать список групп (колонка слева)
def get_cgroup(request):

    # values() возвращает словари Python вместо объекта QuerySet
    # SELECT cgroup FROM HelloDjango_codesdirectory
    # dataforedit = CodesDirectory.objects.values('cgroup')

    # SELECT cgroup FROM HelloDjango_codesdirectory order by cgroup
    # dataforedit = CodesDirectory.objects.values('cgroup').order_by('cgroup')

    # SELECT cgroup FROM HelloDjango_codesdirectory group by cgroup order by cgroup
    dataforedit = CodesDirectory.objects.values('cgroup').annotate(total=Count('id_codesdir')).order_by('cgroup')

    selecteddata = list()
    #
    for item in dataforedit:
            selecteddata.append(item)

    data = {'byfilter': selecteddata}
    return JsonResponse(data, status=201)


# выбрать часто используемые
def get_popular(request):

    dataforedit = CodesDirectory.objects.raw('select * from popular;')

    data_serialized = serialize('python', dataforedit)

    selecteddata = list()

    for item in data_serialized:
        onerecord = {}

        modelfields = item['fields']

        onerecord['id_codesdir'] = item['pk']
        onerecord['cgroup'] = modelfields['cgroup']
        onerecord['header'] = modelfields['header']
        onerecord['description'] = modelfields['description']

        selecteddata.append(onerecord)

    data = {'byfilter': selecteddata}

    return JsonResponse(data, status=201)


# выбрать по указанной группе
def get_by_group(request):

    substr = request.GET.get('search')
    lnk = request.GET.get('lnk')
    counter = -1

    # sql = "SELECT * FROM HelloDjango_codesdirectory WHERE link = 0 and cgroup = '" + cgroupname + "' order by header"
    fl = Q(link=lnk) & Q(cgroup=substr)
    dataforedit = CodesDirectory.objects.filter(fl).order_by('header')
    cnt = dataforedit.count()

    data_serialized = serialize('python', dataforedit)

    selecteddata = list()

    for item in data_serialized:
        onerecord = {}

        modelfields = item['fields']

        onerecord['id_codesdir'] = item['pk']
        onerecord['cgroup'] = modelfields['cgroup']
        onerecord['header'] = modelfields['header']
        onerecord['description'] = modelfields['description']
        onerecord['link'] = modelfields['link']
        onerecord['filename'] = modelfields['filename']

        selecteddata.append(onerecord)

    data = {'cnt' : cnt, 'byfilter': selecteddata}

    return JsonResponse(data, status=201)


# выбрать по указанному фильтру (по нажатию кнопки ПОИСК)
def get_by_filter(request):

        substr = request.GET.get('search')
        lnk = request.GET.get('lnk')
        counter = -1

        # SELECT * FROM `HelloDjango_codesdirectory` WHERE link = 0 and (HEADER like '%" + sl + "%' or description like '%" + sl + "%')
        fl = Q(link=lnk) & (Q(header__icontains=substr) | Q(description__icontains=substr)) # __incontains - аналог LIKE без учета регистра
        dataforedit = CodesDirectory.objects.filter(fl)
        cnt = dataforedit.count()

        data_serialized = serialize('python', dataforedit)

        selecteddata = list()

        for item in data_serialized:
            onerecord = {}

            modelfields = item['fields']

            onerecord['id_codesdir'] = item['pk']
            onerecord['cgroup'] = modelfields['cgroup']
            onerecord['header'] = modelfields['header']
            onerecord['description'] = modelfields['description']
            onerecord['link'] = modelfields['link']
            onerecord['filename'] = modelfields['filename']

            selecteddata.append(onerecord)

        data = {'cnt' : cnt, 'byfilter': selecteddata}

        return JsonResponse(data, status=201)

    # substr = request.GET.get('search')
    # counter = -1
    #
    # try:
    #
    #     dataforedit = CodesDirectory.objects.filter(Q(link=0) & (Q(header__icontains = substr) | Q(description__icontains = substr)))  # __incontains - аналог LIKE без учета регистра
    #
    #     if bool(dataforedit):
    #         datac = {'data': 'IS data'}
    #     else:
    #         datac = {'data': 'NO data'}
    #
    #     data = {'datac': datac, 'byfilter': 'byfilter'}
    #
    # except:
    #     data = {'datac': datac, 'error': 'error data loading'}
    #     return JsonResponse(data, status=201)
    #
    #
    # try:
    #     data_serialized = serialize('python', dataforedit)
    # except:
    #     data = {'datac': datac, 'error': 'error data_serialized'}
    #     return JsonResponse(data, status=201)
    #
    #
    # try:
    #
    #     selecteddata = list()
    #     onerecord = {}
    #
    #     for item in data_serialized:
    #
    #         onerecord = {}
    #
    #         modelfields = item['fields']
    #
    #         onerecord['id_codesdir'] = item['pk']
    #         onerecord['cgroup'] = modelfields['cgroup']
    #         onerecord['header'] = modelfields['header']
    #         onerecord['description'] = modelfields['description']
    #         onerecord['link'] = modelfields['link']
    #         onerecord['filename'] = modelfields['filename']
    #
    #         selecteddata.append(onerecord)
    #
    #     data = {'byfilter': selecteddata}
    #
    #     return JsonResponse(data, status=201)
    # except:
    #     data = {'datac': datac, 'error': 'error data_serialized'}
    #     return JsonResponse(data, status=201)














    #отладочнй проект - testpost
    #исходник проекта:

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # это адрес по которому DJANGO отработает get
    # URL = 'http://a91391d8.beget.tech/get/'
    #
    # client = requests.session()
    #
    # condition = {'search': 'открыть форму'}
    # r = client.get(URL, params=condition)
    #
    # print(r.url)
    # print(r.text)  # это возвращает сервер - return JsonResponse...
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # searchline = request.GET.get("search")
    #
    # count = CodesDirectory.objects.count()
    # alldata = CodesDirectory.objects.all()
    #
    # f1 = alldata.filter(header__iexact = searchline) # аналог LIKE в SQL
    # f2 = alldata.filter(description__iexact=searchline)  # аналог LIKE в SQL
    #
    # f1_serialized = serialize('python', f1)
    # f2_serialized = serialize('python', f2)
    #
    # alldata_serialized = f1_serialized + f2_serialized
    #
    # data = {'searchline':searchline, 'all':alldata_serialized, 'cnt':count}
    #
    # return JsonResponse(data)

    # *********************************************************************************************************************************************************************

    # Это GET напрямую к БД через select - работает !!!
    # через модель пока не получается - необходимо разобраться как сделсть нечто подобное LIKE в SQL
    # searchline = request.GET.get("search")
    # connection = pymysql.connect(host='localhost', user='a91391d8_db', password='GG4ibz13', db='a91391d8_db', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    # cursor = connection.cursor()
    # sql = "SELECT * FROM `HelloDjango_codesdirectory` WHERE  (HEADER like '%" + searchline + "%' or description like '%" + searchline + "%')"
    # cursor.execute(sql)
    # result = cursor.fetchall()
    # data = {'searchline': searchline, 'all': result}
    # return JsonResponse(data)

    # *********************************************************************************************************************************************************************

    # Это GET напрямую к БД через модель, получить все данные - работает !!!
    # count = CodesDirectory.objects.count()
    # alldata = CodesDirectory.objects.all()
    # alldata_serialized = serialize('python', alldata)
    # data = {'all':alldata_serialized, 'cnt':count}
    #
    # return JsonResponse(data)

    # *********************************************************************************************************************************************************************

    # # Это GET напрямую к БД через модель, получить данные по указанному ID через фильтр - работает !!!
    # count = CodesDirectory.objects.count()
    # # alldata = CodesDirectory.objects.all().filter(id_codesdir=137)
    # alldata = CodesDirectory.objects.all().filter(cgroup = 'VB.NET')
    # alldata_serialized = serialize('python', alldata)
    # data = {'all':alldata_serialized, 'cnt':count}
    #
    # return JsonResponse(data)

    # *********************************************************************************************************************************************************************

    # Это GET напрямую к БД через модель, получить данные по указанному ID через objects.get (пока удалось сделать для одной записи) - работает !!!
    # count = CodesDirectory.objects.count()
    # alldata = CodesDirectory.objects.get(id_codesdir=137)
    #
    # alldata_serialized = []  # to store serialized data
    #
    # alldata_serialized.append ({
    #     'cgroup' : alldata.cgroup,
    #     'header' : alldata.header,
    #     'description' : alldata.description
    #     })
    #
    # data = {'all':alldata_serialized, 'cnt':count}
    #
    # return JsonResponse(data)

    # *********************************************************************************************************************************************************************

    # return render(request, 'testany.html', {"crlist": alldata_serialized})






