import json

from src.utils.analysts import get_external_skill_manifest


def main():
    print(json.dumps(get_external_skill_manifest(), indent=2))


if __name__ == "__main__":
    main()
