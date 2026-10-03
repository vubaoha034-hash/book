"""Read a pinned historical tree for validation; never restore the live checkout."""
from __future__ import annotations
import atexit,io,subprocess,tempfile,zipfile
from pathlib import Path
_cache={}
def frozen_tree(repository:Path,head:str)->Path:
    key=(str(repository.resolve()),head)
    if key in _cache:return _cache[key][1]
    raw=subprocess.check_output(['git','archive','--format=zip',head],cwd=repository)
    temporary=tempfile.TemporaryDirectory(prefix='novel-pinned-history-');root=Path(temporary.name).resolve()
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        for name in archive.namelist():
            p=root/name
            if not p.resolve().is_relative_to(root) or '\\' in name:raise ValueError('UNSAFE_HISTORICAL_ARCHIVE_PATH')
            if name.endswith('/'):p.mkdir(parents=True,exist_ok=True)
            else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(archive.read(name))
    _cache[key]=(temporary,root);atexit.register(temporary.cleanup)
    return root
def historical_test_data(repository:Path)->Path:
    import json
    state=json.loads((repository/'state/project_state.json').read_bytes())
    route=state.get('story_replacement_trial')
    return frozen_tree(repository,route['source_head']) if route else repository
