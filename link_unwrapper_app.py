import json

from flask import Flask
from flask_restful import Resource, Api
import flask
import requests
from werkzeug.routing import PathConverter


app = Flask(__name__, template_folder="templates")
api = Api(app)


@app.route('/index.html', methods=['GET'])
@app.route('/index.htm', methods=['GET'])
@app.route('/', methods=['GET'])
def new_checkout():
    return flask.render_template('index.jinja2')

@app.route('/css/<path:path>')
def send_css(path):
    return flask.send_from_directory('staticfiles/css', path)


@app.route('/js/<path:path>')
def send_js(path):
    return flask.send_from_directory('staticfiles/js', path)


@app.route('/fonts/<path:path>')
def send_font(path):
    return flask.send_from_directory('staticfiles/fonts', path)


@app.route('/media/<path:path>')
def send_media(path):
    return flask.send_from_directory('staticfiles/media', path)


class UnwrapLinkResource(Resource):
    def get(self, link_to_unwrap):

        get_response = requests.get(link_to_unwrap, allow_redirects=False)

        redirect_response_codes = [301, 302, 303, 307, 308]
        unwrap_response_data = {"message": None, "location": None}
        unwrap_response_code = 0

        if get_response.status_code == 404:
            unwrap_response_code = 404
        elif get_response.status_code not in redirect_response_codes:
            unwrap_response_data['message'] = f"Response code is {get_response.status_code}. Expected one of {','.join(map(lambda c: str(c), redirect_response_codes))}"
            unwrap_response_code = 412
        elif 'location' not in get_response.headers.keys():
            unwrap_response_data['message'] = "No location header in response'"
            unwrap_response_code = 417
        else:
            unwrap_response_data['location'] = get_response.headers['location']
            unwrap_response_code = 200

        unwrap_response = app.response_class(response=json.dumps(unwrap_response_data),
                                             status=unwrap_response_code,
                                             mimetype='application/json')

        return unwrap_response


class EverythingConverter(PathConverter):
    regex = '.*?'


app.url_map.converters['everything'] = EverythingConverter

api.add_resource(UnwrapLinkResource, '/api/unwraplink/<everything:link_to_unwrap>')

if __name__ == '__main__':
    app.run(debug=True)