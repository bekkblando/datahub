from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView
from data_analysis.models import Project
from fileupload.forms import DatafileUploadForm
from fileupload.uploadhandler import handle_datafile_upload
from datahub.helpers.mixins import AddContextInAsViewMixin


class DatafileUploadView(AddContextInAsViewMixin, FormView):
    template_name = 'single_form_view.html'
    form_class = DatafileUploadForm
    additional_context = {"panel_title": "Upload New File", "submit_button_name": "Upload"}

    def form_valid(self, form):
        user = User.objects.get(username=self.kwargs.get("username"))
        project = Project.objects.get(name=self.kwargs.get("project"), profile=user.profile)
        if self.request.user == user:
            handle_datafile_upload(self.get_form_kwargs().get('files')['file'],
                                   self.get_form_kwargs().get('data'),
                                   user,
                                   project)

        self.success_url = reverse_lazy("data_analysis:project_detail",
                                        kwargs={"username": user.username,
                                                "project": project.name})
        return super().form_valid(form)
