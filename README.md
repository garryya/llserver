## Overview

The purpose of this exercise is to get a small sample of your code under "controlled conditions",
that we can use as a basis for discussion in the interview process. You may solve this exercise
in your own time, but we recommend that you spend no more than a few hours (<=4) on this task.

The task of this exercise is to implement a few methods of a hypothetical API server called "myapp".
This API server's main task is to authenticate users and then serve them analysis reports of
the execution of a (malicious) file in the Lastline analysis sandbox.

This distribution includes a simple skeleton of the API server, implemented in flask, as well as
a vagrant configuration that can be used to quickly get up and running with this code in a virtual
machine.


## Getting Started

The API server itself is in python and requires only:

- python 2.7
- python-flask
- python-bcrypt

You can run the server by executing:

```
$ python runserver.py
 * Running on http://0.0.0.0:8080/
 * Restarting with reloader
```

The server will then be accessible at `http://127.0.0.1:8080/`,
which should return a "hello world" message.

To make sure that we can run your solution in the same environment
and get the same results,
we recommend using vagrant to run a virtual machine running ubuntu trusty 64 bits.
For this, you will need to install the latest version of vagrant (1.8.1 at the time of writing)
from https://www.vagrantup.com/downloads.html, as well as VirtualBox or some other
virtualization software for actually running the VM.

From the root of this distribution, you can then run:

```
$ vagrant up
$ vagrant ssh
Welcome to Ubuntu 14.04.3 LTS (GNU/Linux 3.13.0-76-generic x86_64)

 ...

vagrant@vagrant-ubuntu-trusty-64:~$ cd /vagrant
vagrant@vagrant-ubuntu-trusty-64:/vagrant$ python runserver.py
 * Running on http://0.0.0.0:8080/
 * Restarting with reloader
```

Thanks to port forwarding configured between the virtual machine and the host,
the server that is running in the VM will be accessible at `http://127.0.0.1:6688/`,
which should return a "hello world" message.

The root of this distribution on the host, and the /vagrant folder in the virtual machine
are transparently mapped so that you can edit files in your host and run them in the VM.

If you want to learn more about vagrant, the getting started guide at
https://www.vagrantup.com/docs/getting-started/ provided everything
I needed to know to set up this configuration.


## Contents of this distribution

- README.md: this readme
- VagrantFile: vagrant configuration file
- bootstrap.sh: vagrant bootstrap file (installs a few extra packages in VM)
- runserver.py: entry point for flask API server
- myapp/: implementation skeleton of myapp. Put all your code here
- myapp_test: put your tests here
- data/credentials.db: sqlite3 file containing user accounts and their permissions
- data/passwords.txt: plain-text passwords of the users in the credentials db, so you can actually test things
- data/reports: raw reports to be processed and served to users


## What to implement

A few methods relating to authentication to this API. The skeleton and 
documentation for what these methods should do exactly is found in `myapp/views/auth.py`:

- login
- whoami
- logout

A few methods for serving reports to authenticated users. The skeleton
and documentation for what these methods should do is found in `myapp/views/report.py`:

- get_report
- get_full_report

A user of this API will send a request to the login method to establish
a session, then use this session to invoke the other methods in the API,
such as fetching reports. 

In addition to implementing these functions, please write some
tests for your code. You can pick whatever testing approach
you think is more appropriate for this. Include your test code in
the `myapp_test/` directory, and provide us instructions on how to 
run it in the `myapp_test/README` file.


## Turning in the exercise

To turn in this exercise, please package this directory in a .zip or tar.gz,
and send us the entire package. If your implementation requires additional
software packages to be installed, add the necessary installation steps
to the `bootstrap.sh` file, preferably using `apt-get` or `pip install`.
The goal is for us to be able to get your solution up and running by simply
following the instructions in the getting started section above.


 

