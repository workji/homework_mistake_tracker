from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from diary.forms import PageForm
from diary.models import Page


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

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
        pages = Page.objects.order_by('page_date')
        return render(request, 'list.html', {'page_list': pages})

class PageDetailView(View):
    def get(self, request, id):
        page = get_object_or_404(Page, pk=id)
        return render(request, 'detail.html', {'page': page})

class PageEditView(View):
    def get(self, request, id):
        page = get_object_or_404(Page, pk=id)
        form = PageForm(instance=page)
        return render(request, 'edit.html', {'form': form})

    def post(self, request, id):
        page = get_object_or_404(Page, pk=id)
        form = PageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            return redirect('diary:detail', id=id)
        return render(request, 'edit.html', {'form': form})

class PageDeleteView(View):
    def get(self, request, id):
        page = get_object_or_404(Page, pk=id)
        return render(request, 'delete.html', {'page': page})

    def post(self, request, id):
        page = get_object_or_404(Page, pk=id)
        page.delete()
        return redirect('diary:list')