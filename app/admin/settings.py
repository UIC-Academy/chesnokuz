from starlette_admin.contrib.sqla import Admin

from app.database import engine
from app.models import User
from app.admin.views import UserAdminView
from app.admin.auth import JSONAuthProvider


admin = Admin(
    engine=engine,
    title="Chesnokdek admin",
    base_url="/admin",
    auth_provider=JSONAuthProvider(login_path="/login", logout_path="/logout"),
)


admin.add_view(UserAdminView(User, icon="fa fa-user"))
