importScripts("https://cdn.jsdelivr.net/pyodide/v0.29.3/full/pyodide.js");

function sendPatch(patch, buffers, msg_id) {
  self.postMessage({
    type: 'patch',
    patch: patch,
    buffers: buffers
  })
}

async function startApplication() {
  console.log("Loading pyodide...");
  self.postMessage({type: 'status', msg: 'Loading pyodide'})
  self.pyodide = await loadPyodide();
  self.pyodide.globals.set("sendPatch", sendPatch);
  console.log("Loaded pyodide!");
  const data_archives = [];
  for (const archive of data_archives) {
    let zipResponse = await fetch(archive);
    let zipBinary = await zipResponse.arrayBuffer();
    self.postMessage({type: 'status', msg: `Unpacking ${archive}`})
    self.pyodide.unpackArchive(zipBinary, "zip");
  }
  await self.pyodide.loadPackage("micropip");
  self.postMessage({type: 'status', msg: `Installing environment`})
  try {
    await self.pyodide.runPythonAsync(`
      import micropip
      await micropip.install(['https://cdn.holoviz.org/panel/wheels/bokeh-3.9.0-py3-none-any.whl', 'https://cdn.holoviz.org/panel/1.8.10/dist/wheels/panel-1.8.10-py3-none-any.whl', 'pyodide-http', 'unimport']);
    `);
  } catch(e) {
    console.log(e)
    self.postMessage({
      type: 'status',
      msg: `Error while installing packages`
    });
  }
  console.log("Environment loaded!");
  self.postMessage({type: 'status', msg: 'Executing code'})
  try {
    const [docs_json, render_items, root_ids] = await self.pyodide.runPythonAsync(`\nimport asyncio\n\nfrom panel.io.pyodide import init_doc, write_doc\n\ninit_doc()\n\nimport traceback\n\nimport panel as pn\nfrom unimport.analyzers import MainAnalyzer\nfrom unimport.refactor import refactor_string\nfrom unimport.statement import Import\n\n# Editor stilleri \u2013 tutarli yukseklik\nEDITOR_HEIGHT = 420\n\n\ndef refactor(source: str) -> str:\n    with MainAnalyzer(source=source, include_star_import=True):\n        unused_imports = list(Import.get_unused_imports(include_star_import=True))\n\n    return refactor_string(source=source, unused_imports=unused_imports)\n\n\ndef run_refactor(source: str) -> pn.widgets.CodeEditor:\n    try:\n        refactored_source = refactor(source)\n        language = "python"\n    except Exception:\n        refactored_source = traceback.format_exc()\n        language = "text"\n\n    return pn.widgets.CodeEditor(\n        value=refactored_source,\n        language=language,\n        readonly=True,\n        height=EDITOR_HEIGHT,\n        theme="monokai",\n    )\n\n\npn.config.sizing_mode = "stretch_both"\npn.extension("codeeditor", design="material")\n\n\nexample_source_code = """\\\nimport os\nimport sys\nfrom pathlib import Path\n\nx = 1\nprint(x)\n"""\n\nsource_editor = pn.widgets.CodeEditor(\n    value=example_source_code,\n    language="python",\n    height=EDITOR_HEIGHT,\n    theme="chrome",\n)\nresult_editor = pn.bind(run_refactor, source_editor)\n\n\ndef clear_source(event):\n    source_editor.value = ""\n\n\n# Etiketler\nsource_label = pn.pane.Markdown(\n    "**Kaynak kod**",\n    margin=(0, 0, 4, 0),\n    styles={"font-size": "13px", "color": "var(--design-secondary-color, #666)"},\n)\nresult_label = pn.pane.Markdown(\n    "**Sonuc** (kullanilmayan import'lar kaldirildi)",\n    margin=(0, 0, 4, 0),\n    styles={"font-size": "13px", "color": "var(--design-secondary-color, #666)"},\n)\n\n# Arac butonlari\nclear_btn = pn.widgets.Button(\n    name="Temizle",\n    button_type="default",\n    width=90,\n)\nclear_btn.on_click(clear_source)\n\ndocs_btn = pn.widgets.Button(\n    name="Dokumantasyon",\n    button_type="primary",\n    width=130,\n)\ndocs_btn.js_on_click(code="window.open('https://unimport.hakancelik.dev')")\n\ngithub_btn = pn.widgets.Button(\n    name="GitHub",\n    button_type="primary",\n    width=100,\n)\ngithub_btn.js_on_click(code="window.open('https://github.com/hakancelikdev/unimport')")\n\ntoolbar = pn.Row(\n    clear_btn,\n    margin=(0, 0, 12, 0),\n    styles={"align-items": "center"},\n)\n\n# Ana icerik: iki sutun\nsource_column = pn.Column(\n    source_label,\n    source_editor,\n    margin=(0, 8, 0, 0),\n    styles={"flex": "1", "min-width": "280px"},\n)\nresult_column = pn.Column(\n    result_label,\n    result_editor,\n    margin=(0, 0, 0, 8),\n    styles={"flex": "1", "min-width": "280px"},\n)\n\neditors_row = pn.Row(\n    source_column,\n    result_column,\n    margin=(0, 0, 16, 0),\n    styles={"flex-wrap": "wrap"},\n)\n\n# Aciklama\nintro = pn.pane.Markdown(\n    "Kutuya Python kodu yazin veya yapistirin. Sagdaki panelde kullanilmayan "\n    "import'lar otomatik kaldirilmis hali gorunur.",\n    margin=(0, 0, 16, 0),\n    styles={"font-size": "14px", "opacity": "0.9"},\n)\n\nmain_content = pn.Column(\n    intro,\n    toolbar,\n    editors_row,\n    margin=(24, 24, 24, 24),\n    max_width=1200,\n    styles={"margin-left": "auto", "margin-right": "auto"},\n)\n\ntemplate = pn.template.MaterialTemplate(\n    title="Unimport Playground",\n    main=[main_content],\n    header_background="#1a1a2e",\n    header_color="#eee",\n)\n\n# Header'a link butonlari\ntemplate.header.append(\n    pn.Row(\n        docs_btn,\n        github_btn,\n        margin=(0, 12, 0, 0),\n        styles={"align-items": "center", "gap": "8px"},\n    )\n)\n\ntemplate.servable()\n\n\nawait write_doc()`)
    self.postMessage({
      type: 'render',
      docs_json: docs_json,
      render_items: render_items,
      root_ids: root_ids
    })
  } catch(e) {
    const traceback = `${e}`
    const tblines = traceback.split('\n')
    self.postMessage({
      type: 'status',
      msg: tblines[tblines.length-2]
    });
    throw e
  }
}

self.onmessage = async (event) => {
  const msg = event.data
  if (msg.type === 'rendered') {
    self.pyodide.runPythonAsync(`
    from panel.io.state import state
    from panel.io.pyodide import _link_docs_worker

    _link_docs_worker(state.curdoc, sendPatch, setter='js')
    `)
  } else if (msg.type === 'patch') {
    self.pyodide.globals.set('patch', msg.patch)
    self.pyodide.runPythonAsync(`
    from panel.io.pyodide import _convert_json_patch
    state.curdoc.apply_json_patch(_convert_json_patch(patch), setter='js')
    `)
    self.postMessage({type: 'idle'})
  } else if (msg.type === 'location') {
    self.pyodide.globals.set('location', msg.location)
    self.pyodide.runPythonAsync(`
    import json
    from panel.io.state import state
    from panel.util import edit_readonly
    if state.location:
        loc_data = json.loads(location)
        with edit_readonly(state.location):
            state.location.param.update({
                k: v for k, v in loc_data.items() if k in state.location.param
            })
    `)
  }
}

startApplication()