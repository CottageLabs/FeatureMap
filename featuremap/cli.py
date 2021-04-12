import yaml

from featuremap.core import run


def main():
    """
    ~~CLI:Entrypoint~~
    :return:
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config file")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.load(f.read(), Loader=yaml.CLoader)

    # ~~->Runner:Core~~
    run(config)

if __name__ == "__main__":
    main()
