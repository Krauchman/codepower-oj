from datetime import datetime

from django.db.models import Max, F

from submission.models import Submission

from rest_framework.views import APIView
from rest_framework.response import Response

from django_q.tasks import async_task


class EvaluateAPIView(APIView):
    def post(self, request):
        problem_id = request.data['problemId']
        language = request.data['language']
        code = request.data['code']
        user_id = request.data['userId']

        submission_id = Submission.objects.order_by('-id')[:1].get().id + 1
        Submission.objects.create(
            id=submission_id,
            code=code,
            date=datetime.now(),
            language=language,
            problem_id=problem_id,
            user_id=user_id,
            verdict="In queue",
        )
        async_task('evaluation.tasks.evaluate', submission_id)

        return Response()
