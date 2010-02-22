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
        The 'count' attribute can be specified to default the number of 
        file boxes initially presented.
        """
        super(MultiFileInput, self).__init__(attrs)
        if attrs:
            self.attrs.update(attrs)
    
    def render(self, name, value, attrs=None):
        """
        Renders the MultiFileInput.
        Should not be overridden.  Instead, subclasses should override the
        js, link, and/or fields methods which provide content to this method.
        """
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name+'[]')
        count = final_attrs['count']
        if count<1: count=1
        del final_attrs['count']
        js = self.js(name, value, count, final_attrs)
        link = self.link(name, value, count, final_attrs)
        fields = self.fields(name, value, count, final_attrs)
        return js+fields+link
    
    def fields(self, namey, value, count, attrs=None):
        """
        Renders the necessary number of file input boxes.
        """
        return u''.join([u'<input%s />\n' % flatatt(dict(attrs, id=attrs['id']+str(i))) for i in range(count)])
    
    def link(self, name, value, count, attrs=None):
        """
        Renders a link to add more file input boxes.
        """
        return u"<a onclick=\"javascript:new_%(name)s()\">+</a>" % {'name':name}
    
    def js(self, name, value, count, attrs=None):
        """
        Renders a bit of Javascript to add more file input boxes.
        """
        return u"""
        <script>
        <!--
        %(id)s_counter=%(count)d;
        function new_%(name)s() {
            b=document.getElementById('%(id)s0');
            c=b.cloneNode(false);
            c.id='%(id)s'+(%(id)s_counter++);
            b.parentNode.insertBefore(c,b.parentNode.lastChild.nextSibling);
        }
        -->
        </script>
        """ % {'id':attrs['id'], 'name':name, 'count':count}
    
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
    count = 1
    
    def __init__(self, count=1, *args, **kwargs):
        self.count = count
        super(MultiFileField, self).__init__(*args, **kwargs)
    
    def widget_attrs(self, widget):
        """
        Adds the count to the MultiFileInput widget.
        """
        if isinstance(widget, MultiFileInput):
            return {'count':self.count}
        return {}
    
    def clean(self, data):
        """
        Cleans the data and makes sure that all the files had some content.
        Also checks whether a file was required.
        """
        super(MultiFileField, self).clean(data)
        if not self.required and data in EMPTY_VALUES:
            return None
        
        if len(data) != self.count:
            raise ValidationError(ugettext(u"An incorrect number of files were uploaded."))
        
        return data