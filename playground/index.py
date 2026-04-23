import traceback

import panel as pn
from unimport.analyzers import MainAnalyzer
from unimport.refactor import refactor_string
from unimport.statement import Import

# Editor stilleri – tutarli yukseklik
EDITOR_HEIGHT = 420


def refactor(source: str) -> str:
    with MainAnalyzer(source=source, include_star_import=True):
        unused_imports = list(Import.get_unused_imports(include_star_import=True))

    return refactor_string(source=source, unused_imports=unused_imports)


def run_refactor(source: str) -> pn.widgets.CodeEditor:
    try:
        refactored_source = refactor(source)
        language = "python"
    except Exception:
        refactored_source = traceback.format_exc()
        language = "text"

    return pn.widgets.CodeEditor(
        value=refactored_source,
        language=language,
        readonly=True,
        height=EDITOR_HEIGHT,
        theme="monokai",
    )


pn.config.sizing_mode = "stretch_both"
pn.extension("codeeditor", design="material")


example_source_code = """\
import os
import sys
from pathlib import Path

x = 1
print(x)
"""

source_editor = pn.widgets.CodeEditor(
    value=example_source_code,
    language="python",
    height=EDITOR_HEIGHT,
    theme="chrome",
)
result_editor = pn.bind(run_refactor, source_editor)


def clear_source(event):
    source_editor.value = ""


# Etiketler
source_label = pn.pane.Markdown(
    "**Kaynak kod**",
    margin=(0, 0, 4, 0),
    styles={"font-size": "13px", "color": "var(--design-secondary-color, #666)"},
)
result_label = pn.pane.Markdown(
    "**Sonuc** (kullanilmayan import'lar kaldirildi)",
    margin=(0, 0, 4, 0),
    styles={"font-size": "13px", "color": "var(--design-secondary-color, #666)"},
)

# Arac butonlari
clear_btn = pn.widgets.Button(
    name="Temizle",
    button_type="default",
    width=90,
)
clear_btn.on_click(clear_source)

docs_btn = pn.widgets.Button(
    name="Dokumantasyon",
    button_type="primary",
    width=130,
)
docs_btn.js_on_click(code="window.open('https://unimport.hakancelik.dev')")

github_btn = pn.widgets.Button(
    name="GitHub",
    button_type="primary",
    width=100,
)
github_btn.js_on_click(code="window.open('https://github.com/hakancelikdev/unimport')")

toolbar = pn.Row(
    clear_btn,
    margin=(0, 0, 12, 0),
    styles={"align-items": "center"},
)

# Ana icerik: iki sutun
source_column = pn.Column(
    source_label,
    source_editor,
    margin=(0, 8, 0, 0),
    styles={"flex": "1", "min-width": "280px"},
)
result_column = pn.Column(
    result_label,
    result_editor,
    margin=(0, 0, 0, 8),
    styles={"flex": "1", "min-width": "280px"},
)

editors_row = pn.Row(
    source_column,
    result_column,
    margin=(0, 0, 16, 0),
    styles={"flex-wrap": "wrap"},
)

# Aciklama
intro = pn.pane.Markdown(
    "Kutuya Python kodu yazin veya yapistirin. Sagdaki panelde kullanilmayan "
    "import'lar otomatik kaldirilmis hali gorunur.",
    margin=(0, 0, 16, 0),
    styles={"font-size": "14px", "opacity": "0.9"},
)

main_content = pn.Column(
    intro,
    toolbar,
    editors_row,
    margin=(24, 24, 24, 24),
    max_width=1200,
    styles={"margin-left": "auto", "margin-right": "auto"},
)

template = pn.template.MaterialTemplate(
    title="Unimport Playground",
    main=[main_content],
    header_background="#1a1a2e",
    header_color="#eee",
)

# Header'a link butonlari
template.header.append(
    pn.Row(
        docs_btn,
        github_btn,
        margin=(0, 12, 0, 0),
        styles={"align-items": "center", "gap": "8px"},
    )
)

template.servable()
