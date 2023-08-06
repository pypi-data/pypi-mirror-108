from django.http import JsonResponse
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated


class RMCheckPermissionAPIMixin(object):
    required_permission = True
    permission_codename = ''
    permission_denied_message = 'Você não tem permissão para realizar esta operação.'

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_superuser:
            return super(RMCheckPermissionAPIMixin, self).dispatch(request, *args, **kwargs)

        if not self.required_permission and request.user.is_authenticated:
            return super(RMCheckPermissionAPIMixin, self).dispatch(request, *args, **kwargs)

        if not request.user.is_authenticated:
            return JsonResponse({}, status=403)

        if not self.check_user_permissions(request):
            return JsonResponse({}, status=403)

        return super(RMCheckPermissionAPIMixin, self).dispatch(request, *args, **kwargs)

    def check_user_permissions(self, request):
        if(isinstance(self.permission_codename,(type([]),))):
            # se for um vetor de grupos
            valida = request.user.groups.filter(name__in=self.permission_codename).exists()
        else:
            # se um grupo específico
            valida = request.user.groups.filter(name=self.permission_codename).exists()
        return valida


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return # To not perform the csrf check previously happening


class RMCustomListCreateAPIView(generics.ListCreateAPIView,RMCheckPermissionAPIMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.username,updated_by=self.request.user.username)

    def __init__(self, *args, **kwargs):
        super(RMCustomListCreateAPIView, self).__init__(*args, **kwargs)


class RMCustomRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView,RMCheckPermissionAPIMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication,)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.username)

    def __init__(self, *args, **kwargs):
        super(RMCustomRetrieveUpdateDestroyAPIView, self).__init__(*args, **kwargs)


class RMCustomGenericAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication,)

    def __init__(self, *args, **kwargs):
        super(RMCustomGenericAPIView, self).__init__(*args, **kwargs)