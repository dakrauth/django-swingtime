import os
from invoke import task

PYWARN='python -Wd'

@task
def clean(ctx):
    '''Remove build artifacts'''
    ctx.run('rm -rf .cache build django_swingtime.egg-info .coverage docs/html')

@task
def install(ctx):
    '''Install base requirements'''
    ctx.run('pip install -U pip', pty=True)
    ctx.run('pip install -r requirements/base.txt', pty=True)
    ctx.run('pip install -e .', pty=True)

@task
def dev(ctx):
    '''Install development requirements'''
    install(ctx)
    ctx.run('pip install -r requirements/dev.txt', pty=True)

@task
def test(ctx):
    '''Run tests and coverage'''
    ctx.run(
        "py.test --cov-config .coveragerc --cov-report html --cov-report term --cov=swingtime",
        pty=True
    )

@task
def cov(ctx):
    '''Open the coverage reports'''
    if os.path.exists('build/coverage/index.html'):
        ctx.run('open build/coverage/index.html', pty=True)

@task
def docs(ctx):
    '''Build the documentation'''
    ctx.run('cd docs && make html', pty=True)


@task
def demo(ctx, warn=False):
    '''Set up the demo environment and run the server'''
    manage = '{} manage.py {{}}'.format(PYWARN if warn else 'python')
    if os.path.dirname(__file__) == os.getcwd():
        os.chdir('demo')
    ctx.run(manage.format('check'), pty=True)
    ctx.run(manage.format('loaddemo'), pty=True)
    ctx.run(manage.format('runserver'), pty=True)
