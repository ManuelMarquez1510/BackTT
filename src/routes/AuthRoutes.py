from flask import Blueprint

main = Blueprint('auth_blueprint',__name__)

@main.route('/')
def route_main():
    return "auth"
