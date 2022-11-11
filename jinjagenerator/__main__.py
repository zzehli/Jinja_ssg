"""Build static HTML site from directory of HTML templates and plain files."""
import shutil
import click
from pathlib import Path
import json
from jinja2 import Environment, \
    FileSystemLoader, TemplateError, select_autoescape


# accept arguments and options
@click.command()
@click.argument('directory')
@click.option('-o', '--output', help='Output directory.', type = click.Path())
@click.option('-v', '--verbose', is_flag = True, help='Print more output.')
def main(directory, output, verbose):
    """Static Site Generator for Jinja templates"""

    # turn input directory into a path
    q = Path(directory)
    
    # check if the directory exist

    if not q.exists():
        raise click.ClickException('\'' + directory + '\' is not a directory')

    # create new folder, exit if already exist
    if output is not None:
        outputFolder = Path(output)
    else:
        outputFolder = q/'html'
    if outputFolder.exists():
        raise click.ClickException("output directory already exists.")
    outputFolder.mkdir()

    # read corresponding templated file
    jsonConfig = q/'config.json'
    tempFolder = q/'templates'
    staticFolder = q/'static'

    # if static exists, copy over
    if staticFolder.exists():
        shutil.copytree(staticFolder, outputFolder, dirs_exist_ok=True)
        if verbose:
            click.echo('Copied ' + str(staticFolder) + ' -> ' + 
                        str(outputFolder))

    context = {}
    templateFile = ""
    url = ""
    try:
        with jsonConfig.open() as f:
            jData = json.load(f)
            for page in jData:
                context = page['context']
                templateFile = page['template']
                url = page['url']

                # render with jinja
                try:
                    jinjaEnv = Environment(
                    loader =  FileSystemLoader(tempFolder),
                    autoescape = select_autoescape(['html', 'xml']),
                    )

                    template = jinjaEnv.get_template(templateFile)

                    url = url.lstrip("/")
                    
                    # render output files
                    file_dir = outputFolder/url
                    if not file_dir.exists():
                        file_dir.mkdir(parents = True)
                    p = file_dir/"index.html"
                    p.write_text(template.render(context))
                    if verbose:
                        click.echo('Rendered ' + str(templateFile) + ' -> ' + str(p))
                
                except TemplateError as e:
                    click.ClickException(e.message)
            
    except json.JSONDecodeError as e:
        click.ClickException(e.msg)
    
    

    
if __name__ == "__main__":
    main()