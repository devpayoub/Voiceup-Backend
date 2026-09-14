import os
import subprocess

from django.conf import settings
from django.http import HttpResponse


def status_view(request):
    # Render auto-sets RENDER_GIT_COMMIT (full SHA) for every deploy; its runtime
    # image has no .git dir, so shelling out to git only works for local dev.
    render_commit = os.environ.get('RENDER_GIT_COMMIT')
    if render_commit:
        commit = render_commit[:7]
    else:
        try:
            commit = subprocess.check_output(
                ['git', 'rev-parse', '--short', 'HEAD'], cwd=settings.BASE_DIR
            ).decode().strip()
        except Exception:
            commit = 'unknown'

    html = f"""<!DOCTYPE html>
<html><head><title>VoiceUp API</title></head>
<body style="font-family: sans-serif; display: flex; flex-direction: column;
             align-items: center; justify-content: center; height: 100vh; margin: 0;">
  <h1 style="color: #16a34a;">&#9989; Running</h1>
  <p>Commit: <code>{commit}</code></p>
</body></html>"""
    return HttpResponse(html)
