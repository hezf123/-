from django.contrib import admin
from django.utils.html import format_html
from .models import Coach, Student, PaymentRecord, CoachSettlement
import openpyxl
from django.http import HttpResponse

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'created_at']
    search_fields = ['name', 'phone']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'phone', 'car_type', 'coach', 'status', 'total_fee', 'paid_fee', 'balance']
    list_filter = ['status', 'car_type', 'coach', 'register_date']
    search_fields = ['student_id', 'name', 'phone', 'id_card']
    readonly_fields = ['student_id', 'balance', 'created_at', 'updated_at']
    list_per_page = 20
    actions = ['export_to_excel']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('student_id', 'name', 'phone', 'id_card', 'register_date', 'car_type', 'coach', 'status')
        }),
        ('费用信息', {
            'fields': ('total_fee', 'paid_fee', 'balance')
        }),
        ('时间信息', {
            'fields': ('transfer_date', 'start_training_date', 'graduation_date')
        }),
        ('资金记录', {
            'fields': ('cash_amount', 'prepay_coach_date', 'prepay_coach_amount',
                      'bank_transfer1_date', 'bank_transfer1_amount',
                      'bank_transfer2_date', 'bank_transfer2_amount',
                      'bank_transfer3_date', 'bank_transfer3_amount',
                      'pay_coach_date', 'pay_coach_amount')
        }),
        ('其他信息', {
            'fields': ('car_number', 'notes')
        }),
    )
    
    def export_to_excel(self, request, queryset):
        """导出Excel功能"""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "学员数据"
        
        # 表头
        headers = ['学员编号', '姓名', '手机号', '身份证号', '报名日期', '报考车型', '教练', 
                  '总费用', '已缴费', '欠费', '当前状态', '备注']
        ws.append(headers)
        
        # 数据
        for student in queryset:
            ws.append([
                student.student_id,
                student.name,
                student.phone,
                student.id_card,
                student.register_date,
                student.get_car_type_display(),
                str(student.coach) if student.coach else '',
                student.total_fee,
                student.paid_fee,
                student.balance,
                student.get_status_display(),
                student.notes
            ])
        
        # 响应
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=students.xlsx'
        wb.save(response)
        return response
    
    export_to_excel.short_description = "导出选中学员到Excel"

@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'payment_date', 'amount', 'receiver']
    list_filter = ['payment_date', 'receiver']
    search_fields = ['student__name', 'student__student_id']

@admin.register(CoachSettlement)
class CoachSettlementAdmin(admin.ModelAdmin):
    list_display = ['coach', 'settlement_month', 'total_amount', 'is_paid', 'created_at']
    list_filter = ['settlement_month', 'is_paid']
    search_fields = ['coach__name']