import json
import os
import tomllib
from pathlib import Path

import jinja2


def main():
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("."),
        autoescape=jinja2.select_autoescape(),
        undefined=jinja2.StrictUndefined,
    )

    services = []
    suffixes = []
    filenames = []
    output_dir = Path()
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
        services += config["services"]
        suffixes += [
            ".{}".format(suffix) if not suffix.startswith(".") else suffix
            for suffix in config["suffixes"]
        ]
        output_dir = Path(config["output_dir"])
        filenames += config["filenames"]
    output_dir.mkdir(parents=True, exist_ok=True)

    variables = {"docker_compose_root": str(output_dir.resolve())}
    for file in Path.cwd().glob(
        "*.{}.auto.vars.json".format(os.environ["PROJECT_ENV"])
    ):
        with open(file, "r") as f:
            variables.update(json.load(f))

    for service in services:
        service_dir = Path(service)
        for file in service_dir.glob("**/*"):
            if (file.suffix not in suffixes) and (file.name not in filenames):
                continue
            rendered = jinja_env.get_template(str(file)).render(variables)
            rendered_path = output_dir / (file.resolve().relative_to(Path.cwd()))
            rendered_path.parent.mkdir(parents=True, exist_ok=True)
            with open(rendered_path, "w") as f:
                f.write(rendered)
            rendered_path.chmod(file.stat().st_mode)


if __name__ == "__main__":
    main()
