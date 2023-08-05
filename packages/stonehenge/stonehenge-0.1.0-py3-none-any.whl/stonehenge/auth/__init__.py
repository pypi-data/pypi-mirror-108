from stonehenge.modules import Module
from stonehenge.auth.models import User


class AuthModule(Module):
    models = [
        User,
    ]
