from starlette_admin.contrib.sqla import Admin

from app.database import engine
from app.models import User
from app.admin.views import UserAdminView


admin = Admin(engine=engine, title="Chesnokdek admin", base_url="/admin")


admin.add_view(UserAdminView(User, icon="fa fa-user"))
