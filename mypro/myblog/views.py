from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from . import models
from . import utils
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.core.cache import cache
from django.core.paginator import Paginator, Page, PageNotAnInteger, EmptyPage


# 第一要进入的博客页面
def index1(req):
    return render(req,'myblog/index1.html')


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
                user = models.User.objects.get(name=name, password=password)
                req.session['user'] = user.id

                return render(req, 'myblog/index.html')
            except:
                return render(req, 'myblog/login.html', )
        else:
            return render(req, 'myblog/login.html', {'mas': '验证码或密码错误'})


@csrf_exempt
# 注册页面
def regist(req):
    if req.method == 'GET':
        return render(req, 'myblog/register.html')
    elif req.method == 'POST':
        name = req.POST.get('name')
        password = req.POST.get('pwd')
        avatar = req.FILES['avatar']
        path = 'myblog/img' + avatar.name
        # with open(path, 'wb') as file:
        #     for i in avatar.chunks():
        #         file.write(i)
        try:
            models.User.objects.get(name=name)
            return render(req, 'myblog/register.html', {'mas': '账号存在'})
        except:
            addreg = models.User(name=name, password=password, avatar=path)
            addreg.save()
            return redirect('myblog:login')

    return render(req, 'myblog/register.html')


# 更改密码
def lastpwd(req):
    if req.method == 'GET':
        return render(req, 'myblog/lastpwd.html')
    elif req.method == 'POST':
        name = req.POST.get("name")
        pwd = req.POST.get("pwd")
        newpwd = req.POST.get("newpwd")
        print(pwd, newpwd)
        try:
            models.User.objects.get(name=name, password=pwd)
            models.User.objects.filter(password=pwd, name=name).update(password=newpwd)
            return redirect('myblog:login')
        except:
            return render(req, 'myblog/lastpwd.html')

    # try:
    #     models.User.objects.get(name=name)
    #     models.User.objects.filter(password=password).update(password=newpassword)
    #     return HttpResponse('哈哈')
    # except:
    #     return HttpResponse('哈哈')


@csrf_exempt
# 编辑博客
def article(req):
    if req.method == 'GET':
        return render(req, 'myblog/article.html')
    elif req.method == 'POST':
        title = req.POST.get('title')
        coutext = req.POST.get('coutext')
        author = req.POST.get('author')
        upload = models.Article(title=title, coutext=coutext, author=author, user_id=req.session.get('user'))
        upload.save()
    return render(req, 'myblog/index.html')


# 删除博客
def article_del(req):
    if req.method == 'GET':
        return render(req, 'myblog/article_del.html')
    elif req.method == 'POST':
        title = req.POST.get('title')
        author = req.POST.get('author')
        try:
            models.Article.objects.get(title=title, author=author)
            article = models.Article.objects.get(id=id, author=author, title=title)
            article.delete()
            return HttpResponse('1')
        except:
            return HttpResponse('2')


@csrf_exempt
# 列表页面
def article_list(req):
    # if req.method == 'GET':
    #     #     print('缓存中获取')
    #     #     tit = cache.get('title')
    #     #     print(tit)
    #     #     if tit is None:
    #     #         print('数据库查询')
    #     #         users = models.Article.objects.all()
    #     #         print('存入缓存')
    #     #         cache.set('name', users)
    #     #     own = models.Article.objects.all()
    #     #     context = {'own': own}
    # 使用分页
    article_list1 = models.Article.objects.all()
    pagnum = req.GET.get('pagnum')
    pajinator = Paginator(article_list1, 1)
    # articles = models.Article.objects.all()
    try:
        articles = Paginator.page(pajinator, pagnum)
    except PageNotAnInteger:
        articles = pajinator.page(1)
    except EmptyPage:
        articles = pajinator.page(pajinator.num_pages)
    return render(req, 'myblog/article_list.html', {'articles': articles})


def article_detele(req):
    id = req.GET.get('sid')
    article = models.Article.objects.get(pk=id)
    article.delete()
    return redirect('myblog:article_list')


# 修改博客
@csrf_exempt
def updata_article(req):
    if req.method == 'GET':
        id = req.GET.get('sid')
        print(id)
        art = models.Article.objects.get(pk=id)
        print(art)
        # req.session['art']=id 用session方法 存储ID
        return render(req, 'myblog/updata_article.html', {'art': art})
    elif req.method == 'POST':
        id = req.POST.get('sid')
        newtitle = req.POST.get('title')
        newauthor = req.POST.get('author')
        newcoutext = req.POST.get('coutext')
        art = models.Article.objects.get(pk=id)
        # id=req.session.get('id') #session 方法获取到存储在session 的id
        print(id)
        art.title = newtitle
        art.author = newauthor
        art.coutext = newcoutext
        art.save()
        articleid = art.user_id
        return redirect('myblog:index')


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
