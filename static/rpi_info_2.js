var hostData = {{ info | tojson | safe }};

        console.log(hostData);
        var hostInfoDiv = document.getElementById('deviceInfo');

        for (var hostname in hostData) {
            if (hostData.hasOwnProperty(hostname)) {
                var hostDiv = document.createElement('div');
                hostDiv.classList.add('info');

                var nameHeading = document.createElement('h2');
                nameHeading.textContent = 'Host: ' + hostname;
                hostDiv.appendChild(nameHeading);

                var cpuUsageSpan = document.createElement('span');
                cpuUsageSpan.textContent = 'CPU Usage: ';
                hostDiv.appendChild(cpuUsageSpan);

                var cpuUsageValue = document.createElement('span');
                cpuUsageValue.textContent = hostData[hostname].cpu_usage + '%';
                hostDiv.appendChild(cpuUsageValue);
                hostDiv.appendChild(document.createElement('br'));

                var memoryUsageSpan = document.createElement('span');
                memoryUsageSpan.textContent = 'Memory Usage: ';
                hostDiv.appendChild(memoryUsageSpan);

                var memoryUsageValue = document.createElement('span');
                memoryUsageValue.textContent = hostData[hostname].memory_usage + '%';
                hostDiv.appendChild(memoryUsageValue);
                hostDiv.appendChild(document.createElement('br'));

                var networkInfoSpan = document.createElement('span');
                networkInfoSpan.textContent = 'Network Info: ';
                hostDiv.appendChild(networkInfoSpan);

                var networkInfoPre = document.createElement('pre');
                networkInfoPre.textContent = JSON.stringify(hostData[hostname].network_info, null, 2);
                hostDiv.appendChild(networkInfoPre);

                hostInfoDiv.appendChild(hostDiv);
            }
        }
