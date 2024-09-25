
PAYLOAD_CONSULTRORA = {'response_type=id_token&client_id=5c0cecaa-277c-46dc-b238-59bc1a461907&redirect_uri=https%3A%2F%2Fconsultoradigital.boticario.com.br%2Flogin%2Foauth2callback&prompt=login&scope=openid&p=B2C_1A_JIT_SIGNUPORSIGNIN_PRD'}

PAYLOAD_LOGIN = {
    'request_type':'RESPONSE',
    'signInName':'',
    'password':''
}
HEADERS_CONSULTRORA = {
    'authority': 'login.extranet.grupoboticario.com.br',
    'scheme': 'https',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'origin': 'https://gboticariob2c.b2clogin.com',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer':'https://consultoradigital.boticario.com.br/',
    'Sec-Ch-Ua':'"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"'
}
HEADERS_LOGIN = {
    'authority': 'login.extranet.grupoboticario.com.br',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://login.extranet.grupoboticario.com.br',
    'Priority':'u=0, i',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
PAYLOAD_GRAPH_LOGIN = {"operationName":"Login","variables":{"data":{"updatedAccessToken":"ALTERAR AQUI","accessToken":""}},"query":"mutation Login($data: LoginInput!) {\n  Login(data: $data) {\n    user {\n      ...Consultant\n      __typename\n    }\n    token\n    __typename\n  }\n}\n\nfragment Consultant on Consultant {\n  id\n  name\n  role\n  conversion\n  stores {\n    ...Store\n    __typename\n  }\n  daysOff\n  currentlyInactive\n  maxMissionsQuantity\n  __typename\n}\n\nfragment Store on Store {\n  id\n  name\n  displayName\n  active\n  emails\n  ssidName\n  blockWifi\n  maxMissionsQuantity\n  maxEventsQuantity\n  enabledMissions\n  workingDays\n  __typename\n}\n"}

HEADER_MISSION = {
    'authority': 'appconsultoradigital.boticario.com.br',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'pt-BR,pt;q=0.9',
    'Content-Type': 'application/json',
    'Origin': 'https://consultoradigital.boticario.com.br',
    'Priority': 'u=1, i',
    'Referer': 'https://consultoradigital.boticario.com.br/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

