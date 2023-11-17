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
            resp.text = json.dumps({"volunteer name": name})
        else:
            resp.status = falcon.HTTP_200  # This is the default status
            resp.text = json.dumps({"status": res[1]})

class StopRecSession(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        r = Rec()
        path = r.unrec_video()
        resp.status = falcon.HTTP_200  # This is the default status
        resp.text = json.dumps({"path": path})

class StatusRecSession(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        r = Rec()
        status = r.status_rec()
        if status[0] == True:
            info = r.info_rec()
            resp.status = falcon.HTTP_200
            resp.text = json.dumps({"pid": info[0], 'name': info[1], 'file': info[2], 'path': info[3], 'time': info[4], 'status': info[5]})
        else:
            resp.status = falcon.HTTP_200  # This is the default status
            resp.text = json.dumps({"status": status})

class UploadFile(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        r = Upload()
        status = r.upload_file()
        resp.status = falcon.HTTP_200  # This is the default status
        resp.text = json.dumps({"status": status})

class RunPreview(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        r = Preview()
        status = r.run_preview()
        resp.status = falcon.HTTP_200  # This is the default status
        resp.text = json.dumps({"status": status})

class StopPreview(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        r = Preview()
        status = r.stop_preview()
        resp.status = falcon.HTTP_200  # This is the default status
        resp.text = json.dumps({"status": status})

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
