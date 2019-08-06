from webapp import WebApp 

def say(method, path, body):
    message = 'I said {0}'.format(body)
    return 200, message

handlers = {
    ('/', 'GET'): lambda method, path, body: (200, "<h3>Home</h3>"),
    ('/say', 'POST'): say
}

def main():
    web_app = WebApp('0.0.0.0', 82, handlers)
    web_app.start()

if __name__ == "__main__":
    main()