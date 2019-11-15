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

    results_per_genre = db.engine.execute('SELECT COUNT(id), genre FROM post WHERE created_at >= "' + str(last_month) + '" GROUP BY genre ORDER BY genre ASC')
    pg_arr = [(row[0], row[1]) for row in results_per_genre]
    per_genre = [0, 0, 0]
    for pg in pg_arr:
        if pg[1] == 'ad':
            per_genre[0] = pg[0]
        elif pg[1] == 'news':
            per_genre[1] = pg[0]
        elif pg[1] == 'notice':
            per_genre[2] = pg[0]

    results_per_status = db.engine.execute('SELECT COUNT(id), status FROM post WHERE created_at >= "' + str(last_month) + '" GROUP BY status ORDER BY status ASC')
    ps_arr = [(row[0], row[1]) for row in results_per_status]
    per_status = [0, 0, 0]
    for pg in ps_arr:
        if pg[1] == 'approved':
            per_status[0] = pg[0]
        elif pg[1] == 'denied':
            per_status[1] = pg[0]
        elif pg[1] == 'pending':
            per_status[2] = pg[0]
    
    titulo = 'Dashboard'
    return render_template('dashboard/index.html',titulo=titulo, configuration=configuration, posts_per_genre=per_genre, posts_per_status=per_status), 200

