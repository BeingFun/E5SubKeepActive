# # step3 用刷新令牌更新过期的访问令牌
# import requests
#
# # step1 请求授权码
# client_id = "94a897de-6557-4de0-8d3f-525fa6d67534"
# tenant_id = "9a33b84f-5fc5-4681-bedb-022a09ba7100"
# client_secret = "hKR8Q~lKkdhw.ltdGcZTXBtf12J8eWYKMfX~2a9w"
# client_assertion = "6155e406-dc06-4e77-b8af-ce27a8942aa3"
# scope = "openid+email+offline_access+user.read"
# redirect_uri = "http://localhost:5000/getAToken"
# response_type = "code"
# response_mode = "query"
# refresh_token = ""
#
# authorization_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize?&client_id={client_id}&response_type={response_type}&scope={scope}&response_mode={response_mode}&redirect_uri={redirect_uri}"
# print(authorization_url)
#
# # step2
# # 获取访问令牌
# authorization_code = ""
# access_token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
# scope = ["user.read"]
# authorization_code_body = {
#     "tenant": tenant_id,
#     "client_id": client_id,
#     "grant_type": "authorization_code",
#     "scope": scope,
#     "code": authorization_code,
#     "redirect_uri": redirect_uri,
# }
#
# token_response = requests.post(access_token_url, data=authorization_code_body).json()
# print(token_response)
#
# # step3 用刷新令牌更新过期的访问令牌
# refresh_token = ""
# access_token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
# scope = ["user.read"]
# refresh_token_body = {
#     "tenant": tenant_id,
#     "client_id": client_id,
#     "grant_type": "refresh_token",
#     "scope": scope,
#     "refresh_token": refresh_token
# }
# a = requests.post(access_token_url, data=refresh_token_body)
# refresh_token_response = requests.post(access_token_url, data=refresh_token_body).json()
# print(a.json())
# print(refresh_token_response["expires_in"])
