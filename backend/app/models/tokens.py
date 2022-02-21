# from sqlalchemy import Column, DateTime, Integer, String, Text
# from sqlalchemy.sql import func

# from ..db import Base


# class Token(Base):
#     """Token class"""

#     __tablename__ = 'tokens'

#     id = Column(Integer, primary_key=True, index=True)
#     token_type = Column(String(20), nullable=False)
#     access_token = Column(Text(), nullable=False)
#     created_at = Column(DateTime(timezone=True), default=func.now())

#     def __init__(self,
#                  token_type: str,
#                  access_token: str):
#         self.token_type = token_type
#         self.access_token = access_token
