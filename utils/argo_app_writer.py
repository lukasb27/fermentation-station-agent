from jinja2 import Environment, FileSystemLoader
import os

def sanitize_name(name: str) -> str:
    """Centralized sanitization logic for K8s compatibility."""
    return name.lower().replace('/', '-').replace('_', '-')

def create_template(branch: str, sha: str, pr_number: str) -> str:
    sanitized_branch = sanitize_name(branch)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(current_dir, "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("argocd-application.template.yaml")

    output = template.render(
        # Logical improvement: Using PR_NUMBER makes this globally unique
        APP_NAME=f"fs-agent-pr-{pr_number}",
        NAMESPACE=f"fs-pr-{pr_number}",
        IMAGE=f"lukasball/fermentation-station-agent:{sanitized_branch}",
        BRANCH=branch,
        SHA=sha,
        PR_NUMBER=pr_number
    )

    return output

def write_output_to_file(path_to_file: str, data: str) -> None:
    with open(path_to_file, "w") as f:
        f.write(data)

def main():
    branch = os.environ["BRANCH"]
    sha = os.environ.get("SHA", "latest")
    pr_number = os.environ.get("PR_NUMBER", "0")
    
    filename = f"{sanitize_name(branch)}.yaml"
    output = create_template(branch, sha, pr_number)
    write_output_to_file(filename, output)

if __name__ == '__main__':
    main()