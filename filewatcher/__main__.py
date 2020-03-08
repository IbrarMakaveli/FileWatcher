import argparse
import sys, os, datetime
from action.Lancer import Lancer
from action.Ajouter import Ajouter
from action.Modifier import Modifier
from action.Supprimer import Supprimer
from action.Lister import Lister
from action.Stop import Stop
from action.Statut import Statut
from action.Log import Log
from config.Config import Config
import logging
import time
import subprocess

if __name__ == '__main__':

    config = Config().get_config()

    logFormatter = logging.Formatter(config['logs']['logMessage'],config['logs']['logFormat'])
    rootLogger = logging.getLogger()
    level = logging.getLevelName(config['logs']['logLevel'])
    rootLogger.setLevel(level)

    pidfile = os.path.join(config['pid']['path'], config['pid']['defaultFile'])
    logfile = os.path.join(config['logs']['path'], config['logs']['defaultFile'])
    
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--version', action='version', version='FileWatcher (Ibrar ARIF)')

    subparsers = parser.add_subparsers(description='Liste of all actions',dest='action')
    
    lancer_parser = subparsers.add_parser('start', description='Start of filewatcher')
    lancer_parser.add_argument('--force', default=False, action='store_true',help='Force restart of filewatcher if already start')
    lancer_parser.add_argument('-worker', default=config['args']['default']['worker'], action='store',help='Number of worker for Filewatcher (default : %(default)s )')
    
    list_parser = subparsers.add_parser('list', description='Liste all path in filewatcher')
    list_parser.add_argument('-path', nargs='*', help='Path search, multiple choose possible, Example : -path /bin /var/log...')

    add_parser = subparsers.add_parser('add', description='Add path to filewatcher')
    add_parser.add_argument('path', action='store', help='Path systeme to watch')
    add_parser.add_argument('command', action='store', help='Commande to launch when file found')
    add_parser.add_argument('-regex', nargs='?', help="Regex of the file must match for filewatcher (default : '%(default)s' )", dest='file_pattern', default=config['args']['default']['regex'], type=str, action="store")
    add_parser.add_argument('-minsize', nargs='?', help='Size minimum of file [B,KB,MB,GB,TB] | example : 10.3MB (default : %(default)s )', dest='min_size', type=str, default=config['args']['default']['minsize'], action="store")
    add_parser.add_argument('-timewait', nargs='?', help='Time to wait before launching the command in HH:MM:SS | par exemple : 00:23:00 for 23 minutes (default : %(default)s )', dest='timewait', type=str, default=config['args']['default']['timewait'], action="store")

    modify_parser = subparsers.add_parser('modify', description='Modify path to filewatcher')
    modify_parser.add_argument('path', action='store', help='Path systeme ou va regarder le filewatcher')
    modify_parser.add_argument('-regex', nargs='?', help='Regex of the file must match for filewatcher', dest='file_pattern', default=None, type=str, action="store")
    modify_parser.add_argument('-minsize', nargs='?', help='Size minimum of file [B,KB,MB,GB,TB] | example : 10.3MB', dest='min_size', type=str, default=None, action="store")
    modify_parser.add_argument('-command', nargs='?', help='Commande to launch when file found', dest='command', type=str, default=None, action="store")
    modify_parser.add_argument('-timewait', nargs='?', help='Time to wait before launching the command in HH:MM:SS | par exemple : 00:23:00 for 23 minutes', dest='timewait', type=str, default=None, action="store")

    delete = subparsers.add_parser('delete', description='Delete path to filewatcher')
    delete.add_argument('path', action='store', help='Path to delete')
    
    log_paser = subparsers.add_parser('log', description='Displays the log as a continuous thread')
    log_paser.add_argument('-date', nargs='?', action='store', help='Date of log to display (format : YYYY-MM-DD)', default=None, type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'))
    log_paser.add_argument('--all', default=False, action='store_true', help='Displays all the log since the beginning of the day.')

    status_paser = subparsers.add_parser('status', description="Allows you to see the status of the filewatcher (start or not)", add_help=False)

    stop_paser = subparsers.add_parser('stop', description='Stop the filewatcher if is launch' , add_help=False)
    
    if len(sys.argv)==1:
        print(parser.format_help())
        subparsers_actions = [
            action for action in parser._actions 
            if isinstance(action, argparse._SubParsersAction)]
        for subparsers_action in subparsers_actions:
            for choice, subparser in subparsers_action.choices.items():
                print("------------------------------------------------------------------------------\n")
                print(subparser.format_help())
        exit(10)

    args = parser.parse_args()
    
    #Log console if is not start
    if args.action!='start':
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)

    if args.action=='start':
        Lancer(args,pidfile)
    elif args.action=='add':
        Ajouter(
            path_watch=args.path,
            file_pattern=args.file_pattern,
            min_size=args.min_size,
            command=args.command,
            timewait=args.timewait
        )
    elif args.action=='modify':
         Modifier(
            path_watch=args.path,
            file_pattern=args.file_pattern,
            min_size=args.min_size,
            command=args.command,
            timewait=args.timewait
        )
    elif args.action=='delete':
        Supprimer(path_watch=args.path)
    elif args.action=='list':
        Lister(list_path_watch=args.path)
    elif args.action=='stop':
        Stop(pidfile)
    elif args.action=='log':
        Log(args,logfile)
    elif args.action=='status':
        Statut(pidfile)