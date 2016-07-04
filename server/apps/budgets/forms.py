from copy import copy
import uuid

from django import forms

from .models import (
    Transaction,
    Budget,
    ExpenseBudget,
    SavingsBudget,
    DebtBudget
)


class TransactionDetailForm(forms.ModelForm):

    class Meta:
        model = Transaction
        exclude = []

    def clean(self):
        cleaned_data = super(TransactionDetailForm, self).clean()
        amount = cleaned_data.get('amount')
        transaction_type = cleaned_data.get('transaction_type')
        if (transaction_type == 'credit' and amount <= 0) or \
           (transaction_type == 'debit' and amount >= 0): 
            raise forms.ValidationError(
                    "Invalid amount for transaction type."
                    " Use negative amount for debits and "
                    "positive amount for credits.")


class BudgetDetailForm(forms.ModelForm):
    
    class Meta:
        model = ExpenseBudget
        exclude = []


def dynamic_form_factory(base_model, groups,
                         label, excluded_fields=[]):
    """
        ``base_model`` is a model that contains fields
        that are common to each group.
        ``groups`` is a tuple mapping to additional
        models.
        ``excluded_fields`` is a list of fields to exclude
        from the form.
    """
    TYPES = (
        ('', '----'),
        ('savings', 'Savings'),
        ('expense', 'Expense'),
        ('debt', 'Debt payment'),
    )
    MODELS = {
        'savings': SavingsBudget,
        'expense': ExpenseBudget,
        'debt': DebtBudget
    }

    # Grab extra fields to include
    extra_fields = {}
    for model_mapping in groups:
        extra_fields[model_mapping[0]] = []
        for field in model_mapping[1]._meta.fields:
            if field not in base_model._meta.fields:
                if field.formfield():
                    extra_fields[model_mapping[0]].append(
                        (field.verbose_name, field.formfield()))
    
    def make_unique(fields):
        new = copy(fields)
        seen = {}
        all_fields = [i for sub in fields.values() for i in sub]
        for group, _fields in fields.items():
            for field in _fields:
                if field[0] in seen:
                    dup = new[group].pop(new[group].index(field))
                    print("^",field[1], dir(field[1]))
                    new[group].append((dup[0]+'_'+uuid.uuid4().hex[:5], dup[1]))
                else:
                    seen[field[0]] = True
        print(seen)
        return new      

    class _Form(forms.ModelForm):
        
        # The field which determines which group to display.
        group_select = forms.ChoiceField(choices=TYPES,
            label=label, required=True,
            widget=forms.Select(
                attrs={'onChange': 'getFormGroup()'}))

        class Meta:
            model = base_model
            exclude = excluded_fields
        
        def __init__(self, *args, **kwargs):
            super(_Form, self).__init__(*args, **kwargs)
            # Make sure there's no fields with the same name
            # in different groups.
            _extra_fields = make_unique(extra_fields)
            # Now add the extra form fields from the groups.
            for group, fields in _extra_fields.items():
                for _field in fields:
                    print(_field)
                    self.fields[_field[0]] = _field[1]
                    self.fields[_field[0]].widget.attrs['data-groupid'] = \
                            'group_{}'.format(group)
                    self.fields[_field[0]].required = False

        def clean(self):
            cleaned_data = super(_Form, self).clean()
            selected_group = cleaned_data['group_select']
            for _,f in self.fields.items():
                try:
                    if f.widget.attrs['data-groupid'].split('group_')[1] != selected_group:
                        f.required = False
                except KeyError:
                    continue
            print("-->",cleaned_data)

        def save(self):
            data = self.cleaned_data
            _model = MODELS[data['group_select']]
            data.pop('group_select')
            print(data)
            _model.objects.create(**data)
    
    return _Form



def get_budget_form(base_model):
    
    TYPES = (
        ('', '----'),
        ('savings', 'Savings'),
        ('expense', 'Expense'),
        ('debt', 'Debt payment'),
    )

    PERIODS = (
        ('yearly', 'Yearly'),
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
        ('daily', 'Daily'),
    )

    MODELS = {
        'savings': SavingsBudget,
        'expense': ExpenseBudget,
        'debt': DebtBudget
    }

    class BudgetForm(forms.ModelForm):
        
        limit = forms.DecimalField(widget=forms.NumberInput(
                    attrs={'data-groupid': 'group_expense'}))
        period = forms.ChoiceField(choices=PERIODS,
                    widget=forms.Select(
                        attrs={'data-groupid': 'group_expense'}))

        budget_type = forms.ChoiceField(choices=TYPES,
                        label='What will this budget be used for?',
                        required=True,
                        widget=forms.Select(
                            attrs={'onChange': 'getFormGroup()'}))
        
        class Meta:
            model = base_model
            exclude = []

        def __init__(self, *args, **kwargs):
            super(BudgetForm, self).__init__(*args, **kwargs)

        def save(self):
            data = self.cleaned_data
            _model = MODELS[data['budget_type']]
            data.pop('budget_type')
            _model.objects.create(**data)

    return BudgetForm
    
