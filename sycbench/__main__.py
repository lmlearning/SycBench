import argparse

from .pipeline import transform_dataset


def main():
    parser = argparse.ArgumentParser(description="SycBench dataset transformer")
    subparsers = parser.add_subparsers(dest="command", required=True)

    t = subparsers.add_parser("transform", help="Transform dataset")
    t.add_argument("--input", required=True, help="Input JSONL dataset")
    t.add_argument("--output", required=True, help="Output JSONL dataset")
    t.add_argument("--templates", required=True, help="Template YAML file")
    t.add_argument("--experiment", required=True, help="Name of template to use")

    args = parser.parse_args()
    if args.command == "transform":
        transform_dataset(args.input, args.output, args.templates, args.experiment)


if __name__ == "__main__":
    main()
