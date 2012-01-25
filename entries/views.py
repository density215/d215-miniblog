from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http import HttpResponseServerError, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils import simplejson
from entries.models import Entry

def index(request):
    entries = Entry.objects.filter(publish=True).order_by('-publishdate').order_by('-created')
    return render_to_response('index.html',{ 'ENTRIES':entries, },context_instance = RequestContext(request))

@login_required
def admin(request):
    entries = Entry.objects.all().order_by('-publishdate').order_by('-created')
    return render_to_response('admin.html',{ 'ENTRIES':entries},context_instance = RequestContext(request))

@login_required
def create(request):
    newentry = Entry(headline='<span class="dummy">[Your headline here]</span>',body='<span class="dummy">[Your entry goes here]</span>',author=request.user)
    try:
        newentry.save()
    except IntegrityError:
        return HttpResponse("error")

    return HttpResponseRedirect(reverse('entries.views.admin') )

@login_required
def update(request):
    if request.is_ajax():
        if request.method == 'POST':
            json_data = simplejson.loads(request.raw_post_data)
            try:
                updateentry = get_object_or_404(Entry,pk=json_data['id'])
                if json_data.has_key('publish'):
                    updateentry.publish = not updateentry.publish
                else:
                    updateentry.headline = json_data['headline']
                    updateentry.body = json_data['body']
                updateentry.save()
            except KeyError:
                return HttpResponse(simplejson.dumps({'success':False}),mimetype='application/json')
            return HttpResponse(simplejson.dumps({'success':True}),mimetype='application/json')
    else:
        return HttpResponse(simplejson.dumps({'success':False}),mimetype='application/json')

@login_required
def delete(request):
    if request.is_ajax():
        if request.method == 'POST':
            json_data = simplejson.loads(request.raw_post_data)
            try:
                Entry.objects.get(pk=json_data['id']).delete()
            except ObjectDoesNotExist:
                return HttpResponse(simplejson.dumps({'success':False}),mimetype='application/json')
            return HttpResponse(simplejson.dumps({'success':True}),mimetype='application/json')
    return HttpResponseRedirect(reverse('entries.views.admin'))

