import os
from flask import current_app, Blueprint, render_template, request, url_for, redirect
from sqlalchemy import desc, and_, or_, asc, func
from datetime import date, timedelta
from database.Model import db, Configuration, Post


dashboardBP = Blueprint('dashboard', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')

@dashboardBP.route('/')
def index():
    return redirect(url_for('dashboard.dash'))

@dashboardBP.route('/dashboard')
def dash():
    today = date.today()
    last_month = today - timedelta(days=30)

    configuration = Configuration.query.first()

    # filter = (Post.created_at >= last_month, )
    # countx = func.count(Post.id).label('total')
    # posts = Post.query.filter(*filter).group_by(countx.desc())
    results_per_genre = db.engine.execute('select count(id) from post where created_at >= "' + str(last_month) + '" group by genre')
    posts_per_genre = [row[0] for row in results_per_genre]
    print(posts_per_genre)

    results_per_status = db.engine.execute('select count(id) from post where created_at >= "' + str(last_month) + '" group by status')
    posts_per_status = [row[0] for row in results_per_status]
    print(posts_per_status)
    
    titulo = 'Dashboard'
    return render_template('dashboard/index.html',titulo=titulo, configuration=configuration), 200

