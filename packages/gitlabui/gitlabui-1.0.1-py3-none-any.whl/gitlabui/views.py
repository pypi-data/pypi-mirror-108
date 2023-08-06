from flask import render_template, request, redirect, url_for

from gitlabui import app, api


@app.route('/')
def index():
    return redirect(url_for('tags'))


@app.route('/tags')
def tags():
    return render_template('index.html', projects=api.get_projects(
        request.args.get('q'),
        opts=request.args
    ))


@app.route('/reset')
def reset():
    api.reset()
    return redirect(url_for('tags'))


@app.route('/refresh_tags')
def refresh_tags():
    api.refresh_tags()
    return redirect(url_for('tags'))


@app.route('/search')
def search():
    if 'search' in request.args and 'filepath' in request.args and 'ref' in request.args:
        return render_template('search.html', results=api.search(
            request.args['search'],
            request.args['filepath'],
            request.args['ref'],
            project_search=request.args.get('q'),
            project_opts=request.args
        ))
    else:
        return render_template('search.html')


@app.route('/version')
def version():
    return api.version()
