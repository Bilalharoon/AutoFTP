from flask import *
import sys
import os
import ftputil

app = Flask(__name__)
ftp = ftputil.FTPHost("ftp.aamirharoon.com", "bilal@bilal.aamirharoon.com", "Fozia814")

@app.route("/", methods=['POST'])
def index():
    response = json.dumps(request.json)
    print(response, file=sys.stderr)
    # update_repo()
    ftp_to_server()
    return response

def update_repo():
    os.chdir("./CodingAdventures")
    os.system("git pull")
    os.system("yarn docs:build")

def ftp_to_server():

    dirname = "/home/pi/Projects/AutoFTP/CodingAdventures/blog/.vuepress/dist"
    
    
    for filename in ftp.listdir("/"):
        if ftp.path.isdir(filename):
            print("deleting directory: " + filename, file=sys.stderr)
            ftp.rmtree(filename)
        else:
            print("deleting file: " + filename, file=sys.stderr)
            ftp.remove(filename)
    upload_to_server(dirname)
def upload_to_server(dirname):

    for root, dirs, filenames in os.walk(dirname):
        
        #if os.path.split(root)[1] != 'dist':
        ftp.chdir(root.split('dist')[1])
        
        for name in filenames:
            path = os.path.join(root, name)
            f = open(path)
            print("uploading: " + name, file=sys.stderr)
            ftp.upload(path, name)
            f.close()
        for d in dirs:
            print("creating directory: " + d, file=sys.stderr)
            ftp.mkdir(d)
        

if __name__ == "__main__":
    app.run(port=3000, debug=True, host="0.0.0.0")
    ftp.close()
