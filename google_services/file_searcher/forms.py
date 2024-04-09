from django import forms


class FileUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        uploaded_file = self.cleaned_data["file"]
        if uploaded_file.content_type != "application/pdf":
            self.add_error("file", "Only PDF files are accepted")

        return uploaded_file
