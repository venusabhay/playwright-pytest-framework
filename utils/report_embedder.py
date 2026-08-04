from pathlib import Path

from config.settings import SCREENSHOT_DIR


def embed_failure_screenshots(report_path: str | Path, items: list) -> None:
    report_path = Path(report_path)
    if not report_path.exists():
        return

    html = report_path.read_text(encoding="utf-8")
    assets_dir = report_path.parent / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    screenshot_files = sorted(SCREENSHOT_DIR.glob("*.png")) if SCREENSHOT_DIR.exists() else []
    for screenshot_file in screenshot_files:
        asset_path = assets_dir / screenshot_file.name
        if not asset_path.exists():
            asset_path.write_bytes(screenshot_file.read_bytes())

        marker = (
            '<div style="margin-top: 16px; padding: 12px; border: 1px solid #d0d7de; '
            'border-radius: 6px; background: #f6f8fa;">'
            '<strong style="display: block; margin-bottom: 8px;">Failure Screenshot</strong>'
            f'<img src="assets/{asset_path.name}" alt="failure screenshot" '
            'style="max-width: 100%; border: 1px solid #d0d7de;" />'
            '</div>'
        )

        if marker not in html:
            html = html.replace("</body>", f"{marker}\n</body>", 1)

    report_path.write_text(html, encoding="utf-8")
