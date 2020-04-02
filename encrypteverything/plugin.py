# Based on https://github.com/CoinK0in/mkdocs-encryptcontent-plugin/

import os
import mkdocs
import base64
import hashlib
from Crypto import Random
from jinja2 import Template
from itertools import chain
from Crypto.Cipher import AES
from mkdocs.plugins import BasePlugin

JS_LIBRARIES = [
    '//cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.9-1/core.js',
    '//cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.9-1/enc-base64.js',
    '//cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.9-1/cipher-core.js',
    '//cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.9-1/pad-nopadding.js',
    '//cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.9-1/md5.js',
    '//cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.9-1/aes.js'
]

PLUGIN_DIR = os.path.dirname(os.path.realpath(__file__))
DECRYPT_FORM_TPL_PATH = os.path.join(PLUGIN_DIR, 'decrypt-form.tpl.html')

with open(DECRYPT_FORM_TPL_PATH, 'r') as template:
    DECRYPT_FORM_TPL = template.read()

class EncryptEverything(mkdocs.plugins.BasePlugin):
    config_scheme = (
        ('global_password', mkdocs.config.config_options.Type(str, default=None)),
    )

    def __hash_md5__(self, text):
        """ Creates an md5 hash from text. """
        key = hashlib.md5()
        key.update(text.encode('utf-8'))
        return key.digest()

    def __encrypt_text_aes__(self, text, password):
        """ Encrypts text with AES-256. """
        BLOCK_SIZE = 32
        PADDING_CHAR = b'^'
        iv = Random.new().read(16)
        # key must be 32 bytes for AES-256, so the password is hashed with md5 first
        cipher = AES.new(self.__hash_md5__(password), AES.MODE_CBC, iv)
        plaintext = text.encode('utf-8')
        # plaintext must be padded to be a multiple of BLOCK_SIZE
        plaintext_padded = plaintext + (BLOCK_SIZE - len(plaintext) % BLOCK_SIZE) * PADDING_CHAR
        ciphertext = cipher.encrypt(plaintext_padded)
        return (
            base64.b64encode(iv),
            base64.b64encode(ciphertext),
            PADDING_CHAR
        )

    def __encrypt_content__(self, content, password):
        """ Replaces page or article content with decrypt form. """
        ciphertext_bundle = self.__encrypt_text_aes__(content, password)

        decrypt_form = Template(DECRYPT_FORM_TPL).render({
            # this benign decoding is necessary before writing to the template, 
            # otherwise the output string will be wrapped with b''
            'ciphertext_bundle': b';'.join(ciphertext_bundle).decode('ascii'),
            'js_libraries': JS_LIBRARIES,
        })
        return decrypt_form

    def on_post_page(self, output, page, config):

        if 'global_password' in self.config:
            global_password = self.config.get('global_password')

            output = self.__encrypt_content__(output, global_password)

        return output