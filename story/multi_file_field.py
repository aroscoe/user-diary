from django.utils.datastructures import MultiValueDict
from django.utils.translation import ugettext
from django.forms.fields import Field, EMPTY_VALUES
from django.forms.widgets import FileInput
from django.forms.util import ValidationError, flatatt

class MultiFileInput(FileInput):
    """
    A widget to be used by the MultiFileField to allow the user to upload
    multiple files at one time.
    """
    
    def __init__(self, attrs=None):
        """
        Create a MultiFileInput.
        The 'num_fields' attribute can be specified to default the number of 
        file boxes initially presented.
        """
        super(MultiFileInput, self).__init__(attrs)
        self.attrs = {'num_fields': 1}
        if attrs:
            self.attrs.update(attrs)
    
    def render(self, name, value, attrs=None):
        """
        Renders the MultiFileInput.
        Should not be overridden.  Instead, subclasses should override the
        js, link, and/or fields methods which provide content to this method.
        """
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name+'[]')
        num_fields = final_attrs['num_fields']
        if num_fields<1: num_fields=1
        del final_attrs['num_fields']
        
        js = self.js(name, value, num_fields, final_attrs)
        link = self.link(name, value, num_fields, final_attrs)
        fields = self.fields(name, value, num_fields, final_attrs)
        
        return js+fields+link
    
    def fields(self, name, value, num_fields, attrs=None):
        """
        Renders the necessary number of file input boxes.
        """
        return u''.join([u'<input%s />\n' % flatatt(dict(attrs, id=attrs['id']+str(i))) for i in range(num_fields)])
    
    def link(self, name, value, num_fields, attrs=None):
        """
        Renders a link to add more file input boxes.
        """
        return u"<a onclick=\"javascript:new_%(name)s()\">+</a>" % {'name': name}
    
    def js(self, name, value, num_fields, attrs=None):
        """
        Renders a bit of Javascript to add more file input boxes.
        """
        return u"""
        <script>
        <!--
        %(id)s_num_fieldser=%(num_fields)d;
        function new_%(name)s() {
            b=document.getElementById('%(id)s0');
            c=b.cloneNode(false);
            c.id='%(id)s'+(%(id)s_num_fieldser++);
            b.parentNode.insertBefore(c,b.parentNode.lastChild.nextSibling);
        }
        -->
        </script>
        """ % {'id': attrs['id'], 'name': name, 'num_fields': num_fields}
    
    def value_from_datadict(self, data, files, name):
        """
        File widgets take data from FILES, not POST.
        """
        name = name+'[]'
        if isinstance(files, MultiValueDict):
            return files.getlist(name)
        else:
            return None

class MultiFileField(Field):
    """
    A field allowing users to upload multiple files at once.
    """
    
    widget = MultiFileInput
    num_fields = 1
    
    def __init__(self, num_fields=1, strict=False, *args, **kwargs):
        """
        num_fields - determines how many file input fields to show be default
        strict - number of files uploaded must equal num_fields
        """
        
        self.num_fields = num_fields
        self.strict = strict
        super(MultiFileField, self).__init__(*args, **kwargs)
    
    def widget_attrs(self, widget):
        """
        Adds the num_fields to the MultiFileInput widget.
        """
        if isinstance(widget, MultiFileInput):
            return {'num_fields': self.num_fields}
        return {}
    
    def clean(self, data):
        """
        Cleans the data and makes sure that all the files had some content.
        Also checks whether a file was required.
        """
        super(MultiFileField, self).clean(data)
        if not self.required and data in EMPTY_VALUES:
            return None
        
        if self.strict and len(data) != self.num_fields:
            raise ValidationError(ugettext(u"An incorrect number of files were uploaded."))
        
        return data