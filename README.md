About
=====

This product is Graphical User Interface(CUI) for [CloudConductor](https://github.com/cloudconductor/cloud_conductor).


Requirement
============

- Redhat Linux or CentOS (>=6.5, >=7.0)
- CloudConductor 2.0.0

Quick Start
===========

## Install dependencies
 ```
$ sudo yum -y update
$ sudo yum install -y wget git zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc

# Python
$ cd ~/
$ wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz
$ tar zxvf Python-3.4.3.tgz
$ cd Python-3.4.3
$ ./configure --prefix=/usr/local
$ sudo make
$ sudo make install
$ python3.4 -V
   Python 3.4.3
$ pip3.4 -V
   pip 6.0.8 from /usr/local/lib/python3.4/site-packages (python 3.4)
```
## Install CloudConductor GUI
```
$ cd ~/
$ git clone https://github.com/cloudconductor/cloud_conductor_gui.git
$ cd cloud_conductor_gui
$ sudo /usr/local/bin/pip3.4 install -r requirements.txt
$ python3 manage.py migrate
$ sed -i -e "s|CLOUDCONDUCTOR_URL = .*|CLOUDCONDUCTOR_URL = 'http://<your-cloudconductor-host>:<your-cloudconductor-port>/api/v1/'|g" config/settings.py
```

## Run CloudConductor GUI
```
$ nohup python3 manage.py runserver 0.0.0.0:8000 &
```

Please access to http://\<your-cloudconductor-gui-host\>:8000/ccgui/

Copyright and License
=====================

Copyright 2016 TIS inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Contact
========

For more information: <http://cloudconductor.org/>

Report issues and requests: <https://github.com/cloudconductor/cloud_conductor_cli/issues>

Send feedback to: <ccndctr@gmail.com>
