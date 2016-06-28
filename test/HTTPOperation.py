import httplib2

http = httplib2.Http('.cache')


def post_service(url, headers, body):
    response, content = http.request(url, 'POST', headers=headers, body=body)
    print(response.status)
    print(content)


def put_service(url, headers, body):
    response, content = http.request(url, 'PUT', headers=headers, body=body)
    print(response.status)
    print(content)


def delete_service(url):
    response, content = http.request(url, 'DELETE')
    print(response.status)
    print(content)


def get_service(url, headers):
    response, content = http.request(url, 'GET', headers=headers)
    print(response.status)
    print(str(content))


if __name__ == '__main__':
    url = 'http://127.0.0.1:5000/url/2'
    body = '{"title": "second url", "url": "http://localhost1:5000/urls", "description": "my seconf url"}'
    headers = {'content-type': 'application/json'}
    #post_service(url, headers, body)
    #get_service(url, headers)
    delete_service(url)

