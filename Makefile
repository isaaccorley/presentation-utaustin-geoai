.PHONY: install serve check build clean

install:
	bun install
	uv sync --locked --all-groups

serve:
	bun run dev

check:
	bun run lint:fix
	bun run typecheck
	uv run pre-commit run --all-files

build:
	bun run build

clean:
	rm -rf .next out
