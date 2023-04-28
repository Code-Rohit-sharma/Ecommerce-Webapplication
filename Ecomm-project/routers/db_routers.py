class UsersRouter:

    route_app_labels = {'auth', 'contenttypes','admin','sessions'}

    def db_for_read(self, model, **hints):

        if model._meta.app_label in self.route_app_labels:
            return 'usersapp_db'
        return None

    def db_for_write(self, model, **hints):
        
        if model._meta.app_label in self.route_app_labels:
            return 'usersapp_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        
        if app_label in self.route_app_labels:
            return db == 'usersapp_db'
        return None

class EcommerceRouter:

    route_app_labels = {'Ecommerce'}

    def db_for_read(self, model, **hints):

        if model._meta.app_label in self.route_app_labels:
            return 'ecommerce_db'
        return None

    def db_for_write(self, model, **hints):
        
        if model._meta.app_label in self.route_app_labels:
            return 'ecommerce_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        
        if app_label in self.route_app_labels:
            return db == 'ecommerce_db'
        return None

class PaymentRouter:

    route_app_labels = {'payment'}

    def db_for_read(self, model, **hints):

        if model._meta.app_label in self.route_app_labels:
            return 'payment_db'
        return None

    def db_for_write(self, model, **hints):
        
        if model._meta.app_label in self.route_app_labels:
            return 'payment_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        
        if app_label in self.route_app_labels:
            return db == 'payment_db'
        return None