from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from . import models
from . import utils
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.core.cache import cache
from django.core.paginator import Paginator, Page,PageNotAnInteger,EmptyPage


@csrf_exempt
# 博客主页
def index(req):
    return render(req, 'myblog/index.html')


# 登陆页面
@csrf_exempt
def login(req):
    if req.method == 'GET':
        return render(req, 'myblog/login.html')
    elif req.method == 'POST':
        name = req.POST.get('name')
        password = req.POST.get('pwd')
        code = req.POST.get('code')
        if code == req.session['check_code']:
            try:
                print(code)
                models.User.objects.get(name=name, password=password)
                return render(req, 'myblog/index.html')
            except:
                return render(req, 'myblog/login.html')
        else:
            return render(req, 'myblog/login.html')


@csrf_exempt
# 注册页面
def regist(req):
    if req.method == 'GET':
        return render(req, 'myblog/register.html')
    elif req.method == 'POST':
        name = req.POST.get('name')
        password = req.POST.get('pwd')
        avatar = req.FILES['avatar']
        path = 'myblog/images' + avatar.name
        # with open(path, 'wb') as file:
        #     for i in avatar.chunks():
        #         file.write(i)
        try:
            models.User.objects.get(name=name)
            return HttpResponse('<h1>用户名存在</h1>')
        except:
            addreg = models.User(name=name, password=password, avatar=path)
            addreg.save()
            return redirect('myblog:login')

    return render(req, 'myblog/register.html')


@csrf_exempt
# 编辑博客
def article(req):
    if req.method == 'GET':
        return render(req, 'myblog/article.html')
    elif req.method == 'POST':
        title = req.POST.get('title')
        coutext = req.POST.get('coutext')
        author = req .POST.get('user')
        upload = models.Article(title=title, coutext=coutext, author=author)
        upload.save()
    return render(req, 'myblog/index.html')


@csrf_exempt
# 列表页面
def article_list(req):
    # if req.method == 'GET':
    #     print('缓存中获取')
    #     users = cache.get('name')
    #     print(users)
    #     if users is None:
    #         print('数据库查询')
    #         users = models.User.objects.all()
    #         print('存入缓存')
    #         cache.set('name', users)
    #     own = models.Article.objects.all()
    #     context = {'own': own}
    # 使用分页
    article_list1 = models.Article.objects.all().order_by('title')
    print(article_list1)
    pajinator = Paginator(article_list1, 5)

    pagnum = req.GET.get('pagnum')

    try:
        articles = pajinator.page(pagnum)
    except PageNotAnInteger:
        articles=pajinator.page(1)
    except EmptyPage:
        articles=pajinator.page(pajinator.num_pages)

    # title = models.Article.objects.all()
    # pagena = Paginator(title, 200)
    #
    # paga = pagena.page(pagnum)
    return render(req, 'myblog/article_list.html', {'articles': articles})


@csrf_exempt
# 列表详情
def article_detail(req):
    if req.method == 'GET':
        return render(req, 'myblog/article_detail.html')


@csrf_exempt
# 验证码
def addutils(req):
    # 开辟内存空间
    B = BytesIO()
    # 引入utils的产生图片和数字的方法
    img, code = utils.create_code()
    # 保存图片和数字
    req.session['check_code'] = code
    img.save(B, 'PNG')
    return HttpResponse(B.getvalue())


# Create your views here.
@csrf_exempt
def jsontext(req):
    u = models.User.objects.get(pk=13)
    u = model_to_dict(u)
    return JsonResponse(u)
