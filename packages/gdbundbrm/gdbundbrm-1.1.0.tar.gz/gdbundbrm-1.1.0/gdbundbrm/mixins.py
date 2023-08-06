from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


class RMCheckPermissionMixin(object):
    required_permission = True
    permission_codename = ''
    permission_denied_message = 'Você não tem permissão para realizar esta operação.'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(RMCheckPermissionMixin, self).dispatch(request, *args, **kwargs)

        if not self.required_permission and request.user.is_authenticated:
            return super(RMCheckPermissionMixin, self).dispatch(request, *args, **kwargs)

        if not request.user.is_authenticated:
            messages.add_message(request, messages.WARNING, "Usuário não autenticado")
            return redirect(reverse_lazy('base:login'))

        if not self.check_user_permissions(request):
            messages.add_message(request, messages.WARNING,self.permission_denied_message,'error')
            return redirect('base:no_access')

        return super(RMCheckPermissionMixin, self).dispatch(request, *args, **kwargs)

    def check_user_permissions(self, request):
        if(isinstance(self.permission_codename,(type([]),))):
            # se for um vetor de grupos
            valida = request.user.groups.filter(name__in=self.permission_codename).exists()
        else:
            # se um grupo específico
            valida = request.user.groups.filter(name=self.permission_codename).exists()
        return valida

