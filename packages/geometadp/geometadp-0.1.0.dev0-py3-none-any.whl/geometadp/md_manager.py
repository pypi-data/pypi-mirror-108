import sys
import ipywidgets as widgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
import json
import dicttoxml
from IPython.core.display import display

"""
Each widget object is associated with one metadata entry


Requirements for widget objects
1) .is_visible() <- this function evaluates if a widget is to be shown,
   i.e., based on the current value of another metadata-set

   This also implies marking itself for non-output.
   For example, if the data type is switched from lab to field,
   widget values should be retained, but not exported

2) we need a global refresh function
"""
import asyncio


# https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Events.html#Debouncing
class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        self._callback()

    def cancel(self):
        self._task.cancel()


def debounce(wait):
    """ Decorator that will postpone a function's
        execution until after `wait` seconds
        have elapsed since the last time it was invoked. """
    def decorator(fn):
        timer = None

        def debounced(*args, **kwargs):
            nonlocal timer

            def call_it():
                fn(*args, **kwargs)
            if timer is not None:
                timer.cancel()
            timer = Timer(wait, call_it)
        return debounced
    return decorator


class _widget_select_directory(object):
    """Use the QT5 widget to select a directory
    """
    def __init__(self, output_dict, key, help_text, callback=None):
        self.dialog = QFileDialog(None)
        self.dialog.setFileMode(QFileDialog.Directory)
        self.dialog.setOption(self.dialog.ShowDirsOnly, True)
        self.output_dict = output_dict
        self.key = key
        self.help_text = help_text
        self.callback = callback

    def _select_dir(self):
        fname = self.dialog.getExistingDirectory(
            None,
            self.help_text,
            # '/',
        )
        return fname

    def _button_click(self, x):
        directory = self._select_dir()
        self.label.value = directory
        self.output_dict[self.key] = directory
        if self.callback is not None:
            self.callback()

    def get_widget(self):

        button = widgets.Button(description=self.help_text)
        self.label = widgets.Label()

        button.on_click(self._button_click)
        return widgets.HBox([button, self.label])


class geo_metadata(object):
    def __init__(self):
        self.app = QApplication(sys.argv)

        # this stores the actual values exported to json/xml
        self.metadata = {}

        # stores the various widget objects. They are shown in this order
        self.widget_objects = []

        self._prepare_widgets()

    def _prepare_widgets(self):
        self.widget_objects.append(self._widget_header())
        # operator entries
        operator_widgets = []

        operator_widgets.append(self._widget_owner())
        operator_widgets.append(self._widget_email())

        operator_box = widgets.Box(operator_widgets)
        operator_box.layout.display = 'flex'
        operator_box.layout.align_items = 'stretch'

        self.widget_objects.append(
            widgets.VBox([
                widgets.HTML(
                    '<hr style="height:5px;border-width:0;color:black;' +
                    'background-color:black;"></hr>'
                ),
                widgets.Label('Operator Metadata:'),
                operator_box,
                widgets.HTML(
                    '<hr style="height:5px;border-width:0;color:black;' +
                    'background-color:black;"></hr>'
                ),
            ])
        )

        #
        self.widget_objects.append(self._widget_measurement_type())
        self.widget_objects.append(self._widget_method())
        self.widget_objects.append(self._widget_data_directory())
        self.widget_objects.append(self._widget_picture_directory())
        self.widget_objects.append(self._widget_document_directory())
        self.widget_objects.append(self._widget_output_directory())
        self.widget_objects.append(self._widget_datetime())

        self.widget_objects.append(self._widget_export())

    def _widget_header(self):
        """Show the header of the data mangement gui that explains the basic concepts
        """
        title = widgets.HTML(
            '<h2>Data Manager and Metadata Collector for CGAGS<h2/>')
        text = widgets.HTML('''
            This gui is designed to help with the initial preparation of one
            geophysical dataset. Starting from one or multiple input
            directories, a cleanly structured output directory is generated
            (without deleting any input files).

            <h3>Starting Point</h3>

            <ol>
                <li>Measurement data is located in one local directory (the
                'Data input directory')</li>
                <li>(optional)Pictures are located within a separate
                (sub-)directory</li>
                <li>(optional) Other documents (e.g., notes) are also located
                within a separate (sub-)directory</li>
            </ol>

            <h3>Activities of this gui</h3>

            <ol>
             <li>Copy measurement data files and auxiliary files (pictures,
             etc.) into the output directory structure</li>
             <li>Generate suitable metadata from user input</li>
             <li>Write this metadata into the directory structure, making it
             ready for further distribution</li>
            </ol>

            <b>Hit ENTER after finishing any one-line text input!<b />
             <hr
             style=
             "height:5px;border-width:0;color:black;background-color:gray">
        ''')

        vbox = widgets.VBox([title, text])
        return vbox

    def _widget_data_directory(self):
        data_directory = _widget_select_directory(
            self.metadata, 'data_dir', 'Data input directory',
            callback=self._update_widget_export
        )
        data_widget = data_directory.get_widget()

        return data_widget

    def _widget_picture_directory(self):
        picture_directory = _widget_select_directory(
            self.metadata, 'picture_dir', 'Picture input directory',
            callback=self._update_widget_export
        )
        picture_widget = picture_directory.get_widget()

        return picture_widget

    def _widget_document_directory(self):
        document_directory = _widget_select_directory(
            self.metadata, 'document_dir', 'Document input directory',
            callback=self._update_widget_export
        )
        document_widget = document_directory.get_widget()

        return document_widget

    def _widget_output_directory(self):
        output_directory = _widget_select_directory(
            self.metadata, 'output_dir', 'Output directory',
            callback=self._update_widget_export
        )
        output_widget = output_directory.get_widget()
        return output_widget

    def _widget_measurement_type(self):
        type_measurement = widgets.RadioButtons(
            options=['Laboratory Measurement', 'Field Measurement'],
            default='Laboratory Measurement',
            description='',
            disabled=False,
            # layout=layout,
        )
        label_mt = widgets.Label('Measurement type:')
        # set initial metadata
        self.metadata['measurement_type'] = 'laboratory'

        def _observe_measurement_type(change):
            self.metadata['measurement_type'] = type_measurement.value
            self._update_widget_export()

        type_measurement.observe(_observe_measurement_type)
        return widgets.HBox([label_mt, type_measurement])

    def _widget_method(self):
        method = widgets.RadioButtons(
            options=[
                'Geoelectrical - ERT',
                'Geoelectrical - TDIP',
                'Geoelectrical - sEIT',
                'Geoelectrical - SIP/EIS',
                'GPR',
                'Seismic',
            ],
            default='Geoelectrical - ERT',
            description='Method:',
            disabled=False,
            # layout=layout,
        )
        # set initial metadata
        self.metadata['method'] = 'Geoelectrical - ERT'

        def _observe_method(change):
            self.metadata['method'] = method.value
            self._update_widget_export()

        method.observe(_observe_method)
        return method

    def _widget_export(self):
        """Preview of metadata export"""

        self.widget_export = widgets.HTML()
        self.export_type = widgets.RadioButtons(
            options=['JSON', 'XML'],
            default='JSON',
            description='Export type:'
        )
        vbox = widgets.VBox(
            [
                widgets.HTML(
                    '<hr style="height:5px;border-width:0;color:black;' +
                    'background-color:gray"><hr />' +
                    '<h3>Preview of metadata export:<h3 />'),
                self.export_type,
                self.widget_export
            ]
        )

        def _observe_export_type(change):
            self._update_widget_export()

        self.export_type.observe(_observe_export_type)
        return vbox

    def _widget_owner(self):
        self.widget_owner = widgets.Text(
            description='Owner:',
        )

        @debounce(0.2)
        def _observe_owner(change):
            self.metadata['owner'] = self.widget_owner.value
            self._update_widget_export()

        self.widget_owner.observe(_observe_owner)
        return self.widget_owner

    def _widget_email(self):
        self.widget_email = widgets.Text(
            description='Email:',
        )

        @debounce(0.2)
        def _observe_email(change):
            self.metadata['email'] = self.widget_email.value
            self._update_widget_export()

        self.widget_email.observe(_observe_email)
        return self.widget_email

    def _widget_datetime(self):
        widget_dt = widgets.DatePicker(
            description='Datetime of measurement',
            disabled=False
        )

        def _observe_dt(change):
            date = widget_dt.value
            if date is not None:
                self.metadata['date'] = date.isoformat()
                self._update_widget_export()

        widget_dt.observe(_observe_dt)
        return widget_dt

    def export_metadata_to_json_str(self):
        """Generate a string representation of the metadata"""
        metadata_json_raw = json.dumps(self.metadata, indent=4)
        return metadata_json_raw

    def export_metadata_to_xml_str(self):
        xml = dicttoxml.dicttoxml(self.metadata)
        dom = dicttoxml.parseString(xml)
        metadata_xml = dom.toprettyxml()
        return metadata_xml

    def _update_widget_export(self):
        if self.export_type.value == 'JSON':
            metadata_str = self.export_metadata_to_json_str()
        else:
            metadata_str = self.export_metadata_to_xml_str()
        import html
        # self.widget_export.value = metadata_str
        self.widget_export.value = "<pre>{}</pre>".format(
            html.escape(metadata_str))

    def manage(self):
        self.vbox = widgets.VBox(self.widget_objects)
        display(self.vbox)

        # self.metadata['test1'] = 'balbaba'
        # self.metadata['test2'] = 832

        self._update_widget_export()
