from invoke import task


@task
def build(ctx):
    ctx.run('./manage.py makemigrations')
    ctx.run('./manage.py migrate')


@task
def requirements(ctx):
    ctx.run("pip freeze | sed 's/@[a-z0-9]\+//' > requirements.txt")


@task
def deploy(ctx):
    ctx.run("git pull origin master")
    ctx.run("pip install -r requirements.txt")
    ctx.run('./manage.py migrate')
    ctx.run('./manage.py collectstatic --no-input')
    ctx.run("sudo supervisorctl restart api-thefarma")
    ctx.run("sudo supervisorctl restart api-thefarma-websocket")
    ctx.run("sudo supervisorctl restart api-thefarma-celery:")
