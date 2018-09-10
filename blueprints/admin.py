from flask import Blueprint, render_template, current_app, redirect, g, request, url_for

from database.objects import Player, Group
from helpers.functions import render_with_session

bp = Blueprint('admin', __name__, url_prefix='/admin')


def redirect_url(default='home'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


@bp.before_request
def check_admin():
    if g.user is None or not g.admin:
        return redirect('/')


@bp.route('/')
def home():
    s = current_app.config['db']()
    players = s.query(Player).all()
    groups = s.query(Group).all()
    id_to_groups = {g.id: g.name for g in groups}
    return render_with_session('admin.html', s, players=players, groups=groups, id_to_groups=id_to_groups)


@bp.route('/addrole/<id>/<role>')
def addrole(id, role):
    s = current_app.config['db']()
    role_id = s.query(Group).filter(Group.name == role).first().id
    print(role, role_id)
    player = s.query(Player).filter(Player.platformid == id).first()
    if player is None:
        p = Player(platformid=id, platformname='', avatar='', ranks='', groups=[role_id])
        s.add(p)
    else:
        if role_id not in player.groups:
            player.groups = player.groups + [role_id]
    s.commit()
    return redirect(redirect_url())


@bp.route('/delrole/<id>/<role>')
def delrole(id, role):
    s = current_app.config['db']()
    role_id = s.query(Group).filter(Group.name == role).first().id
    player = s.query(Player).filter(Player.platformid == id).first()
    if player is None:
        # don't do anything because we don't exist
        pass
    else:
        if role_id in player.groups:
            grps = player.groups.copy()
            grps.remove(role_id)
            player.groups = grps # we need it to detect that we changed something
    s.commit()
    return redirect(redirect_url())