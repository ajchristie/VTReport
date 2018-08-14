# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from time import sleep
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import VTReport
from .forms import UploadFileForm
from .tasks import get_add_records
from utils.helpers import cache_grab, get_report, prune_and_dummy
# probably need some kind of celery import here too, whatever you need to call tasks



def index(request):

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            hashes = request.FILES['file'].readlines()
            if not hashes: ## empty file
                form = UploadFileForm()
                return render(request, 'index.html', {'form':form, 'error_message': "Your file was empty."})
            else: ## file not empty
                hashes = [line.strip(['\r','\n']) for line in hashes]
                prune(hashes, request.session)
                if hashes: ## still uncached hashes to query
                    error_list = get_add_records.delay(hashes)
                    sleep(1.5) ## allow some queries to complete before display
                return HttpResponseRedirect(reverse('results', {'errors': error_list}))

    else:  ## ie, request.method == GET
        form = UploadFileForm()
        return render(request, 'index.html', {'form': form})



def results(request):
    records = cache_grab(request.session)
    return render(request, 'results.html', {'records': records})
