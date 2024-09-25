import requests, time, json
import datetime
from datetime import date, timedelta, datetime
import pandas as pd

from const import PAYLOAD_CONSULTRORA,HEADERS_CONSULTRORA,HEADERS_LOGIN,PAYLOAD_LOGIN,PAYLOAD_GRAPH_LOGIN,HEADER_MISSION
class ExtractMissaoConsultoraDigital:
    """
    Essa classe tem por finalidade:
        1. Realizar o login no site consultora digital
        2. Naegar até a página com todas as lojas
        3. Clicar em Loja a loja e verificar se existem missões a serem concluídas
        4. Caso existam é necessário completar as missões
    """
    def execute(self):
        session, acces_token = self.realizando_login_consultrora()
        self.alterando_missao(session,acces_token)
    def realizando_login_consultrora(self):
        """
        Método responsável por realizar o login no site consultora digital
        parâmetros:
            Nenhum
        Retorna:
            id_token: token de acesso para extração e atualização dos parâemtros das lojas
            session: Sessão do requests
        """
        # Criando uma sessão requests
        session = requests.Session()
        # Obtendo o token de autenticação para logar no site
        response = session.get('https://consultoradigital.boticario.com.br/login')

        # Extraindo autorization
        authorization_code = response.text.split('"authorizePath":"')[1].split('"')[0]

        # Extraindo ClientID
        client_id = response.text.split('"clientId":"')[1].split('"')[0]

        # Construindo a URL_CONSULTORA
        URL_CONSULTORA= f'https://login.extranet.grupoboticario.com.br/{authorization_code}?response_type=id_token&client_id={client_id}&redirect_uri=https%3A%2F%2Fconsultoradigital.boticario.com.br%2Flogin%2Foauth2callback&prompt=login&scope=openid&p=B2C_1A_JIT_SIGNUPORSIGNIN_PRD'

        # Navegando ate a url de login
        response = session.get(URL_CONSULTORA,headers=HEADERS_CONSULTRORA)

        # Verificando se houve erro
        if response.status_code != 200:
            raise Exception(f'Erro ao realizar o redirecionamento para o site. Status code: {response.status_code}')

        # Extraindo o tenantId
        tenantId = response.text.split('"tenant":"')[1].split('"')[0]

        # Extraindo transId
        transId = response.text.split('"transId":"')[1].split('"')[0]

        # Extraindo Csrf-Token
        csrf = response.text.split('"csrf":"')[1].split('"')[0]

        # Construindo a URL_LOGIN_CONSULTORA
        URL_LOGIN_CONSULTORA = f'https://login.extranet.grupoboticario.com.br{tenantId}/SelfAsserted?tx={transId}&p=B2C_1A_JIT_SignUpOrSignin_PRD'

        # Armazenando valor da url como texto
        URL_HEADER = f'https://login.extranet.grupoboticario.com.br/{authorization_code}?response_type=id_token&client_id={client_id}&redirect_uri=https%3A%2F%2Fconsultoradigital.boticario.com.br%2Flogin%2Foauth2callback&prompt=login&scope=openid&p=B2C_1A_JIT_SIGNUPORSIGNIN_PRD'

        # Adicioanndo os headers
        HEADERS_LOGIN['Referer'] = URL_HEADER
        # HEADERS_LOGIN['path'] = f'{tenantId}/SelfAsserted?tx={transId}=B2C_1A_JIT_SignUpOrSignin_PRD'
        HEADERS_LOGIN['X-Csrf-Token'] = csrf

        # PAYLOAD_LOGIN['tx'] = transId
        # PAYLOAD_LOGIN['p'] = 'B2C_1A_JIT_SignUpOrSignin_PRD'

        # Fazendo a arequisição POST para logar
        response = session.post(URL_LOGIN_CONSULTORA,headers=HEADERS_LOGIN, data=PAYLOAD_LOGIN)

        # Verificando se houve erro
        if response.status_code != 200:
            raise Exception(f'Erro ao fazer requisição post para logar. Status code: {response.status_code}')

        # #Obtendo access_token
        query_params = f'?rememberMe=false&csrf_token={csrf}&tx={transId}&p=B2C_1A_JIT_SignUpOrSignin_PRD&diags=%7B%22pageViewId%22%3A%22925fdb4e-a37f-4388-baeb-2ad415a6315b%22%2C%22pageId%22%3A%22CombinedSigninAndSignup%22%2C%22trace%22%3A%5B%7B%22ac%22%3A%22T005%22%2C%22acST%22%3A1715345553%2C%22acD%22%3A1%7D%2C%7B%22ac%22%3A%22T021%20-%20URL%3Ahttps%3A%2F%2Fidentityb2cextranet.grupoboticario.digital%2Flogin.html%22%2C%22acST%22%3A1715345553%2C%22acD%22%3A20%7D%2C%7B%22ac%22%3A%22T019%22%2C%22acST%22%3A1715345553%2C%22acD%22%3A3%7D%2C%7B%22ac%22%3A%22T004%22%2C%22acST%22%3A1715345553%2C%22acD%22%3A3%7D%2C%7B%22ac%22%3A%22T003%22%2C%22acST%22%3A1715345553%2C%22acD%22%3A1%7D%2C%7B%22ac%22%3A%22T035%22%2C%22acST%22%3A1715345553%2C%22acD%22%3A0%7D%2C%7B%22ac%22%3A%22T030Online%22%2C%22acST%22%3A1715345553%2C%22acD%22%3A0%7D%2C%7B%22ac%22%3A%22T002%22%2C%22acST%22%3A1715351682%2C%22acD%22%3A0%7D%2C%7B%22ac%22%3A%22T018T010%22%2C%22acST%22%3A1715351680%2C%22acD%22%3A1954%7D%5D%7D'
        confirm_url = 'https://login.extranet.grupoboticario.com.br/1e6392bd-5377-48f0-9a8e-467f5b381b18/B2C_1A_JIT_SignUpOrSignin_PRD/api/CombinedSigninAndSignup/confirmed' + query_params

        # Realizando a requisição  GET pra obter o acc-token
        response = session.get(confirm_url,headers=HEADERS_LOGIN)

        if response.status_code != 200:
            raise Exception(f'Erro ao fazer requisição get para obter o id_token. Status code: {response.status_code}')

        # Obter o access_token por meio da location
        id_token = response.url.split('id_token=')[1].split('&')[0]

        # Requisição POST para graphiql para obter o id_token do login
        url_grphql = 'https://appconsultoradigital.boticario.com.br/graphql'

        # Atribuindo variavel dinamica ao payload
        PAYLOAD_GRAPH_LOGIN['variables']['data']['updatedAccessToken'] = id_token

        # Obtendo response
        response = session.post(url_grphql,json=PAYLOAD_GRAPH_LOGIN)

        if response.status_code != 200:
            raise Exception(f'Erro ao fazer requisição POST para obter o access_token. Status code: {response.status_code}')

        acces_token = response.text.split('"token":"Bearer ')[1].split('"')[0]

        return session, acces_token

    def alterando_missao(self,session, acces_token):
        """
            Este método tem como função percorrer todas as lojas cadastradas e verificar se existem missões pendentes
            Casos exista ele deve concluir as missões pendentes.

            parâmetros:
                r: Sessão do requests
                id_token: Token de acesso
            Retorna:
                None
        """

        bcps = [11992]

        for lojas in bcps:
            # Faz uma requisição POST no bcps indicado para verificar se existem missões pendentes
            url_bcps = 'https://appconsultoradigital.boticario.com.br/graphql'

            PAYLOAD_MISSION = {"operationName":"Missions","variables":{"period":"Day","stores":[lojas]},"query":"query Missions($page: Int, $pageSize: Int, $type: MissionType, $status: MissionStatus, $period: MissionPeriod!, $stores: [Int!], $lastKey: String) {\n  Missions(page: $page, pageSize: $pageSize, type: $type, status: $status, period: $period, stores: $stores, lastKey: $lastKey) {\n    ...MissionsFragment\n    __typename\n  }\n}\n\nfragment MissionsFragment on Missions {\n  totalPending\n  goal\n  pagination {\n    ...Pagination\n    __typename\n  }\n  items {\n    ...MissionFragment\n    __typename\n  }\n  __typename\n}\n\nfragment Pagination on Pagination {\n  current\n  totalPages\n  totalItems\n  pageSize\n  lastKey\n  __typename\n}\n\nfragment MissionFragment on Mission {\n  id\n  class\n  status\n  statusExplanation\n  type\n  sku\n  skuName\n  shareImages\n  defaultMessage\n  order {\n    ...Order\n    __typename\n  }\n  customer {\n    ...CustomerFragment\n    __typename\n  }\n  consultant {\n    ...Consultant\n    __typename\n  }\n  instantMessageTemplateName\n  instantMessageVariables {\n    ...InstantMessageVariable\n    __typename\n  }\n  __typename\n}\n\nfragment Order on Order {\n  date\n  products {\n    ...OrderProduct\n    __typename\n  }\n  storeName\n  __typename\n}\n\nfragment OrderProduct on OrderProduct {\n  sku\n  category\n  description\n  recommendationDate\n  quantity\n  price\n  __typename\n}\n\nfragment CustomerFragment on Customer {\n  cpf\n  name\n  lastName\n  gender\n  email\n  residentialPhone\n  hair\n  hairDilemma\n  skinType\n  birth\n  active\n  statusPoints\n  fidelityDiscount\n  averageTicket\n  frequency\n  itemsPerPurchase\n  lastContact\n  addresses {\n    ...CustomerAddress\n    __typename\n  }\n  productsAlert {\n    ...CustomersProductAlert\n    __typename\n  }\n  relatedProducts {\n    ...ProductRecommendation\n    __typename\n  }\n  fieldsToUpdate\n  optOut\n  mobilePhone\n  __typename\n}\n\nfragment CustomerAddress on CustomerAddress {\n  street\n  number\n  zipCode\n  district\n  complement\n  city\n  stateAbbreviation\n  __typename\n}\n\nfragment CustomersProductAlert on CustomersProductAlert {\n  id\n  name\n  __typename\n}\n\nfragment ProductRecommendation on ProductRecommendation {\n  product {\n    ...Product\n    __typename\n  }\n  percentage\n  __typename\n}\n\nfragment Product on Product {\n  id\n  name\n  __typename\n}\n\nfragment Consultant on Consultant {\n  id\n  name\n  role\n  conversion\n  stores {\n    ...Store\n    __typename\n  }\n  daysOff\n  currentlyInactive\n  maxMissionsQuantity\n  __typename\n}\n\nfragment Store on Store {\n  id\n  name\n  displayName\n  active\n  emails\n  ssidName\n  blockWifi\n  maxMissionsQuantity\n  maxEventsQuantity\n  enabledMissions\n  workingDays\n  __typename\n}\n\nfragment InstantMessageVariable on InstantMessageVariable {\n  position\n  title\n  defaultValue\n  enableEdit\n  __typename\n}\n"}
            HEADER_MISSION['Authorization'] = f'Bearer {acces_token}'

            response = session.post(url_bcps,headers=HEADER_MISSION,json=PAYLOAD_MISSION)

            if response.status_code != 200:
                print('Erro na requisição POST')

            # Veriricar se totalPending = 0
            data = response.json()
            data = data['data']['Missions']['items']
            if data:
            # Percorrer json para veririficar se tem missão pendente
                for item in data:
                    # print(item)
                    # Validar os inputs para o post
                    if item['status'] == 'Pending':
                        id = item['id']
                        nome_consultor = item['instantMessageVariables'][0]['defaultValue']
                        nome_gentil = item['instantMessageVariables'][1]['defaultValue']
                        loja = item['instantMessageVariables'][2]['defaultValue']

                        # Ecnontrando variaveis para o payload
                        PAYLOAD_QUERY_MISSION =  {"operationName":"SendMissionMessage","variables":{"data":{"id":id,"variables":[{"position":1,"value":nome_consultor},{"position":2,"value":nome_gentil},{"position":3,"value":loja}]}},"query":"mutation SendMissionMessage($data: SendMissionMessageInput!) {\n  SendMissionMessage(data: $data) {\n    ...SendMissionMessageResult\n    __typename\n  }\n}\n\nfragment SendMissionMessageResult on SendMissionMessageResult {\n  sent\n  __typename\n}\n"}

                        # Fazendo requisisão para enviar missão
                        response = session.post(url_bcps,headers=HEADER_MISSION,json=PAYLOAD_QUERY_MISSION)
                        # Verificando se houve erro
                        if response.status_code != 200:
                            print('Erro na requisição POST')
                        else:
                            print("Missão pendente enviada")
            else:
                print("Nenhuma missão pendente")
# Chamando script
atualizar_missao = ExtractMissaoConsultoraDigital().execute()