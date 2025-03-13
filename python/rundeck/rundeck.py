import requests

class RundeckHttpApi:
    def __init__(self, server_url, username, password):
        self.server_url = server_url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self._set_cookies(username, password)

    def _set_cookies(self, username, password):
        url = f'{self.server_url}/j_security_check'
        data = {
            'j_username': username,
            'j_password': password,
        }
        r = self.session.post(url, data=data, allow_redirects=False)
        self.session.cookies = r.cookies
        sessionid = r.headers.get("Set-Cookie").split(';')[0].split('=')[1]
        self.session.cookies['sessionid'] = sessionid
        return True

    def get_execution_output_html(self, project, execution_id):
        url = f'{self.server_url}/project/{project}/execution/renderOutput/{execution_id}'
        params = {
            'ansicolor': 'on',
            'loglevels': 'on',
            'convertContent': 'on',
        }
        return self.session.get(url, params=params)

if __name__ == '__main__':
    cli = RundeckHttpApi('http://localhost:4440', username='admin', password='')
    res = cli.get_execution_output_html('43', '6915')
    print(res)