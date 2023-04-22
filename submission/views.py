from datetime import datetime

from django.db.models import Max, F

from submission.models import Submission

from rest_framework.views import APIView
from rest_framework.response import Response

from django_q.tasks import async_task


class EvaluateAPIView(APIView):
    def post(self, request):
        submission_id = request.data['submissionId']

        print(submission_id)

        async_task('evaluation.tasks.evaluate', submission_id)

        return Response()
