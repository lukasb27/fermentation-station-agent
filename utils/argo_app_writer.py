from jinja2 import Environment, FileSystemLoader
import os

def create_template(branch: str) -> str:
    branch = branch.lower()
    env = Environment(loader=FileSystemLoader("utils/templates"))
    template = env.get_template("argocd-application.template.yaml")

    output = template.render(
        APP_NAME=f"fermentation-station-agent-{branch}",
        NAMESPACE=branch,
        IMAGE=f"lukasball/fermentation-station-agent:{branch}"
    )

    return output

def write_output_to_file(path_to_file: str, data: str) -> None:
    with open(path_to_file, "w") as f:
        f.write(data)

def main():
    branch = os.environ["BRANCH"]
    filename = f"{branch}.yaml"
    output = create_template(branch)
    write_output_to_file(filename, output)

if __name__ == '__main__':
    main()