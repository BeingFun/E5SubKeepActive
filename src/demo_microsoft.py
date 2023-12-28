# step3 用刷新令牌更新过期的访问令牌
import requests

# step1 请求授权码
client_id = "94a897de-6557-4de0-8d3f-525fa6d67534"
tenant_id = "9a33b84f-5fc5-4681-bedb-022a09ba7100"
client_secret = "hKR8Q~lKkdhw.ltdGcZTXBtf12J8eWYKMfX~2a9w"
client_assertion = "6155e406-dc06-4e77-b8af-ce27a8942aa3"
scope = "openid+email+offline_access+user.read"
redirect_uri = "http://localhost:5000/getAToken"
response_type = "code"
response_mode = "query"
# refresh_token = "0.AT0AT7gzmsVfgUa-2wIqCbpxAN6XqJRXZeBNjT9SX6bWdTShAIs.AgABAAEAAAAmoFfGtYxvRrNriQdPKIZ-AgDs_wUA9P-zIi-eojTFRq9WVlRPgm_qpTDiY-B63E60nXl20kmQS5FdKlf35MW8VOutQg-E6tnUaL2iGraZPBRZTheRXQGSCEDIEln44dmJL10vf45R2QmN15GskCvJSfRbm6GK_rwdlM0MlbwZ5HyriHQzEUsdBzFXWV8bdGzYJlHM8J_PpTQOJz74lPGbQJiWZAz-DkRQSIA8QHqL3GUTmKdPAOZ-olU5z03h5C5DQPhIHdKAJl7LP8aSmEv7tvq_oHoHeJ8g9hqhH0dRSHrYDfYd12IGu2XK9LC_KNWaJZ5OL-UNyosO416UZGDlLeDpRY89VUUgBYuNQDN5FeYBkRfXWDxqxYo2E3sfK0fP0D-3MojDKFnAweNvT1_HIST4OkU471j5DC674Lg5Q2fp55-yiOsb_jrXyY6fC3S3vlzGPQpFQ2uaLMBdgW6SMfhaBHBtXTgb6x1bmPcgV-DxqrY73kRSSW7_ZFTnxPDsoim1O7l5HpU2COmDwFLsl0CcuMMG5KctWNsyxvczFYaRnoNoFJCeVSqfnW1ndlttG5eaSSXhSvDSDe6lOg3f18Yk0ELpYMJ4avuUmRVBUUiS4_IDdSp8w_MWKFQ9l9U3M6cqhSLuweBhD3NbC4aRBG0Zxi8EOIAUWOyA_0Hx9VNnQ3o06YzmUq2v_-3dExLkzvV7-yO1B27XBHVa0PB1bDfYitzkQgeQt5Y28vZfvJWgKahbeovYHxfPsDgRKlafIHdN-FaLbP4refEWWjF6r6Jw8ag0FYT9JrWqnGNdNdiGq0aUKdoQrdXkFziMlT4SwcAcDAxNofYat-E5zhAPvLPj3QDdvjKeNryeHqcZlr0Zs1QFADLzxO9TsqM3gf9aZJaAZ9DCslxH_ZHLeG9YJ3z5F7rZq_8zOUhG5pGEmo2mRyGj2pQZPHQfZfqku9cYaaKfJy0wndmUYFIhP_V9mjdySig8olmqJ7XRaw"

authorization_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize?&client_id={client_id}&response_type={response_type}&scope={scope}&response_mode={response_mode}&redirect_uri={redirect_uri}"
print(authorization_url)

# step2
# 获取访问令牌
authorization_code = ""
access_token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
scope = ["user.read"]
authorization_code_body = {
    "tenant": tenant_id,
    "client_id": client_id,
    "grant_type": "authorization_code",
    "scope": scope,
    "code": authorization_code,
    "redirect_uri": redirect_uri,
}

token_response = requests.post(access_token_url, data=authorization_code_body).json()
print(token_response)

# step3 用刷新令牌更新过期的访问令牌
refresh_token = "0.AT0AT7gzmsVfgUa-2wIqCbpxAN6XqJRXZeBNjT9SX6bWdTShAIs.AgABAAEAAAAmoFfGtYxvRrNriQdPKIZ-AgDs_wUA9P9OWBUTBWMxKRG8dfJUmyB2ovpwgD7quAa_rdzTRdx0h5eUJWczKmk5L3pxBhxYVgf5Z4S7j0QnOc_i30-WDs10Fya5_Ss1flS6r8WNJYoU3hyFPLssdTlCF3LeZqN6R1bYfwJHjuM526AAKvd6Z1TO_9eWaegRypJ9OAmkwD6nNNQvO5jyhc9BR3bUYqkgfcdFYEWXLG62kvL8Ucu39nFBhVqEsvEIiXSh7MdzwBe5KutKh3_RDI5KxayjLap4ITy9ZVuFab0slA6puyCcbQbmpAQYEeceO-_Hrwpgbc8plLvEqGAqSjJBdmTZi8IXDnqydNtpXHEGhr-T_iqAPJkWDJEzdfOv4OdqImKAZlsN3_EQgkvz9fx19lOzC9ILsUHnZhWKkr6H9VVTzQGoIa4AptMx6C9hwakjfeY4CLkeW7fkOnCuR-DyoiLP8t2m1VWye5zc9fyEgLx4tJqqH_PjEd0XpngXdcd0JLr2436QUYXlgbnB4qpFEhgghZnajlu3_9O0bra4ZLro01z5TevvT3yEHNj-51-zipGGErndkuP6XRxB3y7o75GDpuXCQEJHVfyOpfk3vva5zM_UNPc8oFG93Vu4jluSxjFmwGWgRLauwmqlrBgWCd-eI5hoI05cwW2WSEcp5aFaASk76n2qek-q6A9tt1UNsJkQZrnBbFyJfB1d1DaK3ekkjrRqj49UA1sPTMpgMaLHolGCtDqG-sAclAS_Fz9ZLOmElslpd5rH6vw286tWZ-P36PIXAPG8pjVlbq5jWX4SyjVyRyvjqM6tOgCg7rgzHOOtZO315cxhkennJ3bpAfsVmR4eGt4a-EoTcSbkttN0cxmo0vgHWJqRipQoeaVwAx9IvYzUJRD-UHk6HBOENNN1yfrG2Y4OqxHhwpdOWF7akbGTBdl0B4zhqhBeDznhag0vp3Okhit0orce86iehNaqSl0Qa4AioS6cpQ"
access_token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
scope = ["user.read"]
refresh_token_body = {
    "tenant": tenant_id,
    "client_id": client_id,
    "grant_type": "refresh_token",
    "scope": scope,
    "refresh_token": refresh_token
}
a = requests.post(access_token_url, data=refresh_token_body)
refresh_token_response = requests.post(access_token_url, data=refresh_token_body).json()
print(a.json())
print(refresh_token_response["expires_in"])
