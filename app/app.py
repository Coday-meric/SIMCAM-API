import json
import falcon
import rec


class RunRecSession(object):
    def on_post(self, req, resp):
        """Handles POST requests"""
        data = json.load(req.stream)
        name = data['name']
        r = rec.rec_video(name)
        if r[0] == True:
            resp.status = falcon.HTTP_200  # This is the default status
            resp.text = json.dumps({"Nom du Bénévole": name})
        else:
            resp.status = falcon.HTTP_200  # This is the default status
            resp.text = json.dumps({"state": r[1]})



class StopRecSession(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        pid = rec.unrec_video()
        resp.status = falcon.HTTP_200  # This is the default status
        resp.text = json.dumps({"Pid": pid})

class StatusRecSession(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        status = rec.status_rec()
        if status[0] == 'true':
            info = rec.info_rec(status[1])
            resp.status = falcon.HTTP_200
            resp.text = json.dumps({"id": info[0], 'name': info[1], 'file': info[2], 'time': info[3], 'status': info[4]})
        else:
            resp.status = falcon.HTTP_200  # This is the default status
            resp.text = json.dumps({"status": status})

class UploadFile(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        state = rec.upload_file()
        resp.status = falcon.HTTP_200  # This is the default status
        resp.text = json.dumps({"Status": state})


# falcon.API instances are callable WSGI apps
app = falcon.App()

# Resources are represented by long-lived class instances
run_rec = RunRecSession()
stop_rec = StopRecSession()
status_rec = StatusRecSession()
upload_file = UploadFile()

# things will handle all requests to the '/things' URL path
app.add_route('/run_rec', run_rec)
app.add_route('/stop_rec', stop_rec)
app.add_route('/status_rec', status_rec)
app.add_route('/upload_file', upload_file)
