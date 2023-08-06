from django.conf import settings
import requests
import json


class HubSpotConfig():

    try: API_TOKEN = settings.HUBSPOT_API_KEY
    except: API_TOKEN = ''

    BASE_URL = "https://api.hubapi.com"
    URL_PARAMS = {"hapikey": API_TOKEN}
    HEADERS = {'accept': 'application/json','content-type': "application/json"}


class HubForm(HubSpotConfig):
    form_values = []

    # https://app.hubspot.com/forms/2961792/845a3007-d504-431a-ad82-cdd034fdbbae/performance
    def get_form_submissions(self, formId, limit=50, after='', countResults=10000):
        """
        Método que retorna todas as inscrições no formulario formId

        * formId = Id do Formulário
        * limit = quantidade de resultados por páginas (max =50)
        * after = quando há mais de uma página, after carrega a url ?after= para px página em recursão
        * countResults = Quantos results esperados
        """
        url_api = f"/form-integrations/v1/submissions/forms/{formId}?after={after}&limit={limit}"
        endpoint = f'{ self.BASE_URL }{ url_api }'
        response = requests.request("GET", endpoint, headers=self.HEADERS, params=self.URL_PARAMS)
        result = json.loads(response.text)
        result = result.get('results')
        try:
            self.form_values.append(result[0])
        except:
            pass

        if len(self.form_values) == countResults:
            return self.form_values

        try:
            if result.get('paging').get('next').get('after'):
                after_link = result.get('paging').get('next').get('after')
                self.get_form_submissions(formId,limit,after_link, countResults )
        except:
            pass

        return self.form_values


class HubDB(HubSpotConfig):

    def get_tables(self):
        url_api = "/cms/v3/hubdb/tables"
        endpoint = f'{ self.BASE_URL }{ url_api }'
        response = requests.request("GET", endpoint, headers=self.HEADERS, params=self.URL_PARAMS)
        print(response.text)

    def create_table(self, payload):
        url_api = f"/cms/v3/hubdb/tables"
        endpoint = f'{ self.BASE_URL }{ url_api }'
        if not payload:
            payload = "{\"allowPublicApiAccess\":false,\"useForPages\":true," \
                  "\"columns\":[" \
                  "{\"name\":\"text_column\"," \
                  "\"label\":\"Text Column\"," \
                  "\"archived\":false," \
                  "\"type\":\"TEXT\"}" \
                  "]," \
                  "\"name\":\"test_table\"," \
                  "\"enableChildTablePages\":false," \
                  "\"label\":\"Test Table\"," \
                  "\"allowChildTables\":true}"

        response = requests.request("POST", endpoint, data=payload, headers=self.HEADERS, params=self.URL_PARAMS)

        print(response.text)

    def get_table(self, tableIdOrName):
        url_api = f"/cms/v3/hubdb/tables/{tableIdOrName}"
        endpoint = f'{ self.BASE_URL }{ url_api }'
        response = requests.request("GET", endpoint, headers=self.HEADERS, params=self.URL_PARAMS)
        print(response.text)

    def update_table(self, tableIdOrName, payload):
        url_api = f"/cms/v3/hubdb/tables/{tableIdOrName}"
        endpoint = f'{ self.BASE_URL }{ url_api }'
        response = requests.request("PATCH", endpoint, data=payload, headers=self.HEADERS, params=self.URL_PARAMS)
        print(response.text)

    def delete_table(self, tableIdOrName):
        url_api = f"/cms/v3/hubdb/tables/{tableIdOrName}"
        endpoint = f'{ self.BASE_URL }{ url_api }'
        response = requests.request("DELETE", endpoint, headers=self.HEADERS, params=self.URL_PARAMS)
        print(response.text)

    def get_table_rows(self, tableIdOrName):
        url_api = f"/cms/v3/hubdb/tables/{tableIdOrName}/rows"
        endpoint = f'{ self.BASE_URL }{ url_api }'
        response = requests.request("GET", endpoint, headers=self.HEADERS, params=self.URL_PARAMS)
        print(response.text)

    def add_table_rows(self, tableIdOrName, payload):
        payload = "{\"path\":\"test_path\"," \
                  "\"childTableId\":\"1902373\"," \
                  "\"values\":{\"multiselect\":" \
                  "[" \
                    "{\"id\":\"1\",\"name\":\"Option 1\",\"type\":\"option\"}," \
                    "{\"id\":\"2\",\"name\":\"Option 2\",\"type\":\"option\"}" \
                  "]," \
                  "\"number_column\":76," \
                  "\"text_column\":\"sample text value\"" \
                  "}," \
                  "\"name\":\"test_title\"" \
                  "}"
        url_api = f"/cms/v3/hubdb/tables/{tableIdOrName}/rows"
        endpoint = f'{ self.BASE_URL }{ url_api }'
        response = requests.request("POST", endpoint, data=payload, headers=self.HEADERS, params=self.URL_PARAMS)
        print(response.text)

    def get_table_row(self, tableIdOrName, rowId):
        url_api = f"/cms/v3/hubdb/tables/{tableIdOrName}/rows/{rowId}"
        endpoint = f'{ self.BASE_URL }{ url_api }'
        response = requests.request("GET", endpoint, headers=self.HEADERS, params=self.URL_PARAMS)
        print(response.text)


    def get_draft_table(self, tableIdOrName):
        url_api = f"/cms/v3/hubdb/tables/{tableIdOrName}/draft"
        endpoint = f'{ self.BASE_URL }{ url_api }'
        response = requests.request("GET", endpoint, headers=self.HEADERS, params=self.URL_PARAMS)
        print(response.text)

    def get_draft_tables(self):
        url_api = f"/cms/v3/hubdb/tables/draft"
        endpoint = f'{ self.BASE_URL }{ url_api }'
        response = requests.request("GET", endpoint, headers=self.HEADERS, params=self.URL_PARAMS)
        print(response.text)

    def update_draft_table(self, tableIdOrName):
        url_api = f"/cms/v3/hubdb/tables/{tableIdOrName}/draft"
        endpoint = f'{ self.BASE_URL }{ url_api }'
        response = requests.request("PATCH", endpoint, headers=self.HEADERS, params=self.URL_PARAMS)
        print(response.text)

    def get_draft_table_rows(self, tableIdOrName):
        url_api = f"/cms/v3/hubdb/tables/{tableIdOrName}/rows/draft"
        endpoint = f'{ self.BASE_URL }{ url_api }'
        response = requests.request("GET", endpoint, headers=self.HEADERS, params=self.URL_PARAMS)
        print(response.text)

    def get_draft_table_row(self, tableIdOrName, rowId):
        url_api = f"/cms/v3/hubdb/tables/{tableIdOrName}/rows/{rowId}/draft"
        endpoint = f'{ self.BASE_URL }{ url_api }'
        response = requests.request("GET", endpoint, headers=self.HEADERS, params=self.URL_PARAMS)
        print(response.text)

    def delete_draft_table_row(self, tableIdOrName, rowId):
        url_api = f"/cms/v3/hubdb/tables/{tableIdOrName}/rows/{rowId}/draft"
        endpoint = f'{ self.BASE_URL }{ url_api }'
        response = requests.request("DELETE", endpoint, headers=self.HEADERS, params=self.URL_PARAMS)
        print(response.text)


class HubContact(HubSpotConfig):

    def create_contact(self, hubFieldKeyValue):
        """
        hubFieldKeyValue: list of class hubFieldKeyValue with instance (name, value)

        Returns an HTTP 200 response on success, with the response body containing the details of the new contact record:
        {
          "identity-profiles": [...],
          "properties": {
              ...
          },
          "vid": 00001
        }
        """
        try:
            if not isinstance(hubFieldKeyValue[0], HubFieldKeyValue):
                return None
        except:
            return None
        payload = {"properties":
            [field.__dict__ for field in hubFieldKeyValue]
        }
        url_api = f"/contacts/v1/contact/"
        endpoint = f'{self.BASE_URL}{url_api}'
        response = requests.request("POST", endpoint, data=json.dumps(payload), headers=self.HEADERS, params=self.URL_PARAMS)
        result = json.loads(response.text)
        return result

    def update_contact_by_id(self, vid, hubFieldKeyValue):
        """
        hubFieldKeyValue: list of class hubFieldKeyValue with instance (name, value)
        vid: Chave id do contato no Hubspot
        """
        try:
            if not isinstance(hubFieldKeyValue[0], HubFieldKeyValue):
                return None
        except:
            return None
        payload = {"properties":
            [field.__dict__ for field in hubFieldKeyValue]
        }
        url_api = f"/contacts/v1/contact/{vid}/profile"
        endpoint = f'{self.BASE_URL}{url_api}'
        response = requests.request("POST", endpoint, data=json.dumps(payload), headers=self.HEADERS, params=self.URL_PARAMS)
        result = json.loads(response.text)
        return result

    def update_contact_by_email(self, email, hubFieldKeyValue):
        """
        hubFieldKeyValue: list of class hubFieldKeyValue with instance (name, value)
        email: Email do contato no Hubspot

        Returns a 204 No Content response on success.
        """
        try:
            if not isinstance(hubFieldKeyValue[0], HubFieldKeyValue):
                return None
        except:
            return None
        payload = {"properties":
            [field.__dict__ for field in hubFieldKeyValue]
        }
        url_api = f"/contacts/v1/contact/email/{email}/profile"
        endpoint = f'{self.BASE_URL}{url_api}'
        response = requests.request("POST", endpoint, data=json.dumps(payload), headers=self.HEADERS, params=self.URL_PARAMS)
        result = json.loads(response.text)
        return result

    def delete_contact(self, vid):
        """
        Example JSON output:
            {
              "vid": 61571,
              "deleted": true,
              "reason": "OK"
            }
        """
        url_api = f"/contacts/v1/contact/vid/{vid}"
        endpoint = f'{self.BASE_URL}{url_api}'
        response = requests.request("DELETE", endpoint, headers=self.HEADERS, params=self.URL_PARAMS)
        result = json.loads(response.text)
        return result

    def get_contact_by_id(self, vid):
        url_api = f"/contacts/v1/contact/vid/{vid}/profile"
        endpoint = f'{self.BASE_URL}{url_api}'
        response = requests.request("GET", endpoint, headers=self.HEADERS, params=self.URL_PARAMS)
        result = json.loads(response.text)
        return result
    
    def get_all_contacts(self):
        offset=''
        self.URL_PARAMS['count'] = 50
        url_api = f"/contacts/v1/lists/all/contacts/all"
        endpoint = f'{self.BASE_URL}{url_api}'
        results = []
        while True:
            self.URL_PARAMS['vidOffset'] = offset
            response = requests.request("GET", endpoint, headers=self.HEADERS, params=self.URL_PARAMS)
            #print(response.json())
            if response.status_code == 200:
                result = json.loads(response.text)
                results = results + result.get('contacts')
                offset = result.get('vid-offset')
                print(f'{len(results)} contatos requisitados')
                # num registros
                if not result.get('has-more'): #or len(results) >= 1:
                    break

        return results


    def get_contact_by_email(self, email):
        url_api = f"/contacts/v1/contact/email/{email}/profile"
        endpoint = f'{self.BASE_URL}{url_api}'
        response = requests.request("GET", endpoint, headers=self.HEADERS, params=self.URL_PARAMS)
        result = json.loads(response.text)
        return result

    def search_contact(self, search):
        """
        search by email, name, phone or company
        """

        url_api = f"/contacts/v1/search/query?q={search}"
        endpoint = f'{self.BASE_URL}{url_api}'
        response = requests.request("GET", endpoint, headers=self.HEADERS, params=self.URL_PARAMS)
        result = json.loads(response.text)
        return result


class HubFieldKeyValue():
    property = ''
    value = ''

    def __init__(self, prop, value):
        self.property = prop
        self.value = value


class HubDBColumn():
    name = ''
    label = ''
    type = 'TEXT'

    def __init__(self, name, label):
        self.name = name
        self.label = label

    def get_json(self):
        return "{\"name\":\"{0}\",\"label\":\"{1}\",\"archived\":false,\"type\":\"{2}\"}"\
                .format(self.name, self.label, self.type)


class HubDBTable():
    columns = []
    name = ''
    label = ''

    def __init__(self, columns, name, label):
        self.columns = columns
        self.name = name
        self.label = label

    def get_json(self):
        cols = ",".join([c.get_json() for c in self.columns])
        return "{\"allowPublicApiAccess\":false," \
                "\"useForPages\":true," \
                "\"columns\":[" + cols + "]," \
                "\"name\":\"test_table\"," \
                "\"enableChildTablePages\":false," \
                "\"label\":\"Test Table\"," \
                "\"allowChildTables\":true" \
            "}"
