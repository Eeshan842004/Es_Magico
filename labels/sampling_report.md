# Label sample

- seed 2026; 60 items; per version {'v1': 30, 'v2': 30}
- drawn from 142 summaries scored by both judges and absent from the excluded earlier sample
- all held-out; one per conversation and version; order shuffled; version label hidden
- quick option, fixed before any round-2 label existed: 20 of these (10 per prompt, 20 conversations), `python -X utf8 src/label_tool.py --quick`
- v2's layout is recognisable, so blinding to version is imperfect
