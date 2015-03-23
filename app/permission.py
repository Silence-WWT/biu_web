from flask.ext.principal import RoleNeed, Permission, identity_loaded, Denial

admin_permission = Permission(RoleNeed('admin'))


def config_identity(app):
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        if identity.id and identity.id.startswith('a'):
            identity.provides.add(RoleNeed('admin'))