# from django.conf import settings
from ldap3 import Server, Connection, ALL, NTLM
from ldap3.core.exceptions import LDAPBindError
import subprocess
from dotenv import load_dotenv

from environs import Env


class Settings:
    def __init__(self):
        self.LDAP_HOST = env.str('LDAP_HOST', '')
        self.LDAP_ADMIN = env.str('LDAP_ADMIN', '')
        self.LDAP_PASSWORD = env.str('LDAP_PASSWORD', '')
        self.LDAP_SEARCH_BASE = env.str('LDAP_SEARCH_BASE', '')


class LDAPService:
    def __init__(self):
        self.server = Server(settings.LDAP_HOST, get_info=ALL)
        self.dc = settings.LDAP_SEARCH_BASE
        self.connection = None

    def search_user(self,
                    username,
                    attributes=['DistinguishedName', 'sAMAccountName', 'userPrincipalName', 'objectClass', 'memberOf']):
        if not self.is_connected():
            return None

        search_filter = f"(sAMAccountName={username})"
        self.connection.search(
            self.dc,
            search_filter,
            attributes=attributes,
        )

        if len(self.connection.entries) > 0:
            return self.connection.entries[0]
        else:
            return None

    def connect(self):
        try:
            self.connection = Connection(
                self.server,
                user=settings.LDAP_ADMIN,
                password=settings.LDAP_PASSWORD,
                authentication=NTLM,
                raise_exceptions=True
            )
            self.connection.bind()
            print("Successfully connected to LDAP.")
        except LDAPBindError as e:
            print(f"Failed to bind to LDAP: {e}")
            self.connection = None

    def disconnect(self):
        if self.connection:
            self.connection.unbind()
            print("Disconnected from LDAP.")

    def is_connected(self):
        return self.connection is not None


def main():
    ldap = LDAPService()
    ldap.connect()
    res = ldap.search_user('ilmir.ziganshin')
    print(res)
    ldap.disconnect()


if __name__ == '__main__':
    env = Env()
    env.read_env()
    settings = Settings()
    main()
