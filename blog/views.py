from django.shortcuts import render, get_object_or_404
from .models import User, Article, Message, File
from django.http import HttpResponseRedirect, FileResponse
from django.urls import reverse
import os
# Create your views here.
PATH = os.getcwd()


def register(request):
    if request.method == 'POST':
        if request.POST['name'] and request.POST['password']:
            s = User(name=request.POST['name'], password=request.POST['password'])
            s.save()
            return HttpResponseRedirect(reverse('blog:private', args=(s.pk, )))
        return HttpResponseRedirect(reverse('blog:register', args=()))
    return render(request, 'blog/register.html')


def index(request):
    all_article = Article.objects.order_by('-pub_date')[:30]
    context = {
        'all_article': all_article,
        'not_is_login': not request.session.get('is_login'),
        'pk': request.session.get('user'),
    }
    return render(request, 'blog/index.html', context=context)


def login(request):
    if request.method == "POST":
        if request.POST['name'] and request.POST['password']:
            try:
                s = User.objects.get(name=request.POST['name'], password=request.POST['password'])
                request.session['is_login'] = True
                request.session['user'] = s.id
                print('You are success...')
                return HttpResponseRedirect(reverse('blog:private', args=(s.id, )))
            except (KeyError, User.DoesNotExist):
                print('failed..')
                return HttpResponseRedirect(reverse('blog:login', args=()))
    return render(request, 'blog/login.html')


def private(request, pk):
    if request.session.get('is_login') and request.session.get('user') == pk:
        s = get_object_or_404(User, pk=pk)
        all_article = s.article_set.order_by('-pub_date')
        context = {
            'user': s,
            'all_article': all_article,
        }
        return render(request, 'blog/private.html', context=context)
    print('enter failed...')
    return HttpResponseRedirect(reverse('blog:login', args=()))


def add_private(request, pk):
    if request.session.get('is_login') and request.session.get('user') == pk:
        user = get_object_or_404(User, pk=pk)
        context = {
            'user': user,
        }
        if request.method == 'POST':
            text = request.POST['text']
            user.article_set.create(text=text)
            return HttpResponseRedirect(reverse('blog:private', args=(pk, )))
        else:
            return render(request, 'blog/add_private.html', context=context)
    else:
        return render(request, 'blog/login.html')


def look_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    context = {
        'article': article,
        'not_is_login': not request.session.get('is_login'),
        'pk': request.session.get('user'),
    }
    return render(request, 'blog/look_article.html', context=context)


def look_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    all_article = user.article_set.all()
    context = {
        'user': user,
        'not_is_login': not request.session.get('is_login'),
        'all_article': all_article,
        'pk': request.session.get('user'),
    }
    return render(request, 'blog/look_user.html', context=context)


def logout(request):
    request.session['is_login'] = False
    request.session['user'] = None
    return HttpResponseRedirect(reverse('blog:index', args=()))


def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.session.get('is_login'):
        if article.user.pk == request.session.get('user'):
            if request.method == "POST":
                text = request.POST['text']
                article = get_object_or_404(Article, pk=pk)
                article.text = text
                article.save()
                return HttpResponseRedirect(reverse('blog:private', args=(article.user.pk, )))
            else:
                context = {
                    'article': article,
                }
                return render(request, 'blog/edit_article.html', context=context)
    return HttpResponseRedirect(reverse('blog:login', args=()))


def send_message(request, pk):
    if request.session.get('user') == pk and request.session.get('is_login'):
        context = {
            'pk': pk,
        }
        if request.method == 'POST':
            if request.POST['msg'] and request.POST['receiver_pk']:
                r = request.POST['receiver_pk']
                msg = request.POST['msg']
                receiver = get_object_or_404(User, pk=r)
                m = receiver.message_set.create(sender_id=pk, msg=msg)
                m.save()
                return HttpResponseRedirect(reverse('blog:private', args=(pk, )))
        return render(request, 'blog/send_message.html', context=context)
    return HttpResponseRedirect(reverse('blog:login', args=()))


def check_login(request, pk):
    return request.session.get('is_login') and request.session.get('user') == pk


def check_message(request, pk):
    user = get_object_or_404(User, pk=pk)
    unread_msg = user.message_set.filter(is_read=False)
    context = {
        'user': user,
        'unread_msg': unread_msg,
    }
    return render(request, 'blog/check_message.html', context=context)


def check_one(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    if request.session.get('is_login') and request.session.get('user') == msg.receiver.pk:
        msg.is_read = True
        msg.save()
        context = {
            'msg': msg,
        }
        return render(request, 'blog/check_one.html', context=context)
    return HttpResponseRedirect(reverse('blog:login', args=()))


def add_file(request, pk):
    if check_login(request, pk):
        if request.method == 'POST':
            file = request.FILES.get('file')
            user = get_object_or_404(User, pk=int(request.POST.get('pk')))
            p = int(request.POST.get('pk'))
            if not file:
                return HttpResponseRedirect(reverse('blog:add_file', args=(pk, )))
            if not os.path.exists('files/' + str(p)):
                os.mkdir('files/' + str(p))
            with open('files/' + str(p) + '/' + file.name, 'wb+') as f:
                for i in file.chunks():
                    f.write(i)
            user.file_set.create(name=file)
            user.save()
            return HttpResponseRedirect(reverse('blog:private', args=(pk, )))
        context = {
            'pk': pk,
        }
        return render(request, 'blog/add_file.html', context=context)
    return HttpResponseRedirect(reverse('blog:login'))


def check_files(request, pk):
    if check_login(request, pk):
        user = get_object_or_404(User, pk=pk)
        all_file = user.file_set.all()
        context = {
            'all_file': all_file,
            'user': user,
        }
        return render(request, 'blog/check_files.html', context=context)
    return HttpResponseRedirect(reverse('blog:login'))


def check_file(request, pk):
    file = get_object_or_404(File, pk=pk)
    if check_login(request, file.user.pk):
        f = get_object_or_404(File, pk=pk)
        file = open(PATH + '/files/' + str(request.session.get('user')) + '/' + f.name, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{filename}"'.format(filename=f.name)
        return response
    return HttpResponseRedirect(reverse('blog:login'))

