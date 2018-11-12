from flask import logging

from geulgil.factory import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8088)


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
