from models import Session, User

# create session in database if given user credentials are valid
# takes user's email and hashed password as parameters
# return session token on success, None otherwise
def login(email, password):
    u = User.objects.get(email__exact=email)
    if u.password != password:
        return None
    t = generateToken()
    s = Session(user=u, token=t, ip='0.0.0.0')
    s.save()
    return t

def logout():
    pass

# returns the user associated with the given token
# (TODO) returns None if session doesn't exist or IP is invlid
def getSession(token):
    s = Session.objects.get(token__exact=token)
    return s.user

# produce a token that doesn't already exist in the database
def generateToken():
    import string, random
    while True:
        token = ''.join(random.choice(string.hexdigits) for x in range(32))
        if len(Session.objects.filter(token__exact=token)) == 0:
            return token

