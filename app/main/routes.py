from flask import render_template
from sqlalchemy import desc, select
from app.extensions import db
from app.main import bp
from app.models import WorkExperience

@bp.route('/')
def index():
    get_work_exp_query = select(WorkExperience).order_by(desc(WorkExperience.start_date))
    work_experiences = db.session.scalars(get_work_exp_query).all()
    return render_template(
        'main/index.html',
        work_experiences=work_experiences
    )
