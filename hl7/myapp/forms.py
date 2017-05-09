from django import forms
import datetime
from myapp.models import Task, RoadMap
from django.forms import ModelForm


class CreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'estimate', 'road_map']

    def clean_road_map(self):
        roadmap = self.cleaned_data['road_map']
        return roadmap.name

    def clean_estimate(self):
        estimate = self.cleaned_data['estimate']
        if estimate < datetime.date.today():
            raise forms.ValidationError("Дата меньше сегодняшней")
        if type(estimate) != type(datetime.date.today()):
            raise forms.ValidationError("Неверный тип даты")
        return estimate

    def clean_title(self):
        title = self.cleaned_data['title']
        if type(title) != type(''):
            raise forms.ValidationError("Неверный тип заголовка")


class AnotherCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'estimate']

    def clean_estimate(self):
        estimate = self.cleaned_data['estimate']
        if estimate < datetime.date.today():
            raise forms.ValidationError("Дата меньше сегодняшней")
        if type(estimate) != type(datetime.date.today()):
            raise forms.ValidationError("Неверный тип даты")
        return estimate

    def clean_title(self):
        title = self.cleaned_data['title']
        if type(title) != type(''):
            raise forms.ValidationError("Неверный тип заголовка")


class CreateRoadMap(ModelForm):
    class Meta:
        model = RoadMap
        fields = ['rd_id', 'name']


class EditForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'estimate', 'state', 'road_map']

        # def clean_estimate(self):
        #    estimate = self.cleaned_data['estimate']
        #  if estimate < datetime.date.today():
        #      raise forms.ValidationError("Дата меньше сегодняшней")
        #  if type(estimate) != type(datetime.date.today()):
        #      raise forms.ValidationError("Неверный тип даты")
        #  return estimate

        # def clean_title(self):
        #    title = self.cleaned_data['title']
        #    if type(title) != type(''):
        #       raise forms.ValidationError("Неверный тип заголовка")

        # def clean_state(self):
        #    state = self.cleaned_data['state']
        #    if state!='in_progress' and state!='ready':
        #        raise forms.ValidationError("Невалидный статус")
