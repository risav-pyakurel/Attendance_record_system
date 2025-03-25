from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.urls import reverse_lazy
from django.shortcuts import render

USER_GROUPS = {"employee": ["employee", "admin"],    "admin": ["admin"],}



class AuthMixin(LoginRequiredMixin):      
    login_url = reverse_lazy('dashboard:login')
    
    
class CustomAccessMixin(AccessMixin):
    unauthorized_template = "employee/unauthorized_template.html"
    
    def handle_wrong_user_type(self, request, msg):        
        return render(request, self.unauthorized_template, context=msg)

class EmployeePermissionMixin(CustomAccessMixin):    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.groups.filter(name__in=USER_GROUPS['employee']).exists():
                return super().dispatch(request, *args, **kwargs)
            msg = {"error": "You do not have Employee Permission on this site."}
            return self.handle_wrong_user_type(request, msg)

class AttendancePermissionMixins(CustomAccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.groups.filter(name__in=USER_GROUPS['employee']).exists():
                return super().dispatch(request,*args,**kwargs)
            msg ={"error":"You don't have Employee Permission on this page."}
            return self.handle_wrong_user_type(request, msg)

                
                
