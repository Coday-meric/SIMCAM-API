import json
import falcon
from utils import Upload, Rec, Preview


class RunRecSession(object):
    def on_post(self, req, resp):
        """Handles POST requests"""
        data = json.load(req.stream)
        name = data['name']
        r = Rec()
        res = r.rec_video(name)
        if res[0] == True:
            resp.status = falcon.HTTP_200  # This is the default status
            resp.text = json.dumps({"Nom du Bénévole": name})
        else:
            resp.status = falcon.HTTP_200  # This is the default status
            resp.text = json.dumps({"state": res[1]})

class StopRecSession(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        r = Rec()
        r.unrec_video()
        resp.status = falcon.HTTP_200  # This is the default status
        resp.text = json.dumps({"Path": r})

class StatusRecSession(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        r = Rec()
        status = r.status_rec()
        if status[0] == 'true':
            info = r.info_rec(status[1])
            resp.status = falcon.HTTP_200
            resp.text = json.dumps({"id": info[0], 'name': info[1], 'file': info[2], 'time': info[3], 'status': info[4]})
        else:
            resp.status = falcon.HTTP_200  # This is the default status
            resp.text = json.dumps({"status": status})

class UploadFile(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        r = Upload()
        state = r.upload_file()
        resp.status = falcon.HTTP_200  # This is the default status
        resp.text = json.dumps({"Status": state})

class RunPreview(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        r = Preview()
        state = r.run_preview()
        resp.status = falcon.HTTP_200  # This is the default status
        resp.text = json.dumps({"Status": state})

class StopPreview(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        r = Preview()
        state = r.stop_preview()
        resp.status = falcon.HTTP_200  # This is the default status
        resp.text = json.dumps({"Status": state})

# falcon.API instances are callable WSGI apps
app = falcon.App()

# Resources are represented by long-lived class instances
run_rec = RunRecSession()
stop_rec = StopRecSession()
status_rec = StatusRecSession()
upload_file = UploadFile()
run_preview = RunPreview()
stop_preview = StopPreview()

# things will handle all requests to the '/things' URL path
app.add_route('/rec', run_rec)
app.add_route('/unrec', stop_rec)
app.add_route('/status', status_rec)
app.add_route('/upload', upload_file)
app.add_route('/preview', run_preview)
app.add_route('/unpreview', stop_preview)
