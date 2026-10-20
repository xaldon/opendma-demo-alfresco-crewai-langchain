from __future__ import annotations

import argparse

from alfresco_research.crew import AlfrescoResearchCrew


DEFAULT_QUESTION = (
    "Review the Project Apollo documents and identify the three most important "
    "project risks. Cite the documents supporting each finding."
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a CrewAI risk briefing over documents stored in Alfresco.",
    )
    parser.add_argument(
        "question",
        nargs="?",
        default=DEFAULT_QUESTION,
        help="Question to ask the crew. Defaults to the Project Apollo risk question.",
    )
    parser.add_argument(
        "--site-short-name",
        default="",
        help=(
            "Optional Alfresco site short name. If omitted, the researcher agent "
            "uses alfresco_list_sites to discover the site from the question."
        ),
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    inputs = {
        "question": args.question,
        "site_short_name": args.site_short_name.strip(),
    }
    result = AlfrescoResearchCrew().crew().kickoff(inputs=inputs)
    print(result)


if __name__ == "__main__":
    main()

