from __future__ import absolute_import, unicode_literals

from django import forms
from django.conf import settings
from django.contrib import admin
from django.db.models import When, Value, Case
from django.forms.widgets import Select
from django.template.defaultfilters import pluralize
from django.utils.translation import ugettext_lazy as _

from celery import current_app
from celery.utils import cached_property
from kombu.utils.json import loads

from django.db import models

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text  # noqa




from django import forms
from .models import Equipamento,Gpequipamentos
from django.forms import ModelForm
from django_celery_beat.models import *


class EquipamentoForm(ModelForm):
	class Meta:
		model = Equipamento
		fields = '__all__'

class IntervalForm(ModelForm):
	class Meta:
		model = IntervalSchedule
		fields = '__all__'


class CrontabForm(ModelForm):
	class Meta:
		model = CrontabSchedule
		exclude = ['timezone']
		fields = '__all__'
		

class GpequipamentosForm(ModelForm):
	class Meta:
		model = Gpequipamentos
		fields = '__all__'






class TaskSelectWidget(Select):
    """Widget that lets you choose between task names."""

    celery_app = current_app
    _choices = None

    def tasks_as_choices(self):
        _ = self._modules  # noqa
        tasks = list(sorted(name for name in self.celery_app.tasks
                            if not name.startswith('celery.')))
        return (('', ''), ) + tuple(zip(tasks, tasks))

    @property
    def choices(self):
        if self._choices is None:
            self._choices = self.tasks_as_choices()
        return self._choices

    @choices.setter
    def choices(self, _):
        # ChoiceField.__init__ sets ``self.choices = choices``
        # which would override ours.
        pass

    @cached_property
    def _modules(self):
        self.celery_app.loader.import_default_modules()


class TaskChoiceField(forms.ChoiceField):
    """Field that lets you choose between task names."""

    widget = TaskSelectWidget

    def valid_value(self, value):
        return True





class PeriodicTaskForm(ModelForm):
	
	

	class Meta:
		model = PeriodicTask
		exclude = ()
		fields = ['name','interval','crontab','task','enabled','one_off']
		actions = ('enable_tasks', 'disable_tasks')
		search_fields = ('name',)
		

	def changelist_view(self, request, extra_context=None):
		extra_context = extra_context or {}
		scheduler = getattr(settings, 'CELERY_BEAT_SCHEDULER', None)
		extra_context['wrong_scheduler'] = not is_database_scheduler(scheduler)
		return super(PeriodicTaskAdmin, self).changelist_view(
		request, extra_context)

	def get_queryset(self, request):
		qs = super(PeriodicTaskAdmin, self).get_queryset(request)
		return qs.select_related('interval', 'crontab', 'solar')

	def _message_user_about_update(self, request, rows_updated, verb):
	
		self.message_user(
		    request,
		    _('{0} task{1} {2} successfully {3}').format(
		        rows_updated,
		        pluralize(rows_updated),
		        pluralize(rows_updated, _('was,were')),
		        verb,
		    ),
		)	

	def enable_tasks(self, request, queryset):
		rows_updated = queryset.update(enabled=True)
		PeriodicTasks.update_changed()
		self._message_user_about_update(request, rows_updated, 'enabled')
		enable_tasks.short_description = _('Enable selected tasks')

	def disable_tasks(self, request, queryset):
		rows_updated = queryset.update(enabled=False)
		PeriodicTasks.update_changed()
		self._message_user_about_update(request, rows_updated, 'disabled')
		disable_tasks.short_description = _('Disable selected tasks')

	def _toggle_tasks_activity(self, queryset):
		return queryset.update(enabled=Case(
		    When(enabled=True, then=Value(False)),
		    default=Value(True),
		))

	def toggle_tasks(self, request, queryset):
		rows_updated = self._toggle_tasks_activity(queryset)
		PeriodicTasks.update_changed()
		self._message_user_about_update(request, rows_updated, 'toggled')
		toggle_tasks.short_description = _('Toggle activity of selected tasks')

	def run_tasks(self, request, queryset):
		self.celery_app.loader.import_default_modules()
		tasks = [(self.celery_app.tasks.get(task.task),
		          loads(task.args),
		          loads(task.kwargs))
		         for task in queryset]
		task_ids = [task.delay(*args, **kwargs)
		            for task, args, kwargs in tasks]
		tasks_run = len(task_ids)
		self.message_user(
		    request,
		    _('{0} task{1} {2} successfully run').format(
		        tasks_run,
		        pluralize(tasks_run),
		        pluralize(tasks_run, _('was,were')),
		    ),
		)
		run_tasks.short_description = _('Run selected tasks')



