import datetime
import os
import signal
import subprocess
from pathlib import Path
import owncloud


class Rec:
    def __init__(self):
        self.status = False
        self.pid = None
        self.file_source = None
        self.file_name = None
        self.name = None
        self.time = None

    def rec_video(self, name):
        # Déclaration de variable
        self.time = datetime.datetime.now().timestamp()
        timestamp = datetime.datetime.now()
        jour = timestamp.strftime('%d-%m-%y_%Hh%M')

        # Création dossier
        path = Path('/simcam/data/temp/')
        path.mkdir(parents=True, exist_ok=True)

        # Nom fichier
        self.name = name
        self.file_name = self.name + '_' + jour + '-quality.mp4'
        self.file_source = '/simcam/data/temp/' + self.file_name

        # Démarrage VLC
        cmdbase = 'libcamera-vid --nopreview -t 0 --codec libav -o ' + self.file_source + ' --level 4.2 --framerate 30 --width 1920 --height 1080 --bitrate 5000000 --mode 1920:1080 --profile high --denoise cdn_off -n --libav-audio --audio-source alsa --audio-device default --audio-bitrate 512000'
        process = subprocess.Popen(cmdbase, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True,
                                   preexec_fn=os.setsid)
        # Stockage du PID
        self.pid = os.getpgid(process.pid)

        # Status d'enregistrement
        self.status = True

        return True, self.pid

    def unrec_video(self):
        login = 'Simon'
        password = 'tchaik0123'
        url_nextcloud = 'https://cloud.aymeric-mai.fr/'
        datetime.datetime.now().timestamp()
        timestamp = datetime.datetime.now()
        annee = timestamp.strftime('%Y')
        semaine = timestamp.strftime('%V le %m.%y')

        try:
            os.killpg(self.pid, signal.SIGINT)
        except ProcessLookupError:
            pass

        # Use owncloud library for create dir of file mp4
        try:
            oc = owncloud.Client(url_nextcloud)
            oc.login(login, password)
        except:
            pass

        try:
            oc.mkdir('Simon/Vidéos-Simon/' + annee + '')
        except:
            pass

        try:
            oc.mkdir('Simon/Vidéos-Simon/' + annee + '/Semaine-' + semaine + '')
        except:
            pass

        # Pour une utilisation de la library python
        # oc.drop_file('/home/aymeric/Codage/AEVE-REC-API/app/test.txt')

        # Changement status de l'enregistrement
        self.status = False

        # Supprimer le fichier vidéo temporaire
        # if os.path.exists(file_source):
        #    os.remove(file_source)

        return self.file_source

    def status_rec(self):
        return self.status

    def info_rec(self):
        return self.pid, self.name, self.file_name, self.file_source, self.time, self.status


class Upload:
    def upload_file(self):
        cmd_upload = '/simcam/cron/AEVE-REC_Cron.bash >> /var/log/AEVE-REC_Cron.txt'
        script = subprocess.Popen(cmd_upload, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        script = True
        return script


class Preview:
    def __init__(self):
        self.pid = None

    def run_preview(self):
        cmdbase = 'libcamera-vid -t 0 --rotation 180 --width 1920 --height 1080 --codec h264 --inline --listen -o tcp://0.0.0.0:8888'
        process = subprocess.Popen(cmdbase, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True,
                                   preexec_fn=os.setsid)
        self.pid = os.getpgid(process.pid)

        script = True
        return script

    def stop_preview(self):
        try:
            os.killpg(self.pid, signal.SIGINT)
        except ProcessLookupError:
            pass

        script = True
        return script
