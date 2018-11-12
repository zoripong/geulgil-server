import pytest
import json
from flask import url_for


@pytest.mark.usefixtures('client_class')
class TestLogin:
    def test_login(self, client):
        assert client.get(url_for('stafflogin')).status_code == 405
        res = client.post('/login',
                          data=json.dumps(dict(staff_name='test24',
                                               staff_password='test')),
                          content_type='application/json',
                          follow_redirects=True)

        invalid_password_json = dict(message="not match",
                                     errors=dict(
                                         resource="Login",
                                         code="invalid",
                                         field="staff_authentication",
                                         stack_trace=None, ),
                                     )
        assert json.loads(res.data) == invalid_password_json
