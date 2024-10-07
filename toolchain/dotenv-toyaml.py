import yaml


def env_to_yaml(env_file, yml_file):
    env_dict = {}

    # Lire le fichier .env
    with open(env_file, "r") as file:
        for line in file:
            # skip comments
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # split line into key and value
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")  # strip double quotes
                env_dict[key.lower()] = value

    yaml_content = env_dict
    with open(yml_file, "w") as file:
        file.write("---\n")  # Add the --- mark
        yaml.dump(yaml_content, file, default_flow_style=False, sort_keys=False)


if __name__ == "__main__":
    env_to_yaml(".env", "ops/ansible/vars/env.yml")
