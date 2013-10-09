import bottle
from bottle import route, post, run, request
from instagram import client, subscriptions, InstagramAPI

bottle.debug(True)

CONFIG = {
    'client_id': '8052d87d8e014afbaf92d4e1f3c1318d',
    'client_secret': '4fbf525345e24e63ba999a56472cd979',
    'redirect_uri': 'http://localhost:8515/oauth_callback'
}

unauthenticated_api = client.InstagramAPI(**CONFIG)

def process_tag_update(update):
    print update

reactor = subscriptions.SubscriptionsReactor()
reactor.register_callback(subscriptions.SubscriptionType.TAG, process_tag_update)

@route('/')
def home():
    try:
        url = unauthenticated_api.get_authorize_url(scope=["basic"])
        return '<a href="%s">Log in on Instagram</a>' % url
    except Exception, e:
        print e

@route('/oauth_callback')
def on_callback():
    code = request.GET.get("code")
    if not code:
        return 'Missing code'
    try:
        access_token = unauthenticated_api.exchange_code_for_access_token(code)
        if not access_token:
            return 'Could not get access token'
        
        api = client.InstagramAPI(access_token=access_token[0])
        liked_media, next = api.user_liked_media()
        photos = []
        for media in liked_media:
            photos.append('<img src="%s"/>' % media.images['standard_resolution'].url)
        return ''.join(photos)
    except Exception, e:
        print e

run(host='localhost', port=8515, reloader=True)