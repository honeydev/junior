from flask import url_for

from tests.base import BaseTest


class TestIndexView(BaseTest):

    def test(self):
        response = self.client.get(url_for('.index'))
        self.assert200(response)
