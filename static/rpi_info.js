function fetchDeviceInfo() {
    fetch('http://192.168.0.65:5000/receive_info',{
    	method = 'POST'}
    )
        .then(response => response.json())
        .then(data => {
            displayDeviceInfo(data);
        })
        .catch(error => {
            console.error('Error fetching device info:', error);
        });
}

var hostData = {{ info | tojson | safe }};

function displayDeviceInfo(data) {
    console.log('Displaying device info:', data);
    const deviceInfoDiv = document.getElementById('deviceInfo');
    deviceInfoDiv.innerHTML = ''; 

    for (const [hostname, hostData] of Object.entries(data)) {
        const infoDiv = document.createElement('div');
        infoDiv.classList.add('info');

        const nameHeading = document.createElement('h2');
        nameHeading.textContent = `Host: ${hostname}`;
        infoDiv.appendChild(nameHeading);

        const cpuUsageSpan = document.createElement('span');
        cpuUsageSpan.classList.add('info-label');
        cpuUsageSpan.textContent = 'CPU Usage: ';
        const cpuUsageValue = document.createElement('span');
        cpuUsageValue.textContent = `${hostData.cpu_usage}%`;
        infoDiv.appendChild(cpuUsageSpan);
        infoDiv.appendChild(cpuUsageValue);
        infoDiv.appendChild(document.createElement('br'));

        const memoryUsageSpan = document.createElement('span');
        memoryUsageSpan.classList.add('info-label');
        memoryUsageSpan.textContent = 'Memory Usage: ';
        const memoryUsageValue = document.createElement('span');
        memoryUsageValue.textContent = `${hostData.memory_usage}%`;
        infoDiv.appendChild(memoryUsageSpan);
        infoDiv.appendChild(memoryUsageValue);
        infoDiv.appendChild(document.createElement('br'));

        const networkInfoSpan = document.createElement('span');
        networkInfoSpan.classList.add('info-label');
        networkInfoSpan.textContent = 'Network Info: ';
        const networkInfoPre = document.createElement('pre');
        networkInfoPre.textContent = JSON.stringify(hostData.network_info, null, 2);
        infoDiv.appendChild(networkInfoSpan);
        infoDiv.appendChild(networkInfoPre);

        deviceInfoDiv.appendChild(infoDiv);
    }
}

function addHost() {
    var hostIp = document.getElementById('hostIp').value;
    if (hostIp.trim() !== '') {
        fetch('/add_host', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ hostIp: hostIp })
        })
        .then(response => response.text())
        .then(data => {
            console.log(data);
            alert('已將 ' + hostIp + ' 新增到 Inventory.ini');
        })
        .catch(error => {
            console.error('新增 Host 發生錯誤:', error);
            alert('新增 Host 發生錯誤');
        });
    } else {
        alert('請輸入有效的 Host IP');
    }
}
//fetchDeviceInfo();
displayDeviceInfo(hostData);

setInterval(fetchDeviceInfo,5000); // 每 5 秒刷新一次
