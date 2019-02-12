from flask import (
             redirect, request, Blueprint, session, abort, g, flash, render_template, url_for
        )

from stackapi import StackAPI
import pprint
import time

api_bp = Blueprint(__name__, 'api', url_prefix='/api')

@api_bp.route('/query', methods=('GET', 'POST'))
def api_query():
    SITE = StackAPI('stackoverflow')
    SITE.max_pages=200
    questions = SITE.fetch('questions/no-answers', 
                            order='desc', 
                            fromdate=int(time.time()) - 3600*72, 
                            sort='creation', 
                            tagged='google-cloud-platform')
    question_table = [dict( 
                        title='TITLE',
                        date='DATE',
                        tags='TAGS',
                        views='PAGE VIEWS',
                        link='LINK'
                     )]
    print(question_table)
    for question in questions['items']:
        current = dict(title=question['title'], 
                       date=time.strftime('%m-%d %H:%M', time.localtime(question['creation_date'])), 
                       tags= ', '.join(str(e) for e in question['tags'] if e != 'google-cloud-platform'),
                       views=str(question['view_count']),
                       link=question['link']
                       )
        question_table.append(current)

    return render_template('query.html', questions=question_table)


@api_bp.before_app_request
def get_loaded_user():
    user_id = session.get('user_id')
    if not user_id:
        g.user=None
    else:
        g.user=user_id
