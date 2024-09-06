
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
from django import forms

class AccountCreationForm(forms.ModelForm):
  """A form for creating new users. Includes all the required
  fields, plus a repeated password."""
  class Meta:
    model = Account
    fields = ('email', 'username')

class AccountChangeForm(forms.ModelForm):
  """A form for updating users. Excludes the password field."""
  password = forms.CharField(label="Password", widget=forms.PasswordInput, required=False)

  class Meta:
    model = Account
    fields = ('email', 'username', 'is_active', 'is_admin', 'is_staff')

  def __init__(self, *args, **kwargs):
    super(AccountChangeForm, self).__init__(*args, **kwargs)
    # Don't show the password field when editing existing users
    if self.instance.pk:
      self.fields['password'].widget.attrs['readonly'] = True

class AccountAdmin(UserAdmin):
  form = AccountChangeForm
  add_form = AccountCreationForm

  list_display = ('email', 'username', 'is_admin', 'is_staff')
  list_filter = ('is_admin', 'is_staff')
  fieldsets = (
    (None, {'fields': ('email', 'username', 'password')}),
    ('Permissions', {'fields': ('is_admin', 'is_staff')}),
  )
  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('email', 'username',)}
    ),
  )
  search_fields = ('email', 'username')
  ordering = ('email',)
  filter_horizontal = ()

  def get_form(self, request, obj=None, **kwargs):
    form = super().get_form(request, obj, **kwargs)
    if obj:  # If editing an existing object
      form.base_fields['password'].widget.attrs['readonly'] = True
    return form
  

admin.site.register(Account, AccountAdmin)