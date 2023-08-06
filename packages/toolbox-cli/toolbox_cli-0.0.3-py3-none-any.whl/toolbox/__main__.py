import sys
import click
import platform
from colorama import init,Fore, Back, Style
import os
from getkey import getkey
import socket

@click.group()
@click.version_option("0.0.1")
def cli():
    """A Toolbox runs in Command Line"""
    pass

@cli.command()
def system_info():
    """Get System Information"""
    uname = platform.uname()
    click.echo(Fore.BLUE + "=========System Information=========")
    click.echo(Style.RESET_ALL)
    click.echo(f"System: {uname.system}")
    click.echo(f"Node Name: {uname.node}")
    click.echo(f"Release: {uname.release}")
    click.echo(f"Version: {uname.version}")
    click.echo(f"Machine: {uname.machine}")
    click.echo(f"Processor: {uname.processor}")

@cli.command()
def qrcode():
    """Generate QR code"""
    click.echo(Fore.BLUE + "=========Generate QR code=========\n Press Q to quit")
    click.echo(Style.RESET_ALL)
    try:
        import qrcode
    except ImportError:
        click.echo("Downloading QR Code generator from https://pypi.org/project/qrcode ...")
        os.system("pip install qrcode")
    
    text_input_qr_code = input("Please enter some text here: ")
    img = qrcode.make(text_input_qr_code)
    img.show()

@cli.command()
def get_ip():
    """Get Your IP Address"""
    click.echo(Fore.BLUE + "=========Get Your IP Address=========")
    click.echo(Style.RESET_ALL)
    click.echo(Fore.YELLOW + "Your IP Address is: " + socket.gethostbyname(socket.gethostname()))
    click.echo(Style.RESET_ALL)



@cli.command()
def list():
    """Tools you can use in this toolbox"""
    click.echo(Fore.YELLOW + "Get System Info          Usage: system-info \n")
    click.echo(Fore.BLUE + "*Generate QR code          Usage: qrcode \n")




if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("Toolbox")
    cli()