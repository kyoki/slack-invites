import json
import mailchimp
import requests

from django.conf import settings
from django.contrib.auth import authenticate, login as login_action
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
\
from forms import EmailForm, LoginForm

@login_required
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
                errors.append('Slack: {}'.format(data['error']))
            else:
                invites_list.append('Slack')

            mailchimp_api = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
            try:
                mailchimp_api.lists.subscribe('29b5ace6f2', {'email': email})
                invites_list.append('Newsletter')
            except mailchimp.ListAlreadySubscribedError:
                errors.append('Already subscribed to newsletter')

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
                msg += '{}</br>'.format(', '.join(errors))
            if invites_list:
                msg += 'Invite(s) sent for: {}'.format(', '.join(invites_list))

            form = EmailForm
            return render(request, 'index.html', {'form': form, 'msg': msg})
    else:
        raise Http404('method not allowed')

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login_action(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html', {'form': form})
    else:
        raise Http404('method not allowed')
