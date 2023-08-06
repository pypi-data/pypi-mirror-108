from argparse import ArgumentParser
from . import __version__
from .main import main
import logging

from os import environ

def cli():
    parser = ArgumentParser(prog="tranquilizer",
                            description="Put your functions to REST")
    parser.add_argument('filename', help='Script file with tranquilized functions')
    parser.add_argument('--name', help='Name of the REST API to use in Swagger')
    parser.add_argument('--max_content_length', type=int,
                        help='Maximum size of request in bytes for all endpoints')

    parser.add_argument('--port', '--anaconda-project-port', action='store', default=8086, type=int,
                        help='Port to listen on')
    parser.add_argument('--address', '--anaconda-project-address',
                        action='store',
                        default='0.0.0.0',
                        help='IP address the application should listen on.')
    parser.add_argument('--prefix','--anaconda-project-url-prefix', action='store', default='',
                        help='Prefix in front of urls')
    parser.add_argument('--allow-origin', action='append', type=str,
                        metavar = 'HOST[:PORT]',
                        help='Public hostnames which may connect to the endpoints')

    parser.add_argument('--debug', action='store_true', default=False,
                        help='Run API with debug output.')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {version}'.format(version=__version__))

    # these anaconda-project arguments are ignored by Tranquilizer
    parser.add_argument('--anaconda-project-host', action='append', default=[],
                        help='Hostname to allow in requests')
    parser.add_argument('--anaconda-project-iframe-hosts',
                        action='append',
                        help='Space-separated hosts which can embed us in an iframe per our Content-Security-Policy')
    parser.add_argument('--anaconda-project-no-browser', action='store_true',
                        default=False,
                        help='Disable opening in a browser')
    parser.add_argument('--anaconda-project-use-xheaders',
                        action='store_true',
                        default=False,
                        help='Trust X-headers from reverse proxy')

    return parser


def run():
    args = cli().parse_args()
    app = main(args.filename, args.prefix, args.name, args.max_content_length, args.allow_origin)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

        if args.allow_origin or environ.get('TRANQUILIZER_ALLOW_ORIGIN'):
            logging.getLogger('flask_cors').level = logging.DEBUG

    app.run(host=args.address, port=args.port,
            debug=args.debug)