# from fastapi import APIRouter
# from db.models import User, session
# from fastapi import FastAPI, HTTPException
# from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
# from sqlalchemy.orm import sessionmaker
#
# user_router = APIRouter(
#     prefix="/api/user",
#     tags=["auth"]
# )
#
# # users = Table(
# #     "users",
# #     metadata,
# #     Column("id", Integer, primary_key=True, index=True),
# #     Column("name", String),
# #     Column("email", String),
# # )
# #
# # metadata.create_all(engine)
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# db = Depends(get_db)
#
# @user_router.get('/api/users/{user_id}')
# def get_user(user_id: int):
#     user = db.query(User).filter_by(name=user.id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
#
# # @user_router.get('/api/users/{user_id}')
# # def get_user(user_id: int, db = Depends(get_db)):
# #     query = users.select().where(users.c.id == user_id)
# #     user = db.execute(query).fetchone()
# #     if not user:
# #         raise HTTPException(status_code=404, detail="User not found")
# #     return {"id": user.id, "name": user.username}
#
