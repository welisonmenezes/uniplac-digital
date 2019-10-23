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

    results_per_genre = db.engine.execute('SELECT COUNT(id) FROM post WHERE created_at >= "' + str(last_month) + '" GROUP BY genre ORDER BY genre ASC')
    posts_per_genre = [row[0] for row in results_per_genre]

    results_per_status = db.engine.execute('SELECT COUNT(id) FROM post WHERE created_at >= "' + str(last_month) + '" GROUP BY status ORDER BY status ASC')
    posts_per_status = [row[0] for row in results_per_status]

    
    titulo = 'Dashboard'
    return render_template('dashboard/index.html',titulo=titulo, configuration=configuration, posts_per_genre=posts_per_genre, posts_per_status=posts_per_status), 200

