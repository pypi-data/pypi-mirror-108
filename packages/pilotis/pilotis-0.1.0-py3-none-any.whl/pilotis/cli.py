import click

from pilotis.commands.aws import infra_command
from pilotis.commands.git import git_command
from pilotis.commands.init import init_command


@click.group(name="pilotis")
def main() -> None:
    click.echo("Thank you for using Pilotis.")


main.add_command(init_command)
main.add_command(git_command)
main.add_command(infra_command)

if __name__ == '__main__':
    main()
