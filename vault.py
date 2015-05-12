
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
sftp=''



# Classes


# Functions

def sftp_connect():
    """ create an sftp connection to vault"""
    global sftp
    sftp = pysftp.Connection(hostname, 
                                username=username, 
                                private_key=key)
    sftp.chdir(vaultdir)

def mtime_key(file):
    return file.st_mtime


@click.group()
def vault():
    """tool to extract files from a secure sftp data vault"""
    
    global hostname
    global username
    global key
    global vaultdir
    global outputdir

    # load config file 
    if os.path.exists(os.getcwd() + '/vault.ini'):
        config = ConfigParser.ConfigParser()
        config.read(os.getcwd() + '/vault.ini')
        hostname = config.get('vault', 'hostname')
        username = config.get('vault', 'username')
        key = config.get('vault', 'key')
        vaultdir = config.get('vault', 'vaultdir')
        outputdir = config.get('vault', 'outputdir')
        sftp_connect()


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
    if files == 'all':
        for file in sftp.listdir():
            click.echo(file)
    elif files == 'latest':
        vault_files = sorted(sftp.listdir_attr(), key=mtime_key, reverse=True)
        click.echo(vault_files[0].filename)


@vault.command()
@click.argument('files', nargs=1)
def extract(files):
    """ extract vault file(s) """
    click.echo('extract vault file(s)')
    if files == 'latest':
        vault_files = sorted(sftp.listdir_attr(), key=mtime_key, reverse=True)
        latest = vault_files[0].filename
        outputfile=os.path.realpath(outputdir) + '/' + latest 
        sftp.get(latest, localpath=outputfile, preserve_mtime=True)
        if zipfile.is_zipfile(outputfile):
            zip = zipfile.ZipFile(outputfile)
            zip.extractall(os.path.realpath(outputdir))
            os.remove(outputfile)


if __name__ == '__main__':
    vault()

