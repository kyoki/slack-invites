import json
import requests

from django.http import Http404
from django.shortcuts import render

from forms import EmailForm


def index(request):
    if request.method == 'GET':
        form = EmailForm()
        return render(request, 'index.html', {'form': form})
    elif request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            r = requests.post(
                'https://slack.com/api/users.admin.invite',
                data={
                    'token': '<SLACK_LEGACY_API_TOKEN>',
                    'email': form.cleaned_data['email'],
                }
            )
            if not r.status_code == 200:
                print r.content
                
            msg = None
            data = json.loads(r.content)
            if 'ok' in data and not data['ok']:
                form.add_error(None, data['error'])
            else:
                msg = 'Invite sent to {}'.format(form.cleaned_data['email'])
                form = EmailForm()
            return render(request, 'index.html', {'form': form, 'msg': msg})
    else:
        raise Http404('method not allowed')
