import click
import sys
import getpass
import pyhectiqlab
from pyhectiqlab.auth import AuthProvider
from pyhectiqlab.artifacts import SharedArtifactsManager
from pyhectiqlab.mlmodels import download_mlmodel as ops_download_mlmodel
from pyhectiqlab.datasets import download_dataset as ops_download_dataset

def get_creds():
	username = input("Username: ")
	password = getpass.getpass(prompt='Password: ', stream=None) 
	return username, password

@click.group()
def cli():
    """Just a group."""
    pass

@cli.command()
def login():
	auth = AuthProvider()
	if auth.is_logged():
		click.echo("User is already logged in.")
		return

	username, password = get_creds()
	click.echo("Connecting...")
	success = auth.login_with_password(username, password)
	if success:
		click.echo("User is authentificated.")
	else:
		click.echo('Unsuccessful login.')

@cli.command()
def logout():
	auth = AuthProvider()
	auth.logout()
	click.echo('Logout completed.')

@cli.command()
def version():
	click.echo(pyhectiqlab.__version__)
	
@cli.command()
def projects():	
	manager = SharedArtifactsManager()
	manager.list_projects()

@cli.command()
@click.option('-p', '--project_id', help='id of the project', required=True)
def artifacts(project_id):
	manager = SharedArtifactsManager()
	manager.select_artifact(project_id)

@cli.command()
@click.option('-p', '--project_id', help='id of the project', required=True)
@click.option('-f', '--filename', help='Name of the shared artifact', required=True)
def post_artifact(project_id, filename):
	manager = SharedArtifactsManager()
	click.echo('Pushing artifacts.')
	manager.push_artifact(filename, project_id)
	click.echo('Artifact pushed')

@cli.command()
@click.option('-p', '--project_id', help='id of the project', required=False)
@click.option('-n', '--name', prompt='MLModel name', help='Name of the mlmodel', required=True)
@click.option('-v', '--version', help='Version of the mlmodel. If not specified, will download the latest release', required=False)
@click.option('-s', '--save_path', prompt='Save path', help='Save path', required=True)
@click.option('-o', '--overwrite', is_flag=True)
def download_mlmodel(project_id, name, version, save_path, overwrite):
	dir_path = ops_download_mlmodel(mlmodel_name=name, 
						project_id=project_id, 
						version=version, 
						save_path=save_path, 
						overwrite=overwrite)
	if dir_path is not None:
		click.echo(f'MLModel saved in {dir_path}')

@cli.command()
@click.option('-p', '--project_id', help='id of the project', required=False)
@click.option('-n', '--name', prompt='Dataset name', help='Name of the dataset', required=True)
@click.option('-v', '--version', help='Version of the dataset. If not specified, will download the latest release', required=False)
@click.option('-s', '--save_path', prompt='Save path', help='Save path', required=True)
@click.option('-o', '--overwrite', is_flag=True)
def download_dataset(project_id, name, version, save_path, overwrite):
	dir_path = ops_download_dataset(dataset_name=name, 
						project_id=project_id, 
						version=version, 
						save_path=save_path, 
						overwrite=overwrite)
	if dir_path is not None:
		click.echo(f'MLModel saved in {dir_path}')
