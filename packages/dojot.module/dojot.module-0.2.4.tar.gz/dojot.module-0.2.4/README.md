# dojot-module-python [![PyPI version](https://badge.fury.io/py/dojot.module.svg)](https://badge.fury.io/py/dojot.module)

Common library to be used within dojot modules.

**Attention**: As of version v2.0, this library no longer has integration with the old "auth" service, but with the "keycloak" service.
Be aware that the environment variables `KEYCLOAK_USER` and `KEYCLOAK_PASSWORD` will probably have to be passed to services that use this library. This user should be able to get the existing realm lists from keycloak.
