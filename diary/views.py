from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from datetime import date
import math
from diary.forms import PageForm
from diary.models import Page


class IndexView(View):
    def get(self, request):
        pages = Page.objects.all().order_by('-created_at')[:3]
        return render(request, 'index.html', {'page_list' : pages})

class PageCreateView(View):
    def get(self, request):
        form = PageForm()
        return render(request, 'create.html', {'form': form})

    def post(self, request):
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('diary:index')
        return render(request, 'create.html', {'form': form})

class PageListView(View):
    def get(self, request):
        all_pages = Page.objects.order_by('-page_date')
        page_list = self.paginate_queryset(request, all_pages)

        context = {
            'page_list': page_list
        }

        return render(request, 'list.html', context)

    def post(self, request):
        search_word = request.POST.get('search_word', '').strip()
        all_pages = self.get_queryset(search_word)
        page_list = self.paginate_queryset(request, all_pages)

        context = {
            'page_list': page_list,
            'search_word': search_word,
        }

        return render(request, 'list.html', context)

    def get_queryset(self, search_word):
        queryset = Page.objects.order_by('-page_date')
        if search_word:
            queryset = queryset.filter(
                Q(title__icontains=search_word) |
                Q(content__icontains=search_word)
            )
        return queryset

    def paginate_queryset(self, request, queryset, per_page=5):
        """分页处理"""
        paginator = Paginator(queryset, per_page)
        page_number = request.GET.get('page')
        try:
            page_list = paginator.page(page_number)
        except PageNotAnInteger:
            page_list = paginator.page(1)
        except EmptyPage:
            page_list = paginator.page(paginator.num_pages)
        return page_list

class PageDetailView(View):
    def get(self, request, id):
        page = get_object_or_404(Page, pk=id)
        return render(request, 'detail.html', {'page': page})

class PageEditView(View):
    def get(self, request, id):
        page = get_object_or_404(Page, pk=id)
        form = PageForm(instance=page)
        context = {
            'form': form,
            'existing_picture': page.picture if page.picture else None
        }
        return render(request, 'edit.html', context)

    def post(self, request, id):
        page = get_object_or_404(Page, pk=id)
        form = PageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            return redirect('diary:detail', id=id)
        return render(request, 'edit.html', {'form': form})

class PageDeleteView(View):
    def post(self, request, id):
        page = get_object_or_404(Page, pk=id)
        page.delete()
        return redirect('diary:list')