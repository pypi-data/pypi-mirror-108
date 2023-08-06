"""Declares :class:`EllipticCurvePublicKey`."""
import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.asymmetric import ec

from ..public import PublicKey


class EllipticCurvePublicKey(PublicKey):

    def __init__(self, key, capabilities=None):
        self.__public = key
        self.capabilities = capabilities or self.capabilities

    async def encrypt(self, *args, **kwargs):
        raise NotImplementedError

    async def verify(self, signature: bytes, blob: bytes,
        hasher, algorithm, *args, **kwargs) -> bytes:
        hasher.update(blob)
        digest = hasher.finalize()
        try:
            self.__public.verify(
                bytes(signature), digest,
                ec.ECDSA(utils.Prehashed(algorithm))
            )
            return True
        except InvalidSignature:
            return False
