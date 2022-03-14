from django.db import models
#
from QAPMS.utils.models import BaseModel
#
# Create your models here.


class ProjectInformation(BaseModel):
    GENDER_CHOICES = (
        (1, 'PG1'),
        (2, 'PG2'),
        (3, 'PG3'),
        (4, 'PG4'),
        (5, 'PG5'),
        (6, 'PG6')
    )
    project_name = models.CharField(max_length=30, verbose_name='项目名称', unique=True)
    project_desc = models.CharField(max_length=500, verbose_name='项目描述')
    QAPL = models.CharField(max_length=25, verbose_name='QAPL')
    project_manager = models.CharField(max_length=25, verbose_name='项目经理')
    product_manager = models.CharField(max_length=25, verbose_name='产品经理')
    EPL = models.CharField(max_length=25)
    plan_start = models.DateField(verbose_name='计划开始时间', null=True)
    plan_end = models.DateField(verbose_name='计划结束时间', null=True)
    practical_start = models.DateField(verbose_name='实际开始时间', null=True)
    practical_end = models.DateField(verbose_name='实际结束时间', null=True)
    status = models.SmallIntegerField(choices=GENDER_CHOICES, default=1, verbose_name='项目进度', null=True)

    class Meta:
        db_table = 'Project_Infor'
        verbose_name = '项目信息'

    def __str__(self):
        return self.project_name

class Schedule(BaseModel):
    GENDER_CHOICES = (
        (1, 'PG1'),
        (2, 'PG2'),
        (3, 'PG3'),
        (4, 'PG4'),
        (5, 'PG5'),
        (6, 'PG6')
    )
    project = models.ForeignKey(ProjectInformation, on_delete=models.PROTECT)
    phase = models.SmallIntegerField(choices=GENDER_CHOICES, default=1, verbose_name='PG')
    plan_start = models.DateField(verbose_name='计划开始时间', null=True)
    plan_end = models.DateField(verbose_name='计划结束时间', null=True)
    practical_start = models.DateField(verbose_name='实际开始时间', null=True)
    practical_end = models.DateField(verbose_name='实际结束时间', null=True)

    class Meta:
        db_table = 'project_schedule'
        verbose_name = '项目进度'

class ProductInformation(BaseModel):
    GENDER_CHOICES = (
        (0, 'NVR'),
        (1, 'IPC'),
        (2, 'PTZ'),
        (3, 'Accessory')
    )
    project = models.ForeignKey(ProjectInformation, on_delete=models.PROTECT)
    product_type = models.SmallIntegerField(choices=GENDER_CHOICES, default=1, verbose_name='产品类型')
    SKU = models.CharField(max_length=20, verbose_name='产品型号', unique=True)
    SKU_name = models.CharField(max_length=30, verbose_name='产品名称', null=True)
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'Product_Infor'
        verbose_name = '产品信息'

    def __str__(self):
        return self.SKU_name


class Certification(BaseModel):
    SKU = models.ForeignKey(ProductInformation, on_delete=models.PROTECT)
    certification_type = models.CharField(max_length=10, verbose_name='认证类型', unique=True)
    certification_report = models.CharField(max_length=40, verbose_name='报告', unique=True)
    certification_location = models.CharField(max_length=40, verbose_name='文件保存位置', unique=True)
    # certification_path = models.FilePathField()

    class Meta:
        db_table = 'Certification_Infor'
        verbose_name = '证书信息'

    def __str__(self):
        return self.certification_type


class FWList(BaseModel):
    SKU = models.ForeignKey(ProductInformation, on_delete=models.PROTECT)
    version_information = models.CharField(max_length=40, verbose_name='版本号', unique=True)
    FW_location = models.CharField(max_length=40, verbose_name='软件保存位置', unique=True)
    releasenote_location = models.CharField(max_length=40, verbose_name='软件保存位置', unique=True)

    class Meta:
        db_table = 'FW_List'
        verbose_name = '软件版本信息'

    def __str__(self):
        return self.version_information
