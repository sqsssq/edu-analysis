#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

if [[ -d "templates/project" && -f "VERSION" ]]; then
  mode="template"
else
  mode="instance"
fi

usage() {
  cat <<'EOF'
Usage: bash scripts/verify.sh [--template|--instance|--strict-instance]

Modes:
  --template          Verify the HarnessWeaver source repository and project scaffold.
  --instance          Verify a generated project. Placeholder tokens fail.
  --strict-instance   Verify an implementation-ready project. Placeholders and TODO markers fail.

Default: detect template or generated-project mode from the repository structure.
EOF
}

for arg in "$@"; do
  case "$arg" in
    --template) mode="template" ;;
    --instance) mode="instance" ;;
    --strict-instance) mode="strict-instance" ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $arg"
      usage
      exit 1
      ;;
  esac
done

echo "HarnessWeaver verification"
echo "=========================="
echo "Mode: $mode"

project_required_files=(
  "AGENTS.md"
  ".gitignore"
  ".harnessweaver-version"
  "CHANGELOG.md"
  "LICENSE"
  "README.md"
  "README.zh-CN.md"
  "config/init-project.example.env"
  "docs/design.md"
  "docs/domain/PROJECT_RULES.md"
  "docs/prd/00-product-brief.md"
  "docs/prd/01-mvp-scope.md"
  "docs/prd/02-user-flows.md"
  "docs/prd/03-feature-design.md"
  "docs/prd/04-content-model.md"
  "docs/prd/05-ui-states.md"
  "docs/prd/06-acceptance-criteria.md"
  "docs/prd/07-task-breakdown.md"
  "docs/prd/08-open-questions.md"
  "docs/prd/09-decision-log.md"
  "docs/tasks/README.md"
  "docs/tasks/TASK_TEMPLATE.md"
  "docs/meta/PRD_GENERATOR.md"
  "docs/meta/TASK_BREAKDOWN_GUIDE.md"
  "docs/meta/TASK_EXECUTION_GUIDE.md"
  "docs/meta/CHANGE_REQUEST_GUIDE.md"
  "docs/meta/VERIFICATION_GUIDE.md"
  "docs/meta/DIFF_REVIEW_GUIDE.md"
  "docs/meta/HUMAN_HANDOFF_GUIDE.md"
  "docs/meta/COMMIT_GUIDE.md"
  "docs/meta/UPGRADE_GUIDE.md"
  "docs/harness/00-harness-overview.md"
  "docs/harness/01-verification-matrix.md"
  "docs/harness/02-agent-failure-patterns.md"
  "docs/harness/03-architecture-fitness-rules.md"
  "docs/harness/04-quality-rules.md"
  "docs/harness/05-stage-checklists.md"
  "docs/harness/06-strict-readiness.md"
  "docs/harness/stages/stage-0-framework.md"
  "docs/harness/stages/stage-1-fixture-schema.md"
  "docs/harness/stages/stage-2-logic.md"
  "docs/harness/stages/stage-3-product-ui.md"
  "docs/harness/stages/stage-4-continuous.md"
)

missing=0
if [[ "$mode" == "template" ]]; then
  source_required_files=(
    "AGENTS.md"
    "README.md"
    "README.zh-CN.md"
    "CHANGELOG.md"
    "LICENSE"
    "VERSION"
    "scripts/init-project.sh"
    "scripts/verify.sh"
    "scripts/test-template.sh"
    "skills/harness-weaver/SKILL.md"
  )
  for file in "${source_required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
      echo "Missing required source file: $file"
      missing=1
    fi
  done
  for file in "${project_required_files[@]}"; do
    if [[ ! -f "templates/project/$file" ]]; then
      echo "Missing generated-project template file: templates/project/$file"
      missing=1
    fi
  done
else
  for file in "${project_required_files[@]}" "scripts/init-project.sh" "scripts/verify.sh"; do
    if [[ ! -f "$file" ]]; then
      echo "Missing required project file: $file"
      missing=1
    fi
  done
fi

if [[ "$missing" -ne 0 ]]; then
  exit 1
fi
echo "Required files exist."

for executable in scripts/verify.sh scripts/init-project.sh; do
  if [[ ! -x "$executable" ]]; then
    echo "$executable is not executable."
    exit 1
  fi
done
if [[ "$mode" == "template" && ! -x "scripts/test-template.sh" ]]; then
  echo "scripts/test-template.sh is not executable."
  exit 1
fi
echo "Required scripts are executable."

scan_text() {
  local pattern="$1"
  shift
  find "$@" -type f \
    \( -name '*.md' -o -name '*.sh' -o -name '*.env' -o -name '*.txt' \
       -o -name '*.json' -o -name '*.toml' -o -name '*.yaml' -o -name '*.yml' \
       -o -name 'VERSION' -o -name '.harnessweaver-version' -o -name '.gitignore' \
       -o -name 'LICENSE' \) \
    -exec grep -I -n -E "$pattern" {} +
}

source_scan=(AGENTS.md README.md README.zh-CN.md config docs scripts)
if [[ "$mode" == "template" ]]; then
  source_scan+=(templates)
fi
source_terms='BioQues[t]|QuestLa[b]|QuestWeave[r]|R[B]M|P[r]oposal Analytic[s]|P[S] recommendation'
if scan_text "$source_terms" "${source_scan[@]}"; then
  echo "Found source-project-specific terms. Please review the matches above."
  exit 1
fi
echo "No source-project-specific terms found."

if [[ "$mode" != "template" ]]; then
  identity_leakage='# HarnessWeaver|docs/assets/harnessweaver-hero|templates/project|skills/harness-weaver|maintaining HarnessWeaver|HarnessWeaver repository maintenance'
  if scan_text "$identity_leakage" AGENTS.md README.md README.zh-CN.md docs; then
    echo "Generated project contains HarnessWeaver repository identity leakage."
    exit 1
  fi
  echo "No HarnessWeaver repository identity leakage found."
fi

if [[ "$mode" == "template" ]]; then
  if [[ ! -e ".agents/skills/harness-weaver/SKILL.md" ]]; then
    echo "Repository skill is not discoverable at .agents/skills/harness-weaver."
    exit 1
  fi
  echo "Repository skill discovery path is valid."
fi

placeholder_pattern='\{[A-Z][A-Z0-9_]*\}'
if [[ "$mode" == "instance" || "$mode" == "strict-instance" ]]; then
  if scan_text "$placeholder_pattern" AGENTS.md README.md README.zh-CN.md docs; then
    echo "Instance mode does not allow unresolved placeholder tokens."
    exit 1
  fi
  echo "No unresolved placeholder tokens found."
else
  placeholder_matches="$(scan_text "$placeholder_pattern" templates/project || true)"
  if [[ -n "$placeholder_matches" ]]; then
    placeholder_count="$(printf '%s\n' "$placeholder_matches" | wc -l | tr -d ' ')"
  else
    placeholder_count=0
  fi
  echo "Template placeholder tokens allowed: $placeholder_count matching lines found."
fi

if [[ "$mode" == "strict-instance" ]]; then
  todo_matches="$(mktemp)"
  if scan_text 'TODO:' AGENTS.md README.md README.zh-CN.md docs > "$todo_matches"; then
    cat "$todo_matches"
    echo
    echo "Strict instance TODO summary:"
    cut -d ':' -f 1 "$todo_matches" | sort | uniq -c | awk '{print "- " $2 ": " $1}'
    rm -f "$todo_matches"
    echo "Strict instance mode does not allow TODO markers."
    exit 1
  fi
  rm -f "$todo_matches"
  echo "No TODO markers found."
fi

reference_root="."
reference_scan=(AGENTS.md README.md README.zh-CN.md docs)
if [[ "$mode" == "template" ]]; then
  reference_root="templates/project"
  reference_scan=(templates/project/AGENTS.md templates/project/README.md templates/project/README.zh-CN.md templates/project/docs)
fi

path_failed=0
while IFS= read -r ref; do
  [[ -z "$ref" ]] && continue
  [[ "$ref" == *"..."* ]] && continue
  [[ "$ref" == *"*"* ]] && continue
  [[ "$ref" == *"{"* ]] && continue
  [[ "$ref" == *" "* ]] && continue
  candidate="$reference_root/$ref"
  if [[ "$ref" == scripts/* && "$mode" == "template" ]]; then
    candidate="$ref"
  fi
  if [[ "$ref" == */ ]]; then
    if [[ ! -d "${candidate%/}" ]]; then
      echo "Referenced directory does not exist: $ref"
      path_failed=1
    fi
  elif [[ ! -e "$candidate" ]]; then
    echo "Referenced file does not exist: $ref"
    path_failed=1
  fi
done < <(
  scan_text '`(AGENTS\.md|README[^`]*\.md|config/[^`]+|docs/[^`]+|scripts/[^`]+)`' "${reference_scan[@]}" 2>/dev/null |
    sed -E 's/^[^:]+:[0-9]+://' |
    grep -E -o '`(AGENTS\.md|README[^`]*\.md|config/[^`]+|docs/[^`]+|scripts/[^`]+)`' |
    sed 's/^`//; s/`$//' |
    sort -u
)

if [[ "$path_failed" -ne 0 ]]; then
  echo "Markdown path reference check failed."
  exit 1
fi

echo "Markdown path references are valid."
echo "HarnessWeaver $mode verification passed."
