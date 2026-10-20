from __future__ import annotations

import argparse
import json
from typing import Any

from alfresco_research.settings import load_settings
from alfresco_research.tools import create_alfresco_tools_by_name


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verify that the OpenDMA Alfresco endpoint and tools are reachable.",
    )
    parser.add_argument(
        "--site-short-name",
        default="project-apollo",
        help="Alfresco site short name expected in alfresco_list_sites output.",
    )
    return parser


def _tool_payload(result: Any) -> Any:
    if isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return result
    return result


def _site_short_name(site: dict[str, Any]) -> str:
    return str(site.get("short_name") or site.get("shortName") or site.get("id") or "")


def _site_title(site: dict[str, Any]) -> str:
    return str(site.get("title") or site.get("name") or _site_short_name(site))


def main() -> None:
    args = build_parser().parse_args()
    expected_short_name = args.site_short_name.strip()
    settings = load_settings()
    tools = create_alfresco_tools_by_name(settings)

    print(f"OpenDMA endpoint: {settings.opendma_alfresco_endpoint}")
    print(f"Repository: {settings.opendma_alfresco_repository_id}")
    print()
    print("Tools:")
    for name in sorted(tools):
        print(f"- {name}")

    list_sites = tools.get("alfresco_list_sites")
    if list_sites is None:
        raise SystemExit("Smoke test failed: alfresco_list_sites tool is not available.")

    sites_payload = _tool_payload(list_sites.run())
    if not isinstance(sites_payload, list):
        raise SystemExit(
            "Smoke test failed: alfresco_list_sites returned an unexpected payload:\n"
            f"{sites_payload}"
        )

    print()
    print("Sites:")
    matching_site: dict[str, Any] | None = None
    for site in sites_payload:
        if not isinstance(site, dict):
            print(f"- {site}")
            continue
        short_name = _site_short_name(site)
        title = _site_title(site)
        root_folder_id = site.get("root_folder_id") or site.get("rootFolderId") or "?"
        print(f"- {short_name}: {title} [{root_folder_id}]")
        if short_name == expected_short_name:
            matching_site = site

    if matching_site is None:
        raise SystemExit(
            f"Smoke test failed: site '{expected_short_name}' was not returned by "
            "alfresco_list_sites."
        )

    search_tool = tools.get("opendma_search")
    root_folder_id = matching_site.get("root_folder_id")
    if search_tool is not None and root_folder_id:
        print()
        print(f"Search check in {expected_short_name}:")
        search_result = search_tool.run(
            full_text="risk",
            in_folder=str(root_folder_id),
            include_subfolder_in_folder=True,
            included_metadata=["opendma:Title"],
        )
        print(search_result)

    print()
    print("Smoke test passed.")


if __name__ == "__main__":
    main()
