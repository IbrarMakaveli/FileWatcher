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
    parser.add_argument('--version', action='version', version='FileWatcher release v1.0 (Ibrar ARIF)')

    subparsers = parser.add_subparsers(description='Liste des actions possibles',dest='action')
    
    lancer_parser = subparsers.add_parser('lancer', description='Lance le filewatcher')
    lancer_parser.add_argument('--force', default=False, action='store_true',help='Force la relance du filewatcher si deja actif')
    lancer_parser.add_argument('-worker', default=config['args']['default']['worker'], action='store',help='Nombre de worker simultane (default : %(default)s )')
    
    lister_parser = subparsers.add_parser('lister', description='Liste toutes les chemin sur le filewatcher')
    lister_parser.add_argument('-chemin', nargs='*', help='Chemin rechercher multiple choix possible, Exemple : -chemin /varsoft /parc/ott...')

    ajout_parser = subparsers.add_parser('ajouter', description='Ajout d\'un chemin au filewatcher')
    ajout_parser.add_argument('chemin', action='store', help='Chemin systeme ou va regarder le filewatcher')
    ajout_parser.add_argument('command', action='store', help='Commande a lancer')
    ajout_parser.add_argument('-regex', nargs='?', help="Regex donc le fichier doit correspondre pour le filewatcher (default : '%(default)s' )", dest='file_pattern', default=config['args']['default']['regex'], type=str, action="store")
    ajout_parser.add_argument('-minsize', nargs='?', help='Taille minimum en size en [B,KB,MB,GB,TB] | par exemple : 10.3MB (default : %(default)s )', dest='min_size', type=str, default=config['args']['default']['minsize'], action="store")
    ajout_parser.add_argument('-timewait', nargs='?', help='Temps a attendre avant de lancer la command en HH:MM:SS | par exemple : 00:23:00 pour 23 minutes (default : %(default)s )', dest='timewait', type=str, default=config['args']['default']['timewait'], action="store")

    modifier_parser = subparsers.add_parser('modifier', description='Modifier un chemin au filewatcher')
    modifier_parser.add_argument('chemin', action='store', help='Chemin systeme ou va regarder le filewatcher')
    modifier_parser.add_argument('-regex', nargs='?', help='Regex donc le fichier doit correspondre pour le filewatcher', dest='file_pattern', default=None, type=str, action="store")
    modifier_parser.add_argument('-minsize', nargs='?', help='Taille minimum en size en [B,KB,MB,GB,TB], par exemple : 10.3MB', dest='min_size', type=str, default=None, action="store")
    modifier_parser.add_argument('-command', nargs='?', help='Commande a lancer', dest='command', type=str, default=None, action="store")
    modifier_parser.add_argument('-timewait', nargs='?', help='Temps a attendre avant de lancer la command en HH:MM:SS | par exemple : 00:23:00 pour 23 minutes', dest='timewait', type=str, default=None, action="store")

    supprimer_parser = subparsers.add_parser('supprimer', description='Supprimer un chemin au filewatcher')
    supprimer_parser.add_argument('chemin', action='store', help='Chemin a supprimer')
    
    log_paser = subparsers.add_parser('log', description='Affiche la log en fil continue')
    log_paser.add_argument('-date', nargs='?', action='store', help='Date de log a afficher (format : YYYY-MM-DD)', default=None, type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'))
    log_paser.add_argument('--all', default=False, action='store_true', help='Affiche toute la log depuis le debut de la journee')

    statut_paser = subparsers.add_parser('statut', description="Permet de voir l'etat du filewatcher (actif ou non)", add_help=False)

    stop_paser = subparsers.add_parser('stop', description='Stop le filewatcher si lancer' , add_help=False)
    
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
    
    #Log console si pas un lancement
    if args.action!='lancer':
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)

    if args.action=='lancer':
        Lancer(args,pidfile)
    elif args.action=='ajouter':
        Ajouter(
            path_watch=args.chemin,
            file_pattern=args.file_pattern,
            min_size=args.min_size,
            command=args.command,
            timewait=args.timewait
        )
    elif args.action=='modifier':
         Modifier(
            path_watch=args.chemin,
            file_pattern=args.file_pattern,
            min_size=args.min_size,
            command=args.command,
            timewait=args.timewait
        )
    elif args.action=='supprimer':
        Supprimer(path_watch=args.chemin)
    elif args.action=='lister':
        Lister(list_path_watch=args.chemin)
    elif args.action=='stop':
        Stop(pidfile)
    elif args.action=='log':
        Log(args,logfile)
    elif args.action=='statut':
        Statut(pidfile)