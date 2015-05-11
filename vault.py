
# libs
import sys
import click
import ConfigParser
import pysftp
import zipfile
import os.path

# global variables
hostname=''
username=''
key=''
vaultdir=''
outputdir=''




# Classes


# Functions






@click.group()
@click.option('--config', '-c', multiple=True, nargs=1, help='config file')
@click.option('--host', '-h', multiple=True, nargs=1, help='vault hostname/ip address')
@click.option('--user', '-u', multiple=True, nargs=1, help='vault username')
@click.option('--key', '-k', multiple=True, help='vault private key')
@click.option('--vaultdir', '-v', multiple=True, nargs=1, default='vault', help='vault directory')
@click.option('--outputdir', '-o', multiple=True, nargs=1, default='.', help='output directory')
def vault(config, host, user, key, vaultdir, outputdir):
    """tool to extract files from a secure sftp data vault"""
    
    # load config file 
    
    # vaultconfig = load_config()


    # (3) program


@vault.command()
def init():
    """ initialise the config file"""

    hostname = click.prompt('Vault hostname [None]: ', default='')
    username = click.prompt('Vault username [None]: ', default='')
    key = click.prompt('Vault key [None]: ', default='')
    vaultdir = click.prompt('Vault directory [vault]: ', default='vault')
    outputdir = click.prompt('Output directory [.]: ', default='.')

    config = ConfigParser.ConfigParser()
    cfgfile = open("./vault.ini",'w')
    config.add_section('vault')
    config.set('vault', 'hostname', hostname)
    config.set('vault', 'username', username)
    config.set('vault', 'key', key)
    config.set('vault', 'vaultdir', vaultdir)
    config.set('vault', 'outputdir', outputdir)
    config.write(cfgfile)
    cfgfile.close()



@vault.command()
@click.argument('files', nargs=1)
def list(files): 
    """ list vault files """
    click.echo('list vault files')


@vault.command()
@click.argument('files', nargs=1)
def extract(files):
    """ extract vault file(s) """
    click.echo('extract vault file(s)')








if __name__ == '__main__':
    vault()

