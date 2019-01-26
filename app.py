import falcon
import waitress

from HelloWorldResources import HelloWorldResource

if __name__ == '__main__':
    api = falcon.API()
    api.add_route("/hello", HelloWorldResource())
    print("Created API")
    waitress.serve(api, host='127.0.0.1', port=5555)