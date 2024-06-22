from ADsession import ADsession
from ADrequests import ADrequests

ad_requests = ADrequests("http://127.0.0.1/")
print(ad_requests.get("https://music.youtube.com/").cookies)
print(ad_requests.get("https://music.youtube.com/").cookies)
print()

ad_session = ADsession("http://127.0.0.1:5000")
print(ad_session.get("https://music.youtube.com/").cookies)
print(ad_session.get("https://music.youtube.com/").cookies)
print()
