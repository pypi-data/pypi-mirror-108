from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Group
import base64
from django.conf import settings
import requests
import json

UserModel = get_user_model()


class RMConfig():
    try:
        RM_USER = settings.RM_USER
        RM_PASS = settings.RM_PASS
        RM_API_PORT = settings.RM_API_PORT
        RM_BASE_URL = settings.RM_BASE_URL
        dataString = f"{RM_USER}:{RM_PASS}"
        dataString = dataString.encode("utf-8")
        basic = str(base64.b64encode(dataString))
        AUTHORIZATION = basic.replace("b'", "").replace("'", "")
        BASE_URL = f"{RM_BASE_URL}:{RM_API_PORT}"
    except:
        RM_USER = ''
        RM_PASS = ''
        print('Necessário incluir as variáveis RM_USER, RM_PASS, RM_API_PORT e RM_BASE_URL no arquivo settings.py')

    HEADERS = {'accept': 'application/json', 'content-type': "application/json",
               "Authorization": f"Basic {AUTHORIZATION}"}


class RMUser(RMConfig):

    def update_usuario(self, username, payload):
        url_api = f"/api/framework/v1/users/{username}"
        endpoint = f'{self.BASE_URL}{url_api}'
        response = requests.request("PATCH", endpoint, headers=self.HEADERS, data=json.dumps(payload))
        result = json.loads(response.text)

        return result

    def ativar_usuario(self, username):
        url_api = f"/api/framework/v1/users/{username}"
        endpoint = f'{self.BASE_URL}{url_api}'
        payload = {"active": True}
        response = requests.request("PATCH", endpoint, headers=self.HEADERS, data=json.dumps(payload))
        result = json.loads(response.text)

        return result

    def desativar_usuario(self, username):
        url_api = f"/api/framework/v1/users/{username}"
        endpoint = f'{self.BASE_URL}{url_api}'
        payload = {"active": False}
        response = requests.request("PATCH", endpoint, headers=self.HEADERS, data=json.dumps(payload))
        result = json.loads(response.text)

        return result

    def get_usuario(self, username):
        url_api = f"/api/framework/v1/users/{username}"
        endpoint = f'{self.BASE_URL}{url_api}'
        response = requests.request("GET", endpoint, headers=self.HEADERS)
        try:
            if response.status_code == 200:
                return response.json()
        except:
            pass

        return None

    def recuperar_senha(self, username):
        url_api = f"/api/framework/v1/users/{username}/recoveryPassword"
        endpoint = f'{self.BASE_URL}{url_api}'
        response = requests.request("POST", endpoint, headers=self.HEADERS)
        try:
            return response.json()
        except:
            return None

    def alterar_senha_com_token(self, username='', token='', senha=''):
        url_api = f"/api/framework/v1/{username}/changePasswordWithToken"
        payload = {
            "lastPassword": token,
            "newPassword": senha,
            "confirmationPassword": senha
        }
        endpoint = f'{self.BASE_URL}{url_api}'
        response = requests.request("POST", endpoint, headers={"Content-Type": "application/json"},
                                    data=json.dumps(payload))
        return response


class RMUtils(RMConfig):

    def get_query(self, codConsulta, codfilial=0, codsistema='S', params=''):
        url_api = f"/api/framework/v1/consultaSQLServer/RealizaConsulta/{codConsulta}/{codfilial}/{codsistema}/?parameters={params}"
        endpoint = f'{self.BASE_URL}{url_api}'
        response = requests.get(endpoint, headers=self.HEADERS)
        try:
            return response.json()
        except:
            return None


class RMJWT(RMConfig):

    def connect(self, username, password):
        url_api = f"{self.BASE_URL}/api/connect/token"
        payload = {'username': username, 'password': password}
        response = requests.post(url_api, data=payload)

        if response.status_code == 200:
            rm = RMUser()
            usu = rm.get_usuario(username)
            #usu = json.loads(usu)

            # username
            username = usu.get('userName')

            # First_name
            first_name = usu.get('name')
            first_name = ''.join(first_name.get('givenName'))

            # Last_name
            last_name = usu.get('name')
            last_name = ''.join(last_name.get('familyName'))

            # E-mail
            email = usu.get('emails')[0]
            email = ''.join(email.get('value'))

            # Ativo
            active = True

            # Roles
            roles = usu.get('roles')

            # Retorno do Objeto
            usuario = {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "is_active": active,
                "email": email,
                "roles": roles
            }
            return usuario
        else:
            return None


class RmAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None):
        try:
            rm = RMJWT()
            try:
                login_rm = rm.connect(username, password)
            except:
                login_rm = None
            if login_rm:
                try:
                    user = UserModel.objects.get(username=login_rm.get('username'))

                    try:
                        # Atualizar usuário
                        user.first_name = ''.join(login_rm.get('first_name'))
                        user.last_name = ''.join(login_rm.get('last_name'))
                        user.email = ''.join(login_rm.get('email'))
                        user.is_active = True
                        user.save()
                    except Exception as exception:
                        pass
                    # criar e vincular Perfil ao Usuário
                    user.groups.clear()
                    user.save()
                    for perfil in login_rm.get('roles'):
                        perfil_name = perfil.get('value')
                        self.cross_user_group(perfil_name, user)
                    user.set_password(password)
                    user.save()
                    return user

                except UserModel.DoesNotExist:
                    user = UserModel.objects.create_user(
                        username=login_rm.get('username'),
                        first_name=login_rm.get('first_name'),
                        last_name=login_rm.get('last_name'),
                        email=login_rm.get('email'),
                        is_active=True,
                        is_staff=False,
                        is_superuser=False
                    )
                    # criar e vincular Perfil ao Usuário
                    for perfil in login_rm.get('roles'):
                        perfil_name = ''.join(perfil.get('value'))
                        self.cross_user_group(perfil_name, user)
                    user.set_password(password)
                    user.save()

                    return user
                except Exception as ex:
                    pass
            return None

        except Exception as ex:
            # No user was found, return None - triggers default login failed
            return None

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

    def cross_user_group(self, name, user):
        # Vincular Grupo ao usuário
        group, create = Group.objects.get_or_create(name=name)
        if group:
            group.user_set.add(user)
        if create:
            try:
                cross = Group.objects.get(name=name)
                cross.user_set.add(user)
            except:
                pass
