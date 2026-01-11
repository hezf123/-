from django.db import models
from django.core.validators import MinValueValidator
import datetime

class Coach(models.Model):
    """教练模型"""
    name = models.CharField('教练姓名', max_length=50)
    phone = models.CharField('联系电话', max_length=20)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '教练'
        verbose_name_plural = '教练管理'
    
    def __str__(self):
        return self.name

class Student(models.Model):
    """学员模型"""
    # 状态选择
    STATUS_CHOICES = [
        ('报名中', '报名中'),
        ('科目一', '科目一'),
        ('科目二', '科目二'),
        ('科目三', '科目三'),
        ('科目四', '科目四'),
        ('毕业', '毕业'),
    ]
    
    # 车型选择
    CAR_TYPE_CHOICES = [
        ('C1', 'C1'),
        ('C2', 'C2'),
    ]
    
    # 自动生成学员编号
    def generate_student_id():
        prefix = "QC"
        year_month = datetime.datetime.now().strftime("%y%m")
        last_student = Student.objects.filter(student_id__startswith=f"{prefix}{year_month}").order_by('student_id').last()
        if last_student:
            last_num = int(last_student.student_id[-3:])
            new_num = last_num + 1
        else:
            new_num = 1
        return f"{prefix}{year_month}{new_num:03d}"
    
    # 基础信息字段（12个必填字段）
    student_id = models.CharField('学员编号', max_length=20, unique=True, default=generate_student_id)
    name = models.CharField('姓名', max_length=50)
    phone = models.CharField('手机号', max_length=20)
    id_card = models.CharField('身份证号', max_length=18)
    register_date = models.DateField('报名日期')
    car_type = models.CharField('报考车型', max_length=10, choices=CAR_TYPE_CHOICES)
    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True, verbose_name='教练')
    total_fee = models.DecimalField('总费用', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    paid_fee = models.DecimalField('已缴费', max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    balance = models.DecimalField('欠费', max_digits=10, decimal_places=2, default=0)
    status = models.CharField('当前状态', max_length=20, choices=STATUS_CHOICES, default='报名中')
    notes = models.TextField('备注', blank=True)
    
    # 时间相关字段
    transfer_date = models.DateField('转入时间', null=True, blank=True)
    start_training_date = models.DateField('上车时间', null=True, blank=True)
    graduation_date = models.DateField('结业时间', null=True, blank=True)
    
    # 资金相关字段
    cash_amount = models.DecimalField('现金收取金额', max_digits=10, decimal_places=2, default=0)
    prepay_coach_date = models.DateField('预付教练时间', null=True, blank=True)
    prepay_coach_amount = models.DecimalField('预付教练金额', max_digits=10, decimal_places=2, default=0)
    
    # 银行转账记录
    bank_transfer1_date = models.DateField('银行转账1时间', null=True, blank=True)
    bank_transfer1_amount = models.DecimalField('银行转账1金额', max_digits=10, decimal_places=2, default=0)
    bank_transfer2_date = models.DateField('银行转账2时间', null=True, blank=True)
    bank_transfer2_amount = models.DecimalField('银行转账2金额', max_digits=10, decimal_places=2, default=0)
    bank_transfer3_date = models.DateField('银行转账3时间', null=True, blank=True)
    bank_transfer3_amount = models.DecimalField('银行转账3金额', max_digits=10, decimal_places=2, default=0)
    
    # 教练支付
    pay_coach_date = models.DateField('支付教练时间', null=True, blank=True)
    pay_coach_amount = models.DecimalField('支付教练金额', max_digits=10, decimal_places=2, default=0)
    
    # 其他
    car_number = models.CharField('车号', max_length=20, blank=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '学员'
        verbose_name_plural = '学员管理'
        ordering = ['-register_date']
    
    def save(self, *args, **kwargs):
        # 自动计算欠费
        self.balance = self.total_fee - self.paid_fee
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.student_id})"

class PaymentRecord(models.Model):
    """收费记录模型"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payment_records', verbose_name='学员')
    payment_date = models.DateField('收费日期')
    amount = models.DecimalField('金额', max_digits=10, decimal_places=2)
    receiver = models.CharField('收款人', max_length=50, default='系统')
    notes = models.TextField('备注', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '收费记录'
        verbose_name_plural = '收费记录'
        ordering = ['-payment_date']
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 更新学员的已缴费金额
        student = self.student
        total_paid = PaymentRecord.objects.filter(student=student).aggregate(models.Sum('amount'))['amount__sum'] or 0
        student.paid_fee = total_paid
        student.save()
    
    def __str__(self):
        return f"{self.student.name} - {self.amount}元 - {self.payment_date}"

class CoachSettlement(models.Model):
    """教练结算模型"""
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, verbose_name='教练')
    settlement_month = models.CharField('结算月份', max_length=7)  # 格式：2024-01
    graduated_students = models.ManyToManyField(Student, verbose_name='毕业学员')
    unit_price = models.DecimalField('单价', max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField('应结算金额', max_digits=10, decimal_places=2)
    is_paid = models.BooleanField('是否已支付', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '教练结算'
        verbose_name_plural = '教练结算'
    
    def __str__(self):
        return f"{self.coach.name} - {self.settlement_month}"