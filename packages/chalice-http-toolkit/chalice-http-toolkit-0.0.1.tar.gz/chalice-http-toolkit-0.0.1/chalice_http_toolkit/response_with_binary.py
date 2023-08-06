from chalice import Response
import os

class ResponseWithBinary(Response):
    isBase64Encoded = False
    isLocal = os.environ.get('STAGE', 'dev') == 'dev'
    def to_dict(self, binary_types=None) -> dict:
        response = super().to_dict(binary_types=binary_types)
        if self.isBase64Encoded and not self.isLocal:
            response['isBase64Encoded'] = True
        return response