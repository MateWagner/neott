# NeoTT

## About Project
This is a Raspberry Pi and Python-based IoT project designed to provide a seamless IoT experience.
Imagine a scenario where someone arrives at your house and wants to turn your smart lights on or off. Traditionally, they would need to download an application to gain access and control the lights. In this project, I'm combining MQTT connectivity with a locally sourced web interface that stays in sync across all clients on every platform, allowing integration and automation via MQTT in a local environment.
The project involves the integration of four technologies: MQTT client, Web Server, socketIO, Adafruit NeoPixel, and some basic light shows in the early stages of development.

## How to use

### MQTT
The project uses [Request-Response Pattern][RRPattern-url]

#### MQTT Request-Response Pattern
It is a widely used practice in MQTT communication, and most of the clients support it.
In my implementation, with the appropriate client, on every connection, the client gets the current state of the NeoTT and keeps synchronizing all the clients while they are connected to the Broker.  
`Example:` The client sends a message to `path/topic` and over the Broker it's arriving at NeoTT. NeoTT will send the same data back on `path/topic/state` with the retain flag. During this time, the client waited for the acknowledgement to arrive on the state topic, and just when the acknowledgement arrived, it set the new state on itself.
- Don't need to keep sessions  
- Easy synchronization
- Keep sync the Clients

| topic | value |
|---|---|
| main_switch | String: ON / OFF |
| hex_rgb | String: Hexadecimal RGB #FFF / #FFFFFF |
| show_typ | String: COLOR / RAINBOW |
| wait | Float: 0.010 - 1 |
| brightness | Float: 0.010 - 1 |

## Install

### Introduction
This project should be working on various Raspberry models, but it's tested on the Raspberry Pi 4B 4GB model and the SK6812 RGBW LED strip. The biggest limitation is [Adafruit Blinka][AdafruitBlinka-url]. To get started with this project, you need to have prior knowledge of Individual addressable LED strips, aka NeoPixel, you can dive deep into [Adafruit NeoPixel Überguide][AdafruitNeoPixelÜberguide-url], and for Raspberry Pi and NeoPixels, you can read here [NeoPixels on Raspberry Pi][NeoPixelsOnRaspberryPi-url].

### Prepare Raspberry
To start the installation, you need to install Raspberry Pi OS Lite with some advanced options.
- Set a hostname
  - It helps to find the device on localhost in the background using [mDNS][mDNS-url]
- Enable SSH
  - The Lite version of Raspberry OS doesn't have a GUI you need to access your Pi via [SSH][SSH-url].
  - Ansible also works on this connection.
  - Choose your Password wisely and follow best practices, even if the Pi doesn't hang out from your network.
- Set up your WiFi network if you prefer that type of connection.
### Prepare Ansible
Ansible is an Automation platform, it requires installation on your own system, aka 'control node' and some configuration to be able to run, but on the target, aka 'Managed node' it doesn't require more than an SSH connection. I use it in my project to copy necessary files, do configuration, and install dependencies on the Raspberry to be able to run the Project. For a completely localhost, you can install the Mosquito MQTT Server if needed.
Some help to [install Ansible][InstallAnsible-url]. After installing, you need to configure your hosts and add the details of your Pi to be able to start the installation process.
- Add the following lines with your details on the Control Node to the end of the `/etc/ansible/hosts` file:
```ini
  [pi] # Name of node in Ansible
  pi.local # Hostname or ip 
    [pi:vars] # Node name and some variable for the node 
  ansible_user=username # Username what you give for the Pi installation
  ansible_ssh_pass=password # Password what you give for the Pi installation
  ansible_become=yes # To install and configure dependencies 
  ansible_become_method=sudo # Ansible need administrator access 
  ansible_become_pass=password # Password what you give for the Pi installation
```
 
### Install Mosquito (Optional)
Clone or download the project, open a terminal window in the `playbooks` folder, and run the command:
```
ansible-playbook install_mosquito.yml
```
It's going to install and configure a Mosquito Server on the Pi without any User or password. If you're intrusted, you can read more on the [Project Official page][MosquittoAuthenticaton-url]

### Configure And Install NeoTT
Clone or download the project, open a terminal window in the `playbooks` folder, and run the command:
First, open the config.yml and fill up the NeoPixel details and the MQTT details, and then run the Ansible Playbook from the playbook folder. It's going to take a while because it will update your Pi and restart it, but after that, you can go to the control page of the NeoTT `hostname.local:5000`
```
cd ./playbook
ansible-playbook install_neott_project.yml 
```
## Tech stack 

### Hardware
[![Raspberry][Raspberry-badge]][Raspberry-url]  
[![NeoPixel][NeoPixel-badge]][NeoPixel-url]
### Technologies  
[![Python][Python-badge]][Python-url]  
[![Paho MQTT][PahoMQTT-badge]][PahoMQTT-url]  
[![Flask][Flask-badge]][Flask-url]  
[![SocketIo][SocketIo-badge]][SocketIo-url]  
[![Java Script][JavaScript-badge]][JavaScript-url]  
[![Bootstrap][Bootstrap-badge]][Bootstrap-url]  
### Software
[![Mosquitto][Mosquitto-badge]][Mosquitto-url]  
[![Ansible][Ansible-badge]][Ansible-url]


<!-- Badge links -->
[Raspberry-badge]: https://img.shields.io/badge/Raspberry%20Pi-black?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white
[NeoPixel-badge]: https://img.shields.io/badge/NeoPixel-black?style=for-the-badge&logo=adafruit&logoColor=white
[Python-badge]: https://img.shields.io/badge/Python-black?style=for-the-badge&logo=python&logoColor=white 
[PahoMQTT-badge]: https://img.shields.io/badge/Paho%20MQTT-black?style=for-the-badge&logo=mqtt&logoColor=white
[Flask-badge]: https://img.shields.io/badge/Flask-black?style=for-the-badge&logo=flask&logoColor=white
[SocketIo-badge]: https://img.shields.io/badge/Socket.io-010101?&style=for-the-badge&logo=Socket.io&logoColor=white
[JavaScript-badge]: https://img.shields.io/badge/Vanilla%20Js-black?style=for-the-badge&logo=javascript&logoColor=white
[Bootstrap-badge]: https://img.shields.io/badge/bootstrap-black?style=for-the-badge&logo=bootstrap&logoColor=white
[Mosquitto-badge]: https://img.shields.io/badge/Mosquitto-black?style=for-the-badge&logo=eclipsemosquitto&logoColor=white
[Ansible-badge]: https://img.shields.io/badge/Ansible-black?style=for-the-badge&logo=ansible&logoColor=white

<!-- Project url -->
[Raspberry-url]: https://www.raspberrypi.com/
[NeoPixel-url]: https://learn.adafruit.com/neopixels-on-raspberry-pi/overview
[Python-url]: https://www.python.org/
[PahoMQTT-url]: https://eclipse.dev/paho/
[Flask-url]: https://flask.palletsprojects.com/en/2.3.x/
[SocketIo-url]: https://flask-socketio.readthedocs.io/en/latest/
[JavaScript-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript
[Bootstrap-url]: https://getbootstrap.com/
[Mosquitto-url]: https://mosquitto.org/
[Ansible-url]: https://www.ansible.com/

<!-- Background materials -->
[RRPattern-url]:https://www.hivemq.com/blog/mqtt5-essentials-part9-request-response-pattern/
[AdafruitBlinka-url]:https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
[AdafruitNeoPixelÜberguide-url]:https://learn.adafruit.com/adafruit-neopixel-uberguide
[NeoPixelsOnRaspberryPi-url]:https://learn.adafruit.com/neopixels-on-raspberry-pi/overview
[mDNS-URL]:https://en.wikipedia.org/wiki/Multicast_DNS
[SSH-url]:https://en.wikipedia.org/wiki/Secure_Shell
[InstallAnsible-url]:https://docs.ansible.com/ansible/latest/installation_guide/index.html
[MosquittoAuthenticaton-url]:https://mosquitto.org/documentation/authentication-methods/
