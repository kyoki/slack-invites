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

            errors = []
            invites_list = []
            data = json.loads(r.content)
            if 'ok' in data and not data['ok']:
                errors.append(data['error'])
            else:
                invites_list.append('Slack')

            mailchimp_api = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
            try:
                mailchimp_api.lists.subscribe('29b5ace6f2', {'email': email})
                invites_list.append('Newsletter')
            except mailchimp.ListAlreadySubscribedError:
                errors.append('already subscribed to newsletter')

            r = requests.get(
                'https://civictools.appspot-preview.com/api/v1/invite',
                params = {
                    'teamId': '-Kd27R2-vkjuWxHEQ23A',
                    'secret': settings.AMPLIFY_SECRET,
                    'email': email
                }
            )
            if not r.status_code == 200:
                errors.append('Failed to send Amplify invite')
            else:
                invites_list.append('Amplify')
            msg = ''
            if errors:
                msg += 'Errors: {}</br>'.format(', '.join(errors))
            if invites_list:
                msg += 'Invites sent for: {}'.format(', '.join(invites_list))

            form = EmailForm
            return render(request, 'index.html', {'form': form, 'msg': msg})
    else:
        raise Http404('method not allowed')
