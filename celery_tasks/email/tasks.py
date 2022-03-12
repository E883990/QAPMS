import logging
from django.core.mail import send_mail
from django.conf import settings

from celery_tasks.main import celery_app
# @celery_app.task(name='send_verify_email')
# bind：保证task对象会作为第一个参数自动传入
# name：异步任务别名
# retry_backoff：异常自动重试的时间间隔 第n次(retry_backoff×2^(n-1))s
# max_retries：异常自动重试次数的上限
logger = logging.getLogger('django')
@celery_app.task(bind=True, name='send_email_code', retry_backoff=3)
def send_email_code(self, email, email_code):
    # send_mail('标题', '普通邮件正文', '发件人', '收件人列表', '富文本邮件正文(html)')
    # html_message = '<p>尊敬的用户您好！</p>' \
    #                '<p>感谢您使用霍尼韦尔QA项目管理系统。</p>' \
    #                '<p>您的邮箱为：%s ：</p>' \
    #                '<p>您的激活码为：%06d</p>' % (email, email_code)
    try:

        send_mail('邮箱验证码', '您的邮箱验证码为'+ str(email_code), settings.EMAIL_FROM, [email])
    except Exception as e:
        logger.error(e)
        # 有异常自动重试三次
        raise self.retry(exc=e, max_retries=3)
