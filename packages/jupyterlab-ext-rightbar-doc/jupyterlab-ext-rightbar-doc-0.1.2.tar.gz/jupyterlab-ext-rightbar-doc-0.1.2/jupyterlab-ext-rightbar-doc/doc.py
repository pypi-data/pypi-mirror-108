import json, os
from tornado import gen, web
from notebook.base.handlers import APIHandler
CODELAB_DOCUMENT_URL = os.environ.get('CODELAB_DOCUMENT_URL') if os.environ.get('CODELAB_DOCUMENT_URL') != None else 'https://www.baidu.com'

class DocumentHandler(APIHandler):
    """
    A handler that manage codelab document.
    """

    @web.authenticated
    @gen.coroutine
    def get(self):
        self.finish({'status': '200', 'data': CODELAB_DOCUMENT_URL})