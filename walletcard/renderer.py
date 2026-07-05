"""Render wallet-card HTML to PDF via WeasyPrint."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from weasyprint import CSS, HTML

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent

TEMPLATE_DIR = PROJECT_ROOT / "templates"
STATIC_DIR = PROJECT_ROOT / "static"
CSS_PATH = STATIC_DIR / "card.css"


def render_card(data: dict, output_path: str | Path) -> None:
    """Render a wallet-card PDF from the given data dict.

    Parameters
    ----------
    data : dict
        Template context with keys:
            - title: str
            - exchange_rate_text: str
            - generated_date: str
            - rows: list[dict]  each with keys "local" and "usd"
    output_path : str | Path
        Destination for the generated PDF.
    """
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template("card.html")

    html_str = template.render(**data)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    HTML(string=html_str).write_pdf(
        str(output_path),
        stylesheets=[CSS(filename=str(CSS_PATH))],
    )
