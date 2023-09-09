from django import forms
from .models import UOMMaster, CategoryMaster, SubCatMaster, ProductMaster,UserCompMaster

class UserCompMasterForm(forms.ModelForm):
    class Meta:
        model=UserCompMaster
        fields=['name','email','contact','password','userfirst','isadmin']

class CatMasterForm(forms.ModelForm):
    class Meta:
        model=CategoryMaster
        fields=['catname','active']

class SubCatMasterForm(forms.ModelForm):
    class Meta:
        model=SubCatMaster
        fields=['catname','subcat','active']

class UOMMasterForm(forms.Form):
    class Meta:
        model=UOMMaster
        fields=['','']

# class ProdMasterForm(forms.ModelForm):
#     class Meta:
#         model=ProductMaster
#         fields=['prodcat','subcat','prodname','mainuom',
#         'contains','salesuom','purchaserate','salesrate',
#         'tax','stock','warnstock','discount','hsncode']