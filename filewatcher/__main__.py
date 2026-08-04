import argparse
import datetime
import logging
import os
import sys

from filewatcher.action.Start import Start
from filewatcher.action.Add import Add
from filewatcher.action.Modify import Modify
from filewatcher.action.Delete import Delete
from filewatcher.action.List import List
from filewatcher.action.Stop import Stop
from filewatcher.action.Status import Status
from filewatcher.action.Log import Log
from filewatcher.config.Config import Config
from filewatcher import __version__


def build_parser(config):
    parser = argparse.ArgumentParser(prog='filewatcher', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--version', action='version', version='FileWatcher {} (Ibrar ARIF)'.format(__version__))

    subparsers = parser.add_subparsers(description='List of all actions', dest='action')

    start_parser = subparsers.add_parser('start', description='Start of filewatcher')
    start_parser.add_argument('--force', default=False, action='store_true', help='Force restart of filewatcher if already started')
    start_parser.add_argument('-worker', default=config['args']['default']['worker'], type=int, action='store', help='Number of workers for FileWatcher (default : %(default)s )')

    list_parser = subparsers.add_parser('list', description='List all paths in filewatcher')
    list_parser.add_argument('-path', nargs='*', help='Path search, multiple choose possible, Example : -path /bin /var/log...')

    add_parser = subparsers.add_parser('add', description='Add path to filewatcher')
    add_parser.add_argument('path', action='store', help='Path system to watch')
    add_parser.add_argument('command', action='store', help='Command to launch when file found')
    add_parser.add_argument('-regex', nargs='?', help="Regex the file must match for filewatcher (default : '%(default)s' )", dest='file_pattern', default=config['args']['default']['regex'], type=str, action='store')
    add_parser.add_argument('-minsize', nargs='?', help='Minimum size of file [B,KB,MB,GB,TB] | example : 10.3MB (default : %(default)s )', dest='min_size', type=str, default=config['args']['default']['minsize'], action='store')
    add_parser.add_argument('-timewait', nargs='?', help='Time to wait before launching the command in HH:MM:SS | example : 00:23:00 for 23 minutes (default : %(default)s )', dest='timewait', type=str, default=config['args']['default']['timewait'], action='store')

    modify_parser = subparsers.add_parser('modify', description='Modify path in filewatcher')
    modify_parser.add_argument('path', action='store', help='Path system watched by filewatcher')
    modify_parser.add_argument('-regex', nargs='?', help='Regex the file must match for filewatcher', dest='file_pattern', default=None, type=str, action='store')
    modify_parser.add_argument('-minsize', nargs='?', help='Minimum size of file [B,KB,MB,GB,TB] | example : 10.3MB', dest='min_size', type=str, default=None, action='store')
    modify_parser.add_argument('-command', nargs='?', help='Command to launch when file found', dest='command', type=str, default=None, action='store')
    modify_parser.add_argument('-timewait', nargs='?', help='Time to wait before launching the command in HH:MM:SS | example : 00:23:00 for 23 minutes', dest='timewait', type=str, default=None, action='store')

    delete_parser = subparsers.add_parser('delete', description='Delete path from filewatcher')
    delete_parser.add_argument('path', action='store', help='Path to delete')

    log_parser = subparsers.add_parser('log', description='Displays the log as a continuous stream')
    log_parser.add_argument('-date', nargs='?', action='store', help='Date of log to display (format : YYYY-MM-DD)', default=None, type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'))
    log_parser.add_argument('--all', default=False, action='store_true', help='Displays all the log since the beginning of the day.')

    subparsers.add_parser('status', description='Allows you to see the status of the filewatcher (started or not)', add_help=False)
    subparsers.add_parser('stop', description='Stop the filewatcher if it is launched', add_help=False)

    return parser


def main():
    config = Config().get_config()

    logFormatter = logging.Formatter(config['logs']['logMessage'], config['logs']['logFormat'])
    rootLogger = logging.getLogger()
    level = logging.getLevelName(config['logs']['logLevel'])
    rootLogger.setLevel(level)

    pidfile = os.path.join(config['pid']['path'], config['pid']['defaultFile'])
    logfile = os.path.join(config['logs']['path'], config['logs']['defaultFile'])

    parser = build_parser(config)

    if len(sys.argv) == 1:
        print(parser.format_help())
        subparsers_actions = [
            action for action in parser._actions
            if isinstance(action, argparse._SubParsersAction)]
        for subparsers_action in subparsers_actions:
            for choice, subparser in subparsers_action.choices.items():
                print("------------------------------------------------------------------------------\n")
                print(subparser.format_help())
        sys.exit(10)

    args = parser.parse_args()

    # Log to console for every action except the daemon start
    if args.action != 'start':
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)

    if args.action == 'start':
        Start(args, pidfile)
    elif args.action == 'add':
        Add(
            path_watch=args.path,
            file_pattern=args.file_pattern,
            min_size=args.min_size,
            command=args.command,
            timewait=args.timewait
        )
    elif args.action == 'modify':
        Modify(
            path_watch=args.path,
            file_pattern=args.file_pattern,
            min_size=args.min_size,
            command=args.command,
            timewait=args.timewait
        )
    elif args.action == 'delete':
        Delete(path_watch=args.path)
    elif args.action == 'list':
        List(list_path_watch=args.path)
    elif args.action == 'stop':
        Stop(pidfile)
    elif args.action == 'log':
        Log(args, logfile)
    elif args.action == 'status':
        Status(pidfile)


if __name__ == '__main__':
    main()
