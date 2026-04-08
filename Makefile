PASSWORD = test123
BUMP     = patch

.PHONY: venv pack publish

venv:
	uv venv .venv --clear
	uv pip install --python .venv pyzipper textual build twine tomli

pack:
	.venv/bin/python scripts/pack.py --password $(PASSWORD)

# Pack the zip, build the distribution, then upload to PyPI via the [divami] profile
publish: pack
	.venv/bin/python -m build
	.venv/bin/twine upload --repository divami dist/*
