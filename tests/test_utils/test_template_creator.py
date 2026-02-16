from unittest import mock
from utils.argo_app_writer import create_template, write_output_to_file

import os 

BRANCH = "XYZABC"
branch_lower = BRANCH.lower()
EXPECTED_OUTPUT = f'''
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: fermentation-station-agent-{branch_lower}
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/lukasb27/fermentation-station-agent.git
    targetRevision: {BRANCH}
    path: k8s
    kustomize:
      images:
        - lukasball/fermentation-station-agent=lukasball/fermentation-station-agent:{branch_lower}
  destination:
    server: https://kubernetes.default.svc
    namespace: {branch_lower}
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
'''

@mock.patch.dict(os.environ, {"BRANCH": BRANCH})
def test_config_file_renders_correctly():
    rendered_output = create_template(BRANCH)
    assert rendered_output.strip() == EXPECTED_OUTPUT.strip()
    

def test_output_writes_correctly():
    write_output_to_file("test.txt", "ok")
    with open("test.txt") as f:
        file_data = f.read()
    
    assert file_data == "ok"
    os.remove("test.txt")
    
    
