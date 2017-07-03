import os
from invoke import task

@task
def clean(ctx):
    ctx.run('rm -rf .cache build django_swingtime.egg-info .coverage')

@task
def install(ctx):
    ctx.run('pip install -U pip', pty=True)
    ctx.run('pip install -r requirements/base.txt', pty=True)
    ctx.run('pip install -e .', pty=True)

@task
def dev(ctx):
    install(ctx)
    ctx.run('pip install -r requirements/dev.txt', pty=True)

@task
def test(ctx):
    ctx.run(
        "py.test --cov-config .coveragerc --cov-report html --cov-report term --cov=swingtime",
        pty=True
    )

@task
def cov(ctx):
    if os.path.exists('build/coverage/index.html'):
        ctx.run('open build/coverage/index.html')
