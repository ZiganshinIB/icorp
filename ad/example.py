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
        self.LDAP_DOMAIN = env.str('LDAP_DOMAIN', '')


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

    def create_user(self, username, first_name, last_name, position, path_ou, email, password, surname=None):
        if not self.is_connected():
            return False
        surname = f" {surname}" if surname else ''
        user_cn = f"{last_name} {first_name}{surname}"
        user_dn = f"cn={user_cn},{path_ou},{self.dc}"
        attributes = {
            'displayName': user_cn,
            'givenName': first_name,
            'sn': last_name,
            'sAMAccountName': username,
            'userPrincipalName': f"{username}@{settings.LDAP_DOMAIN}",
            'mail': email,
            'title': position,
        }

        try:
            self.connection.add(dn=user_dn, attributes=attributes, object_class='user')
            self.connection.extend.microsoft.unlock_account(user_dn)
            self.reset_password(username, password)
            change_uac_attribute = {
                "userAccountControl": [(MODIFY_REPLACE, [66048])]}
            print("Successfully created user.")
            return True
        except Exception as e:
            print(f"Failed to create user: {e}")
            return False

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

    def reset_password(self, username, new_password):
        powershell_script = f'Set-ADAccountPassword {username} -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "{new_password}" -Force -Verbose) -PassThru'
        subprocess.run(['powershell', powershell_script])

    def disconnect(self):
        if self.connection:
            self.connection.unbind()
            print("Disconnected from LDAP.")

    def is_connected(self):
        return self.connection is not None

    def search_group(self,
                     name,
                     attributes=['DistinguishedName', 'GroupCategory', 'SamAccountName', 'Members']):
        if not self.is_connected():
            return None
        search_filter = f'(&(CN={name})(ObjectClass=group))'
        self.connection.search(
            self.dc,
            search_filter
        )
        if len(self.connection.entries) > 0:
            return self.connection.entries[0]
        else:
            return None

    def get_user_groups(self,
                        username
                        ):
        if not self.is_connected():
            return None
        search_filter = f'(sAMAccountName={username})'
        self.connection.search(
            self.dc,
            search_filter,
            attributes=['memberOf']
        )
        if len(self.connection.entries) > 0:
            return self.connection.entries[0].memberOf
        else:
            return None

    def get_object_by_ds(self, ds_name, attributes=['DistinguishedName', 'sAMAccountName', 'userPrincipalName', 'objectClass', 'memberOf']):
        if not self.is_connected():
            return None
        search_filter = f'(distinguishedName={ds_name})'
        self.connection.search(
            self.dc,
            search_filter,
            attributes=attributes
        )
        if len(self.connection.entries) > 0:
            return self.connection.entries[0]
        else:
            return None

    def get_all_groups(self, attributes=['CN', 'DistinguishedName', 'SamAccountName', 'objectClass', 'member',]):
        if not self.is_connected():
            return None
        search_filter = '(objectClass=group)'
        self.connection.search(
            self.dc,
            search_filter,
            attributes=attributes
        )
        if len(self.connection.entries) > 0:
            return self.connection.entries
        else:
            return None



def main():
    ldap = LDAPService()
    ldap.connect()
    res = ldap.search_user('ilmir.ziganshin')
    print(res)
    res = ldap.search_group('ОИТ')
    print(res)
    res = ldap.get_user_groups('ilmir.ziganshin')
    print(res)
    res = ldap.get_all_groups()
    print(res)
    for r in res:
        print(r['SamAccountName'])
    # res = ldap.create_user(
    #     username='testuser',
    #     first_name='Тест',
    #     last_name='пользователь',
    #     position='Администратор',
    #     path_ou='OU=ОИТ',
    #     email='testuser@icorp.com',
    #     password='password')
    # print(res)
    ldap.disconnect()


if __name__ == '__main__':
    env = Env()
    env.read_env()
    settings = Settings()
    main()
