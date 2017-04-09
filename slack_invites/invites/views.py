import json
import mailchimp
import requests

from django.conf import settings
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
            email = form.cleaned_data['email']
            r = requests.post(
                'https://slack.com/api/users.admin.invite',
                data={
                    'token': settings.SLACK_TOKEN,
                    'email': email,
                }
            )
            if not r.status_code == 200:
                print r.content

            msg = None
            data = json.loads(r.content)
            if 'ok' in data and not data['ok']:
                form.add_error(None, data['error'])
                return render(request, 'index.html', {'form': form, 'msg': msg})
            else:
                mailchimp_api = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
                mailchimp_api.lists.subscribe('29b5ace6f2', {'email': email})
                msg = 'Invite(s) sent to {} for: Slack, Mailchimp'.format(email)

                r = requests.get(
                    'https://civictools.appspot-preview.com/api/v1/invite',
                    params = {
                        'teamId': '-Kd27R2-vkjuWxHEQ23A',
                        'secret': settings.AMPLIFY_SECRET,
                        'email': email
                    }
                )
                if not r.status_code == 200:
                    msg += '\n Something went wrong with sendin the Amplify invite. Please ask the volunteer to take down your email address.'
                else:
                    msg += ', and Amplify'
                form = EmailForm
                return render(request, 'index.html', {'form': form, 'msg': msg})
    else:
        raise Http404('method not allowed')
