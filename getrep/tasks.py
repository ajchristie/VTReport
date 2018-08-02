from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
from time import sleep
#from importlib import import_module
from VTReport.settings import api_key
#from django.conf import settings
from getrep.models import VTReport


@shared_task
def get_add_records(hashlist):
    """ Queries VirusTotal for the hashes contained in hashlist and adds them to the cache database. Any errors are stored in a list and returned.

    """
    errlist = []
    for loop, x in enumerate(hashlist):
        params = {'apikey': api_key, 'resource': x}
        try:
            response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params, proxies=None)
        except requests.RequestException as e:
            errlist.append(str(e))
        VTReport.objects.get(hashtype(x)=x).update()
        # need to add rate-limiting handling here? If we just have one worker, probs not
        rec = make_rec(response.json())
        rec.save()

    return errlist
