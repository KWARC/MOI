from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from moiregistry.models import ObjectRegistration, ObjectCitations

from .forms import ObjectRequestForm


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

    return render(request, 'moi/detail.html', {'obj': object, 'cites': cites, 'cited': cited})


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
