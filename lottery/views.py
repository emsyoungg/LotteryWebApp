# IMPORTS
from flask import Blueprint, render_template, flash, redirect, url_for
from sqlalchemy.orm import make_transient
from app import db, requires_roles
from lottery.forms import DrawForm
from models import Draw
from flask_login import login_required, current_user

# CONFIG
lottery_blueprint = Blueprint('lottery', __name__, template_folder='templates')


# VIEWS
# view lottery page
@lottery_blueprint.route('/lottery')
@login_required
@requires_roles('user')
def lottery():
    return render_template('lottery/lottery.html', name=current_user.firstname)


# view all draws that have not been played
@lottery_blueprint.route('/create_draw', methods=['POST'])
@login_required
@requires_roles('user')
def create_draw():
    form = DrawForm()
    # validate forms draw numbers
    if form.is_submitted() and form.validate():
        numbers = [form.number1.data, form.number2.data, form.number3.data, form.number4.data, form.number5.data,
                   form.number6.data]
        # save numbers in ascending order
        numbers.sort()
        submitted_numbers = ' '.join(str(n) for n in numbers)
        # create a new draw with the form data.
        new_draw = Draw(user_id=current_user.id, numbers=submitted_numbers, master_draw=False, lottery_round=0,
                        public_key=current_user.public_key)
        # add the new draw to the database
        db.session.add(new_draw)
        db.session.commit()

        # re-render lottery.page
        flash('Draw %s submitted.' % submitted_numbers)
        return redirect(url_for('lottery.lottery'))
    return render_template('lottery/lottery.html', name=current_user.firstname, form=form)


# view all draws that have not been played
@lottery_blueprint.route('/view_draws', methods=['POST'])
@login_required
@requires_roles('user')
def view_draws():
    # get all draws that have not been played [played=0]
    playable_draws = Draw.query.filter_by(been_played=False, user_id=current_user.id).all()

    # if playable draws exist
    if len(playable_draws) != 0:
        for draw in playable_draws:
            make_transient(draw)
            # symmetric encryption would be: draw.view_draw(current_user.draw_key)
            # asymmetric:
            draw.view_draw(current_user.private_key)
        # re-render lottery page with playable draws
        return render_template('lottery/lottery.html', playable_draws=playable_draws)
    else:
        flash('No playable draws.')
        return lottery()


# view lottery results
@lottery_blueprint.route('/check_draws', methods=['POST'])
@login_required
@requires_roles('user')
def check_draws():
    # get played draws
    played_draws = Draw.query.filter_by(been_played=True, user_id=current_user.id).all()

    # if played draws exist
    if len(played_draws) != 0:
        return render_template('lottery/lottery.html', results=played_draws, played=True)

    # if no played draws exist [all draw entries have been played therefore wait for next lottery round]
    else:
        flash("Next round of lottery yet to play. Check you have playable draws.")
        return lottery()


# delete all played draws
@lottery_blueprint.route('/play_again', methods=['POST'])
@login_required
@requires_roles('user')
def play_again():
    # deletes only current users draws
    Draw.query.filter_by(been_played=True, master_draw=False, user_id=current_user.id).delete(synchronize_session=False)
    db.session.commit()

    flash("All played draws deleted.")
    return lottery()
