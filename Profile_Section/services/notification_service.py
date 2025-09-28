from models import Notice
from schemas import NoticeCreateSchema

def get_notices():
    return Notice.all()

def create_notice(data: NoticeCreateSchema):
    notice = Notice(**data.dict())
    notice.save()
    return notice
