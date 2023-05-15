from fastapi import FastAPI
from api.endpoints import login, users, admin

app = FastAPI()

app.include_router(login.login_router, prefix='/api')
app.include_router(users.users_router, prefix='/api')
app.include_router(admin.admin_router, prefix='/api')
