# encrypt_tools: encrypt and decrypt


[![Github License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Updates](https://pyup.io/repos/github/woctezuma/google-colab-transfer/shield.svg)](pyup)
[![Python 3](https://pyup.io/repos/github/woctezuma/google-colab-transfer/python-3-shield.svg)](pyup)
[![Code coverage](https://codecov.io/gh/woctezuma/google-colab-transfer/branch/master/graph/badge.svg)](codecov)




encrypt_tools is a Python package of low-level cryptographic primitives.

Installation
============
The code is packaged for PyPI, so that the installation consists in running:
```sh
pip install encrypt-tools
```


Usage AES
=====
    from encrypt_tools import CryptoAes
    from encrypt_tools import generate_b64decode
    
    KEY = generate_b64decode("onAGSOj7NXlJo0xo5iorF3vQT+ip/uRBcZDMuEljyCo=")
    IV = generate_b64decode("WvdNOBeWH+nApbbqz/WAZg==")
    
    cipher = CryptoAes()
    text = "51123456789"
    
    encrypt = cipher.encrypt(text, KEY, IV)
    print(f'encrypt:\n{encrypt}')
    
    decrypt = cipher.decrypt(encrypt, KEY, IV)
    print(f'decrypt:\n{decrypt}')


Usage RSA
=====
    from encrypt_tools import CrypyoRsa
    from encrypt_tools import generate_key_pair

    cipher = CrypyoRsa()
    text = "51955376623"
    
    passphrase_private = "passphrase_private"
    passphrase_public = "passphrase_public"
    generate_key_pair(passphrase_private,
                      passphrase_public)
    
    encrypt = cipher.encrypt(text, passphrase_public)
    print(f'encrypt:\n{encrypt}')
    
    decrypt = cipher.decrypt(encrypt, passphrase_private)
    print(f'decrypt:\n{decrypt}')


Usage RSA Files
==============
    from encrypt_tools import CryptoFiles
    from pathlib import Path

    cipher = CryptoFiles()
    text = "51955376623"
    passphrase_private = "passphrase_private"
    passphrase_public = "passphrase_public"
    
    private_key = Path('private.pem')
    public_key = Path('public.pem')
    unencrypted_file = Path('file.txt')
    
    encrypt = cipher.encrypt(unencrypted_file, public_key, passphrase_public)
    print(f'encrypt:\n{encrypt}')
    
    
    decrypt = cipher.decrypt(encrypt, private_key, passphrase_private)
    print(f'decrypt:\n{decrypt}')

## License

[Apache License 2.0](https://www.dropbox.com/s/8t6xtgk06o3ij61/LICENSE?dl=0).


## New features v1.0

 
## BugFix
- choco install visualcpp-build-tools



## Reference

 - Jonathan Quiza [github](https://github.com/jonaqp).
 - Jonathan Quiza [RumiMLSpark](http://rumi-ml.herokuapp.com/).
 - Jonathan Quiza [linkedin](https://www.linkedin.com/in/jonaqp/).
