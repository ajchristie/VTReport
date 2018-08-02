# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from time import sleep
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import VTReport
from .forms import UploadFileForm
from .tasks import get_add_records
from utils.helpers import cache_grab, get_report, get_is, prune_and_dummy
# probably need some kind of celery import here too



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
                request.session['hashlist'].extend(hashes) ## session dict contains all hashes submitted across session
                prune_and_dummy(hashes) ## remove hashes with cached records
                if hashes: ## still uncached hashes to query
                    get_add_records.delay(hashes)
                return HttpResponseRedirect(reverse('results'))

    else:  ## ie, request.method == GET
        form = UploadFileForm()
        return render(request, 'index.html', {'form': form})



def results(request):

    records = cache_grab(request.session['hashlist'])
    ## make the records pairs if session isn't accessible in template
    return render(request, 'results.html', {'records': records})
