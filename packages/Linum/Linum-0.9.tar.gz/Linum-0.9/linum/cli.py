import click

from linum import SvgRenderer
from linum.excel_renderer.excel_renderer import ExcelRenderer
from linum.txt_renderer.console_renderer import ConsoleRenderer
from linum.txt_renderer.txt_renderer import TxtRenderer


@click.command()
@click.argument('tasks_path', type=click.Path(exists=True))
@click.option('-o', '--out', type=click.Path(writable=True),
              help='Output file. If not specified then linum creates new file in current directory.')
@click.option('-r', '--renderer', default='CONSOLE', type=click.Choice(['CONSOLE', 'TXT', 'XLSX', 'SVG'], ),
              help="Renderer to use. "
                   "'CONSOLE' - for console printing. "
                   "'TXT' - for rendering txt file. "
                   "'XLSX' - for rendering xlsx file. "
                   "'SVG' - for rendering svg file. "
                   "Default is 'CONSOLE'.")
@click.option('-c', '--context', type=click.Path(exists=True),
              help="Context for renderer. It is YAML file with render settings. "
                   "If not specified then default settings will be applied.")
def cli(tasks_path, out, renderer, context):
    """ Command line interface for linum. """

    if renderer == 'CONSOLE':
        renderer = ConsoleRenderer(tasks_path, context)
    elif renderer == 'TXT':
        renderer = TxtRenderer(tasks_path, context, out)
    elif renderer == 'XLSX':
        renderer = ExcelRenderer(tasks_path, context, out)
    elif renderer == 'SVG':
        renderer = SvgRenderer(tasks_path, context, out)
    renderer.render()


if __name__ == '__main__':
    cli()
