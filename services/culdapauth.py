"""
See an example that uses basic auth with an LDAP
backend in examples/helloworld_basic_ldap.py
from: https://github.com/gmr/Tinman/blob/master/tinman/auth/ldapauth.py
"""
import ldap3 as ldap
import logging

# where to start the search for users
LDAP_SEARCH_BASE = 'dc=colorado,dc=edu'

# the server to auth against
LDAP_URL = 'ldap://directory.colorado.edu'

# The attribute we try to match the username against.
LDAP_UNAME_ATTR = 'uid'

# specific bind id for cu students
CU_BIND_ID = 'cuedupersonuuid'

# The attribute we need to retrieve in order to perform a bind.
LDAP_BIND_ATTRS = [CU_BIND_ID]

# prefered search scope
LDAP_SEARCH_SCOPE='SUBTREE'

def auth_user_ldap(uname, pwd):
    """
    Attempts to bind using the uname/pwd combo passed in.
    If that works, returns true. Otherwise returns false.
    """
    if not uname or not pwd:
        logging.error("Username or password not supplied")
        return False
    resp = user_info_ldap(uname, LDAP_BIND_ATTRS)
    if resp:
        dn = resp[0]['dn']
        server = ldap.Server(LDAP_URL, get_info=ldap.ALL, use_ssl=True)
        conn = ldap.Connection(server, user=dn, password=pwd)
        # attempt bind twice to start_tls
        # amazing hack, sam is quite proud
        if not conn.bind():
            conn.start_tls()
        conn.bind()
        logging.info('C gamma')
        result = conn.result
        if result['description'] == 'success':
            return True
        if result['description'] == 'invalidCredentials':
            logging.error("Invalid or incomplete credentials for %s", uname)
            return False
        else:
            logging.error("Auth attempt for %s had an unexpected error: %s", uname, error)
            return False
    else:
        logging.error("No user by that name")
        return False

# returns info for a user with a given uid
# return attribute values for the users ldap if they are provided
def user_info_ldap(uname, attributes=None):
    if not uname:
        logging.error("Username not supplied")
        return False
    server = ldap.Server(LDAP_URL, get_info=ldap.ALL, use_ssl=True)
    logging.info('A alpha')
    try:
        conn = ldap.Connection(server)
        conn.bind()
        conn.start_tls()
    except:
        return False
    logging.info('B beta')
    udn = conn.search(LDAP_SEARCH_BASE, '(%s=%s)' % (LDAP_UNAME_ATTR, uname), search_scope=LDAP_SEARCH_SCOPE, attributes=attributes)
    resp = conn.response
    if udn:
        return resp
    else:
        return False
