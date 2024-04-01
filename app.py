from flask import Flask, render_template, request,jsonify,send_file
from subprocess import Popen, PIPE
import os
import requests

app = Flask(__name__)

rec_info = {}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_playbook', methods=['POST'])
def run_playbook():

    git_url = request.form['git_url']
    github_token = request.form['github_token']
    git_clone(git_url, github_token)
    
    playbook_file = request.form['playbook_file']
    playbook = os.path.join(os.path.dirname(__file__), 'playbooks', playbook_file)  
    inventory = os.path.join(os.path.dirname(__file__), 'inventories', 'hosts')  
    cmd = ['ansible-playbook', '-i', inventory, playbook]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    output, error = p.communicate()
    if p.returncode == 0:
        result = "Playbook executed successfully:\n" + output.decode('utf-8')
    else:
        result = "Error executing playbook:\n" + error.decode('utf-8')
    return result

def git_clone(git_url, github_token):
    
    local_repo_path = os.path.join(os.path.dirname(__file__), 'playbooks')
    
    
    if not os.path.exists(local_repo_path):
        cmd = ['git', 'clone', git_url, local_repo_path]
        env = os.environ.copy()
        env['GITHUB_TOKEN'] = github_token
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, env=env)
        output, error = p.communicate()
        if p.returncode != 0:
            print("Error cloning repository:", error.decode('utf-8'))
    else:
        cmd = ['git', 'pull']
        env = os.environ.copy()
        env['GITHUB_TOKEN'] = github_token
        p = Popen(cmd, cwd=local_repo_path, stdout=PIPE, stderr=PIPE, env=env)
        output, error = p.communicate()
        if p.returncode != 0:
            print("Error pulling repository:", error.decode('utf-8'))

     
@app.route('/receive_info', methods=['POST','GET'])
def receive_info():
    global rec_info 
    if request.method == 'POST':
        info = request.json  
        #print("Received info:", info)
        rec_info = info
        #return 'Info received successfully'
        #return  render_template('hosts.html',info=info)
        return jsonify(info)  
    else:
    	if rec_info is None or len(rec_info) == 0:  
            return 'No hosts'
    	else:
            return render_template('hosts.html', info=rec_info)
            #return jsonify(rec_info)

@app.route('/add_host', methods=['POST'])
def add_host():
    INVENTORY_PATH = 'inventories/hosts'
    data = request.get_json()
    host_ip = data['hostIp']
    if host_ip:
        with open(INVENTORY_PATH, 'r') as inventory_file:
            lines = inventory_file.readlines()
            host_count = sum(1 for line in lines if line.startswith('rpi'))

        hostname = f'rpi{host_count + 1}'

        host_info = f'\n{hostname} ansible_host={host_ip}'

        with open(INVENTORY_PATH, 'a') as inventory_file:
            inventory_file.write(host_info)

        return 'Success: Host added to hosts'

    return 'Error: Please provide a valid Host IP'
    
@app.route('/update_package', methods=['POST'])
def update_package():
    #playbook = request.form.get('playbook')
    playbook = os.path.join(os.path.dirname(__file__), 'playbooks', 'update.yml')
    inventory = os.path.join(os.path.dirname(__file__), 'inventories', 'hosts')
    cmd = ['ansible-playbook', '-i', inventory, playbook]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    output, error = p.communicate()
    if p.returncode == 0:
        result = "Playbook executed successfully:\n" + output.decode('utf-8')
    else:
        result = "Error executing playbook:\n" + error.decode('utf-8')
    return result
    
@app.route('/download_file', methods=['POST'])
def download_file():
    file_url = request.form['file_url']

    try:
        response = requests.get(file_url)
        if response.status_code == 200:
            file_name = file_url.split('/')[-1]
            
            with open(file_name, 'wb') as f:
                f.write(response.content)
            
            return send_file(file_name, as_attachment=True)
        else:
            return "Failed to download file."
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=5000)
