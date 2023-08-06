from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_c

queue_importer = CeleryQueue(
    label=_('Importer'), name='importer', worker=worker_c
)
queue_model_filer = CeleryQueue(
    label=_('Model filer'), name='filer', worker=worker_c
)

queue_importer.add_task_type(
    label=_('Process an import setup'),
    dotted_path='importer.tasks.task_import_setup_process'
)
queue_importer.add_task_type(
    label=_('Process an import setup item'),
    dotted_path='importer.tasks.task_import_setup_item_process'
)
queue_importer.add_task_type(
    label=_('Populate the items of an import setup'),
    dotted_path='importer.tasks.task_import_setup_populate'
)

queue_model_filer.add_task_type(
    label=_('Generates CSV files from a model'),
    dotted_path='importer.tasks.task_model_filer_save'
)
queue_model_filer.add_task_type(
    label=_('Loads CSV files and created models'),
    dotted_path='importer.tasks.task_model_filer_load'
)
