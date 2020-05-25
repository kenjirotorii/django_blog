from django import forms
from django.urls import reverse_lazy
from django.conf import settings


class FileUploadableTextArea(forms.Textarea):
    """ファイルアップロード可能なテキストエリア"""

    class Media:
        js_url = settings.STATIC_URL + 'js/'
        js = [js_url + 'csrf.js', js_url + 'upload.js']

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if 'class' in self.attrs:
            self.attrs['class'] += ' uploadable vLargeTextField'
        else:
            self.attrs['class'] = 'uploadable vLargeTextField'
        self.attrs['data-url'] = reverse_lazy('blog:upload')
