from flask import Flask, render_template, request
from subprocess import Popen, PIPE
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_playbook', methods=['POST'])
def run_playbook():

    git_url = request.form['git_url']
    github_token = request.form['github_token']
    git_clone(git_url, github_token)
    
    playbook_file = request.form['playbook_file']
    playbook = os.path.join(os.path.dirname(__file__), 'playbooks', playbook_file)  # 使用相對路徑設置 playbook 的路徑
    inventory = os.path.join(os.path.dirname(__file__), 'inventories', 'hosts')  # 使用相對路徑設置 inventory 的路徑
    cmd = ['ansible-playbook', '-i', inventory, playbook]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    output, error = p.communicate()
    if p.returncode == 0:
        result = "Playbook executed successfully:\n" + output.decode('utf-8')
    else:
        result = "Error executing playbook:\n" + error.decode('utf-8')
    return result

def git_clone(git_url, github_token):
    # 指定本地存儲庫路徑
    local_repo_path = os.path.join(os.path.dirname(__file__), 'playbooks')
    
    # 檢查本地存儲庫是否存在，如果不存在則克隆
    if not os.path.exists(local_repo_path):
        # 使用 Personal Access Token 進行拉取操作
        cmd = ['git', 'clone', git_url, local_repo_path]
        env = os.environ.copy()
        env['GITHUB_TOKEN'] = github_token
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, env=env)
        output, error = p.communicate()
        if p.returncode != 0:
            print("Error cloning repository:", error.decode('utf-8'))
    else:
        # 如果本地存儲庫已經存在，則更新它
        cmd = ['git', 'pull']
        env = os.environ.copy()
        env['GITHUB_TOKEN'] = github_token
        p = Popen(cmd, cwd=local_repo_path, stdout=PIPE, stderr=PIPE, env=env)
        output, error = p.communicate()
        if p.returncode != 0:
            print("Error pulling repository:", error.decode('utf-8'))


if __name__ == '__main__':
    app.run(debug=True)
