BUMP     = patch  # patch | minor | major
REPO     = yeshwanth-divami/divami-skills-dist

.PHONY: venv pack publish

venv:
	uv venv .venv --clear
	uv pip install --python .venv pyzipper textual build twine tomli

pack:
	DIVAMI_AGENTS_PASSWORD=$${DIVAMI_AGENTS_PASSWORD:?DIVAMI_AGENTS_PASSWORD is required} \
		.venv/bin/python scripts/pack.py

# Usage: make publish [BUMP=minor]
publish: pack
	uv version --bump $(BUMP)
	VERSION=$$(grep '^version' pyproject.toml | head -1 | sed 's/.*"\(.*\)"$$/\1/'); \
	rm -rf dist/; \
	.venv/bin/python -m build; \
	.venv/bin/twine upload --repository divami dist/*.whl; \
	gh release create "v$$VERSION" --title "v$$VERSION" --notes "" \
		--repo $(REPO) \
		"src/divami_skills/skills.zip#skills.zip"
