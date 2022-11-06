import yaml

from featuremap.core import run


def main():
    """
    ~~CLI:Entrypoint~~
    :return:
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--basedir", help="root directory of the documents you want featuremap to run over.  Will override the base_dir in the config file")
    parser.add_argument("-c", "--config", help="config file")
    parser.add_argument("-s", "--source_url", help="URL to link to source files. Will override any source_url in the config file")
    parser.add_argument("-o", "--out_dir",
                        help="Output directory. Will override any source_url in the config file")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.load(f.read(), Loader=yaml.CLoader)

    if args.basedir:
        config["base_dir"] = args.basedir

    if args.source_url:
        config["source_url"] = args.source_url

    if args.out_dir:
        config["out_dir"] = args.out_dir

    # ~~->Runner:Core~~
    run(config)

if __name__ == "__main__":
    main()
