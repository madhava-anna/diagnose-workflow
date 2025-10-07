from workers import WorkerEntrypoint, Response
import os
import uuid
import time

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return Response("Hello World!")
