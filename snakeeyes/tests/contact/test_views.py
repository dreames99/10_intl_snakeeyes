from flask import url_for, app

from lib.tests import assert_status_with_message


class TestContact(object):
    def test_contact_page(self, client):
        """ Contact page should respond with a success 200. """
        response = client.get(url_for('contact.index'))
        assert response.status_code == 200

    def test_contact_form(self, client):
        """ Contact form should redirect with a message. """
        form = {
          'email': 'info@rmsfinance.com',
          'message': 'Test message from Snake Eyes.'
        }
        # !!!!  turn-off CSRF??  !!!!
        from flask import current_app
        current_app.config['WTF_CSRF_ENABLED'] = False
        response = client.post(url_for('contact.index'), data=form,
                               follow_redirects=True)
        assert_status_with_message(200, response, 'Thanks')
        # assert_status_with_message(221, response, 'Thanks')
