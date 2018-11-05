from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render

class OwnerOnlyMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and self.get_object().owner != self.request.user:
            return render(self.request, '403.html',status=403)

        return super(OwnerOnlyMixin, self).dispatch(request, *args, **kwargs)

