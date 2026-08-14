from jinja2 import Environment, FileSystemLoader
import os
import re

MAX_NAME_LENGTH = 63  # DNS-1123 label ceiling


def slugify_branch(branch: str) -> str:
    slug = branch.lower().replace("/", "-")
    return re.sub(r"[^a-z0-9-]", "", slug)


def build_full_name(app_name: str, branch: str) -> str:
    branch_slug = slugify_branch(branch)
    return f"{app_name}-{branch_slug}"[:MAX_NAME_LENGTH]


def create_template(
    app_name: str, branch: str, sha: str, pr_number: str, repo_slug: str
) -> str:
    full_name = build_full_name(app_name, branch)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(current_dir, "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("argocd-application.template.yaml")

    output = template.render(
        APP_NAME=full_name,
        NAMESPACE=full_name,
        IMAGE=f"lukasball/fermentation-station-agent:{branch}",
        TEST_IMAGE=f"lukasball/fermentation-station-agent-integ-tests:{branch}",
        BRANCH=branch,
        SHA=sha,
        PR_NUMBER=pr_number,
        REPO_SLUG=repo_slug,
    )

    return output


def write_output_to_file(path_to_file: str, data: str) -> None:
    with open(path_to_file, "w") as f:
        f.write(data)


def main():
    app_name = os.environ["APP_NAME"]
    branch = os.environ["BRANCH"]
    sha = os.environ["SHA"]
    pr_number = os.environ["PR_NUMBER"]
    repo_slug = os.environ["REPO_SLUG"]
    full_name = build_full_name(app_name, branch)
    filename = f"{full_name}.yaml"
    output = create_template(app_name, branch, sha, pr_number, repo_slug)
    write_output_to_file(filename, output)


if __name__ == '__main__':
    main()
