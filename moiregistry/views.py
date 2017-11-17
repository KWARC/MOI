from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from .models import ObjectRegistration, ObjectCitations
from .forms import ObjectRequestForm, MultipleRequestForm

import json


def index(request):
    return render(request, 'moi/index.html',
                  {'objects': ObjectRegistration.objects.filter(approved=True)})


def detail(request, object_id):
    object = get_object_or_404(ObjectRegistration, pk=object_id)

    # if the object exists,  but the user is not allowed to see it
    # TODO: Return a 401
    if not object.approved:
        if not (request.user and (
                    request.user.is_superuser or
                        object.user == request.user)):
            raise Http404()

    cites = ObjectCitations.objects.filter(object=object)
    cited = ObjectCitations.objects.filter(subject=object)

    return render(request, 'moi/detail.html',
                  {'obj': object, 'cites': cites, 'cited': cited})


@login_required
def register(request):
    form = ObjectRequestForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            registration = form.save(commit=False)
            registration.clean()
            registration.user = request.user
            registration.save()

            return redirect('moi:details', registration.moi)

    return render(request, 'moi/register.html', {'form': form})


@login_required
def register_multiple(request):
    form = MultipleRequestForm(request.POST or None)

    if request.method == 'POST':
        try:
            if form.is_valid():
                obj = json.loads(form.cleaned_data["request_json"])
                (models, citations) = create_models(obj, request.user)

                for m in models:
                    m.save()

                for (s, o) in citations:
                    ObjectCitations(subject=s, object=o).save()

                return render(request, 'moi/registermultiple_success.html',
                              {'objects': models})
        except Exception as e:
            form.add_error('request_json', str(e))

    return render(request, 'moi/registermultiple.html', {'form': form})


def create_models(spec, user):
    models = {}
    citations = []

    def try_get_key(o, k, d=""):
        try:
            return o[k]
        except KeyError:
            return d

    for item in spec:
        name = item["MOI"]
        if name in models:
            raise ValueError('MOI {} already used'.format(name))

        models[name] = ObjectRegistration(
            user=user,
            approved=False,
            type=try_get_key(item, "Type"),
            note=try_get_key(item, "Note"),
            keywords=try_get_key(item, "Keywords"),
            modref=json.dumps(item["MODRef"])
        )

        if "Related-To" in item:
            citations.append((name, item["Related-To"]))

    mos = [value for (key, value) in models.items()]
    cos = [(models[s], models[o]) for (s, o) in citations]
    return (mos, cos)
