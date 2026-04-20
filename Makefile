BUMP     = patch  # patch | minor | major
REPO     = yeshwanth-divami/divami-skills-dist
THIS_REPO = yeshwanth-divami/divami-agents
TEAM_FILE = divami-team.csv

.PHONY: venv pack publish add-collabs setup-tui

# Usage: make add-collabs [TEAM_FILE=other.txt] [THIS_REPO=owner/repo]
add-collabs:
	@test -f $(TEAM_FILE) || (echo "$(TEAM_FILE) not found"; exit 1)
	@while IFS=',' read -r email username_col || [ -n "$$email" ]; do \
		[ -z "$$email" ] && continue; \
		if [ -n "$$username_col" ]; then \
			username="$$username_col"; \
		else \
			case "$$email" in \
				*@*) username=$$(gh api "search/users?q=$$email+in:email" --jq '.items[0].login // empty' 2>/dev/null) ;; \
				*)   username="$$email" ;; \
			esac; \
		fi; \
		if [ -z "$$username" ]; then \
			echo "  $$email -> no GitHub username, skipping"; \
			continue; \
		fi; \
		echo "Adding $$username ($$email) ..."; \
		gh api --method PUT repos/$(THIS_REPO)/collaborators/$$username \
			-f permission=push --silent && echo "  ok" || echo "  failed"; \
	done < $(TEAM_FILE)

venv:
	uv venv .venv --clear
	uv pip install --python .venv textual build twine tomli

pack:
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

# Bootstrap this repo with uv, install divami-agents globally, unpack the skill pack, and open the TUI.
setup-tui:
	brew list uv >/dev/null 2>&1 || brew install uv
	uv tool install --reinstall .
	divami-agents unpack
	divami-agents tui
