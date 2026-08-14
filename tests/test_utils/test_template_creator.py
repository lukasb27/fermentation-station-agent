from unittest import mock
from utils.argo_app_writer import create_template, write_output_to_file, build_full_name, slugify_branch

import os

APP_NAME = "fermentation-station-agent"
BRANCH = "XYZABC"
PR_NUMBER = "pr-123"
SHA = "1234"
REPO_SLUG = "lukasb27/fermentation-station-agent"
branch_slug = slugify_branch(BRANCH)
full_name = build_full_name(APP_NAME, BRANCH)
EXPECTED_OUTPUT = f'''
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {full_name}
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/lukasb27/fermentation-station-agent.git
    targetRevision: {BRANCH}
    path: k8s
    kustomize:
      images:
        - lukasball/fermentation-station-agent=lukasball/fermentation-station-agent:{BRANCH}
        - lukasball/fermentation-station-agent-integ-tests=lukasball/fermentation-station-agent-integ-tests:{BRANCH}
      commonAnnotations:
        prNumber: "{PR_NUMBER}"
        commitSha: {SHA}
        repoSlug: {REPO_SLUG}
  destination:
    server: https://kubernetes.default.svc
    namespace: {full_name}
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
'''


def test_slugify_branch_lowercases_and_strips_slashes():
    assert slugify_branch("Feature/My_Branch!") == "feature-mybranch"


def test_build_full_name_truncates_after_prefixing():
    long_branch = "a" * 100
    result = build_full_name(APP_NAME, long_branch)
    assert len(result) == 63
    assert result.startswith(f"{APP_NAME}-")


@mock.patch.dict(os.environ, {"APP_NAME": APP_NAME, "BRANCH": BRANCH, "SHA": SHA, "PR_NUMBER": PR_NUMBER, "REPO_SLUG": REPO_SLUG})
def test_config_file_renders_correctly():
    rendered_output = create_template(APP_NAME, BRANCH, SHA, PR_NUMBER, REPO_SLUG)
    assert rendered_output.strip() == EXPECTED_OUTPUT.strip()


def test_output_writes_correctly():
    write_output_to_file("test.txt", "ok")
    with open("test.txt") as f:
        file_data = f.read()

    assert file_data == "ok"
    os.remove("test.txt")
