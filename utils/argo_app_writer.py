from jinja2 import Environment, FileSystemLoader
import os

def create_template(branch: str, sha: str, pr_number: str) -> str:
    branch_lower = branch.lower()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(current_dir, "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("argocd-application.template.yaml")

    output = template.render(
        APP_NAME=f"fermentation-station-agent-{branch_lower}",
        NAMESPACE=branch_lower,
        IMAGE=f"lukasball/fermentation-station-agent:{branch_lower}",
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
    sha = os.environ["SHA"]
    pr_number = os.environ["PR_NUMBER"]
    # Sanitize and lowercase filename to match workflow expectations and avoid path issues
    filename = f"{branch.lower().replace('/', '-')}.yaml"
    output = create_template(branch, sha, pr_number)
    write_output_to_file(filename, output)

if __name__ == '__main__':
    main()