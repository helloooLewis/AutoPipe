from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import automodel
from datetime import datetime
import pandas as pd
import zipfile,tempfile,io,os
from wsgiref.util import FileWrapper

def homepage(request):
    posts = automodel.objects.all()
    now = datetime.now()

    #posts_list = list()
    #for it in posts:
    #    posts_list.append(str(it.pk)+'-----'+it.auto_type +'-----'+'【'+it.desc+'】'+"<br>")
    #return HttpResponse(posts_list)
    return render(request, "index.html", locals())

def paForSplit(request):
    desc = automodel.objects.get(pk=4)

    return render(request, "paForSplit.html",{'posts':desc})



def newhomepage(request):
    posts = automodel.objects.all()
    now = datetime.now()
    return render(request, "newindex.html", locals())


def searchexcel(request):
    studentsList = automodel.objects.filter(auto_type__in=['excel'])

    return render(request, 'newindex.html',{'posts':studentsList })


def Form_merge(get_file, num=1):#表格列数据合并
    dfs = []
    for each_file in get_file:
            df = pd.read_excel(each_file)
            dfs.append(df)
    if num ==1:
        df = pd.concat(dfs)
    elif num == 2:
        df = pd.concat(dfs,axis = 1)
    return(df)


def split_sheet(get_file):
    '''
    拆分单个表格中的sheet
    '''

    d_read = pd.read_excel(get_file,None)
    names = d_read.keys()
    # 创建BytesIO
    s = io.BytesIO()
    # 创建一个临时文件夹用来保存下载的文件
    temp = tempfile.TemporaryDirectory()
    # 使用BytesIO生成压缩文件
    zip = zipfile.ZipFile(s, 'w',zipfile.ZIP_DEFLATED)
    for name in names:
        tempsheet = pd.read_excel(get_file, sheetname=name)
        local_path = os.path.join(temp.name, name)
        filename = local_path + name + ".xlsx"
        tempsheet.to_excel(filename, sheet_name=name, index=False)
        # 把下载文件的写入压缩文件
        zip.write(filename,name + ".xlsx")
    # 关闭文件
    zip.close()
    # 指针回到初始位置，没有这一句前端得到的zip文件会损坏
    s.seek(0)
    # 用FileWrapper类来迭代器化一下文件对象，实例化出一个经过更适合大文件下载场景的文件对象，实现原理相当与把内容一点点从文件中读取，
    # 放到内存，下载下来，直到完成整个下载过程。这样内存就不会担心你一下子占用它那么多空间了。
    wrapper = FileWrapper(s)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename={0}.zip'.format('auto_excel')
    return response
    #return HttpResponse(names)

def split_by_colname(get_file,colname):
    '''
    按某列数据拆分表格
    :param get_file: 单个文件
    :param colname: 列名
    :return: 返回分割文件的压缩文件
    '''

    df = pd.read_excel(get_file)
    c_name = colname
    classinformation = df[c_name].unique().tolist()
    # 创建BytesIO
    s = io.BytesIO()
    # 创建一个临时文件夹用来保存下载的文件
    temp = tempfile.TemporaryDirectory()
    # 使用BytesIO生成压缩文件
    zip = zipfile.ZipFile(s, 'w',zipfile.ZIP_DEFLATED)
    for temp_class in classinformation:
        temp_data = df[df[c_name].isin([temp_class])]
        temp_class = str(temp_class)
        local_path = os.path.join(temp.name, temp_class)
        filename = local_path + temp_class + ".xlsx"
        temp_data.to_excel(filename, index=False)
        # 把下载文件的写入压缩文件
        zip.write(filename, temp_class + ".xlsx")
    # 关闭文件
    zip.close()
    # 指针回到初始位置，没有这一句前端得到的zip文件会损坏
    s.seek(0)
    # 用FileWrapper类来迭代器化一下文件对象，实例化出一个经过更适合大文件下载场景的文件对象，实现原理相当与把内容一点点从文件中读取，
    # 放到内存，下载下来，直到完成整个下载过程。这样内存就不会担心你一下子占用它那么多空间了。
    wrapper = FileWrapper(s)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename={0}.zip'.format('auto_excel')
    return response


def all_form_merge(myFile,num):
    outfile = BytesIO()
    excel_data = Form_merge(myFile,num)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    execl_name = 'auto_excel'
    response['Content-Disposition'] = 'attachment;filename={0}.xlsx'.format(execl_name)
    excel_data.to_excel(outfile, index=False)
    response.write(outfile.getvalue())
    return response

#import xlrd
#import xlwt
from io import BytesIO
def uploadtable(request,num):
    if request.method == "POST":    # 请求方法为POST时，进行处理
        if num == 1 or num == 2:
            myFile =request.FILES.getlist("file", None)    # 获取上传的文件，如果没有文件，则默认为None
            if not myFile:
                return HttpResponse("no files for upload!")
            else:
                return all_form_merge(myFile,num)
        if num == 3:
             myFile = request.FILES.get("file", None)
             if not myFile:
                 return HttpResponse("no files for upload!")
             else:
                 return split_sheet(myFile)
        if num == 4:
            myFile = request.FILES.get("file", None)
            colname = request.POST.get("colname")
            if not myFile:
                return HttpResponse("no files for upload!")
            else:
                print(colname)
                return split_by_colname(myFile,colname)
            #return HttpResponse("upload over!")



def p2(request):
    if request.method == "GET":
        return render(request, "p2.html")
    elif request.method == "POST":
        city = request.POST.get("city")
        print(city)
        return render(request, "popup_response.html", {"city": city})