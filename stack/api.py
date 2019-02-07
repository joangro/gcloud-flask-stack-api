from flask import (
             redirect, request, Blueprint, session, abort, g, flash, render_template, url_for
        )

from stackapi import StackAPI

api_bp = Blueprint(__name__, 'api', url_prefix='/api')

@api_bp.route('/<token>/query', methods=('GET', 'POST'))
def api_query(token):
    if request.method=='GET':
        
        return token
