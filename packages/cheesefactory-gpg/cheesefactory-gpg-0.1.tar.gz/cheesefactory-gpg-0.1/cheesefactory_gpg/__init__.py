# cheesefactory_gpg/__init__.py

import logging
from typing import List

import gnupg

logger = logging.getLogger(__name__)


class CfGpg:
    def __init__(self, key_file: str = None):
        """GPG encrypt and decrypt.

        Args:
            key_file:
        """
        self.gpg = gnupg.GPG()
        self.log = {
            'gpg_actions': [],
            'gpg_suffix': None,
            'gpg_note': '',
            'gpg_keys': [],
        }

        if key_file is not None:
            self.load_key(key_file=key_file)

    def load_key(self, key_file: str = None):
        """Load a public or private key into a GPG instance."""
        self.log['gpg_keys'].append(key_file)
        self.log['gpg_note'] = f'Importing key: {key_file}'

        with open(key_file) as fp:
            key_data = fp.read()
        import_result = self.gpg.import_keys(key_data)

        for result in import_result.results:
            logger.debug(f'GPG key load: {result}')
        self.log['gpg_note'] = ''

    def decrypt(self, destination_path: str = None, passphrase: str = None, source_path: str = None):
        """Decrypt file.

        Args:
            destination_path: Decrypted target filename.
            passphrase: Passphrase for GPG key.
            source_path: Encrypted source filename.
        """
        if not isinstance(destination_path, str):
            raise ValueError('destination != str type')
        if not isinstance(passphrase, str):
            raise ValueError('passphrase != str type')
        if not isinstance(source_path, str):
            raise ValueError('source != str type')

        log = {
            'action': 'decrypt',
            'action_ok': False,
            'destination': destination_path,
            'note': None,
            'passphrase': passphrase,
            'source': source_path,
        }
        logger.debug(f'Decrypt file: {source_path} -> {destination_path}')

        try:
            with open(source_path, 'rb') as fp:
                status = self.gpg.decrypt_file(file=fp, passphrase=passphrase, output=destination_path)

            logger.debug(f'CfGpg.decrypt_file ok: {status.ok}')
            logger.debug(f'CfGpg.decrypt_file status: {status.status}')
            logger.debug(f'CfGpg.decrypt_file stderr: {status.stderr}')

            log['action_ok'] = status.ok
            if status.ok is False:  # Encryption failed
                log['note'] = status.status
                raise IOError(f'CfGpg.decrypt() failed: {status.status}; {status.stderr}')

        except IOError as e:
            log['note'] = f'IOError: {e}'  # Could be from open() or decrypt_file()
            raise

        else:
            log['note'] = ''
            log['action_ok'] = True

        finally:
            self.log['gpg_actions'].append(log)

    def encrypt(self, destination_path: str = None, passphrase: str = None, recipients: List = None,
                source_path: str = None):
        """Encrypt file.

        Args:
            destination_path: Encrypted target filename.
            passphrase: Passphrase for GPG key.
            recipients:
            source_path: Unencrypted source filename.
        """
        if not isinstance(destination_path, str):
            raise ValueError('destination != str type')
        if not isinstance(passphrase, str):
            raise ValueError('passphrase != str type')
        if not isinstance(source_path, str):
            raise ValueError('source != str type')

        log = {
            'action': 'encrypt',
            'action_ok': False,
            'destination': destination_path,
            'note': None,
            'passphrase': passphrase,
            'recipients': recipients,
            'source': source_path,
        }
        logger.debug(f'Encrypt file: {source_path} -> {destination_path}')

        try:
            with open(source_path, 'rb') as fp:
                status = self.gpg.encrypt_file(file=fp, passphrase=passphrase, output=destination_path,
                                               recipients=recipients)

            logger.debug(f'CfGpg.encrypt_file ok: {status.ok}')
            logger.debug(f'CfGpg.encrypt_file status: {status.status}')
            logger.debug(f'CfGpg.encrypt_file stderr: {status.stderr}')

            log['action_ok'] = status.ok
            if status.ok is False:  # Encryption failed
                log['note'] = status.status
                raise IOError(f'CfGpg.encrypt() failed: {status.status}; {status.stderr}')

        except IOError as e:
            log['note'] = f'IOError: {e}'  # Could be from open() or decrypt_file()
            raise

        else:
            log['action_ok'] = True
            log['note'] = ''

        finally:
            self.log['gpg_actions'].append(log)

    @staticmethod
    def find_new_name(path, log):
        for action in log['gpg_actions']:
            if action['source'] == path:  # If we found the old file path name, ...
                return action['destination']  # ...then return the new file path name.
        return None
