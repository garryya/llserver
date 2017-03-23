Implement a few methods of a hypothetical API server called "myapp".
This API server's main task is to authenticate users and then serve them analysis reports of
the execution of a (malicious) file in the Lastline analysis sandbox.

This distribution includes a simple skeleton of the API server, implemented in flask, as well as
a vagrant configuration that can be used to quickly get up and running with this code in a virtual
machine.


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



