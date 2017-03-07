#!/usr/bin/python
import sys

import myapp


def main(argv):
    app = myapp.create_app()

    # Turn on debug mode, to make your life easier in development
    # http://flask.pocoo.org/docs/0.10/quickstart/#debug-mode
    app.debug = True

    app.run(port=8080,
            host="0.0.0.0")


if __name__ == '__main__':
    main(sys.argv)
