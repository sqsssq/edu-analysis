#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  bash scripts/init-project.sh \
    --project-name "Project Name" \
    --domain "project domain" \
    --primary-user "primary user" \
    --mvp-focus "MVP focus"

Optional:
  --config path/to/init-project.env
  --target path/to/new-project
  --dry-run
  --generic-failure-mode "generic app drift"
  --primary-user-goal "primary user goal"
  --content-review-status-rule "review status rule"
  --feedback-reasoning-rule "feedback reasoning rule"

Run from the HarnessWeaver repository with --target to create a clean project.
Inside a generated project, omit --target to update placeholders in place.
Config files use declarative HW_* key-value pairs and are never executed.
See config/init-project.example.env.
Run `bash scripts/verify.sh --instance` after initialization.
Run `bash scripts/verify.sh --strict-instance` when the project is ready for task execution.
EOF
}

require_value() {
  local option="$1"
  local value="${2-}"
  if [[ -z "$value" || "$value" == --* ]]; then
    echo "Missing value for $option"
    usage
    exit 1
  fi
}

missing_required=0
check_required() {
  local name="$1"
  local value="$2"
  if [[ -z "$value" ]]; then
    echo "Missing required value: $name"
    missing_required=1
  fi
}

print_plan() {
  cat <<EOF
HarnessWeaver initialization plan
=================================
Project name: $project_name
Domain: $domain
Primary user: $primary_user
MVP focus: $mvp_focus
Non-goals: $non_goals
Project summary: $project_summary
Generic failure mode: $generic_failure_mode
Primary user goal: $primary_user_goal
Target: ${target_dir:-current generated project}

Run without --dry-run to generate or update AGENTS.md, README files, and docs/*.md.
EOF
}

allowed_config_key() {
  case "$1" in
    HW_PROJECT_NAME|HW_DOMAIN|HW_PRIMARY_USER|HW_MVP_FOCUS|HW_NON_GOALS|HW_PROJECT_SUMMARY|\
    HW_PRIMARY_USER_PROBLEM|HW_PRODUCT_PROMISE|HW_SUCCESS_CRITERION_1|HW_SUCCESS_CRITERION_2|\
    HW_SUCCESS_CRITERION_3|HW_IN_SCOPE_1|HW_IN_SCOPE_2|HW_IN_SCOPE_3|HW_OUT_OF_SCOPE_1|\
    HW_OUT_OF_SCOPE_2|HW_OUT_OF_SCOPE_3|HW_MVP_LOOP_STEP_1|HW_MVP_LOOP_STEP_2|HW_MVP_LOOP_STEP_3|\
    HW_MVP_LOOP_STEP_4|HW_PRIMARY_FLOW_STEP_1|HW_PRIMARY_FLOW_STEP_2|HW_PRIMARY_FLOW_STEP_3|\
    HW_PRIMARY_FLOW_STEP_4|HW_EDGE_FLOW_1|HW_EDGE_FLOW_2|HW_EDGE_FLOW_3|HW_CORE_LOOP_STEP_1|\
    HW_CORE_LOOP_STEP_2|HW_CORE_LOOP_STEP_3|HW_CORE_LOOP_STEP_4|HW_FEATURE_PRINCIPLE_1|\
    HW_FEATURE_PRINCIPLE_2|HW_FEATURE_PRINCIPLE_3|HW_FIELD_1|HW_FIELD_2|HW_FIELD_3|\
    HW_PRODUCT_QUESTION_1|HW_PRODUCT_QUESTION_2|HW_PRODUCT_QUESTION_3|HW_TECHNICAL_QUESTION_1|\
    HW_TECHNICAL_QUESTION_2|HW_TECHNICAL_QUESTION_3|HW_GENERIC_FAILURE_MODE|HW_PRIMARY_USER_GOAL|\
    HW_CONTENT_REVIEW_STATUS_RULE|HW_FEEDBACK_REASONING_RULE)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

load_config() {
  local file="$1"
  local line
  local trimmed
  local key
  local value
  if [[ ! -f "$file" ]]; then
    echo "Config file does not exist: $file"
    exit 1
  fi

  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%$'\r'}"
    trimmed="$(printf '%s' "$line" | sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//')"
    [[ -z "$trimmed" || "$trimmed" == \#* ]] && continue

    if [[ ! "$trimmed" =~ ^(HW_[A-Z0-9_]+)=(.*)$ ]]; then
      echo "Invalid config line in $file: $line"
      echo "Use one HW_NAME=value assignment per line."
      exit 1
    fi

    key="${BASH_REMATCH[1]}"
    value="${BASH_REMATCH[2]}"
    if ! allowed_config_key "$key"; then
      echo "Unknown config key in $file: $key"
      exit 1
    fi

    if [[ "$value" == \"* ]]; then
      if [[ "$value" != *\" || ${#value} -lt 2 ]]; then
        echo "Unterminated double-quoted value for $key in $file"
        exit 1
      fi
      value="${value:1:${#value}-2}"
    elif [[ "$value" == \'* ]]; then
      if [[ "$value" != *\' || ${#value} -lt 2 ]]; then
        echo "Unterminated single-quoted value for $key in $file"
        exit 1
      fi
      value="${value:1:${#value}-2}"
    elif [[ "$value" =~ [[:space:]] ]]; then
      echo "Values containing spaces must be quoted for $key in $file"
      exit 1
    fi

    printf -v "$key" '%s' "$value"
  done < "$file"
}

apply_config_defaults() {
  project_name="${HW_PROJECT_NAME:-$project_name}"
  domain="${HW_DOMAIN:-$domain}"
  primary_user="${HW_PRIMARY_USER:-$primary_user}"
  mvp_focus="${HW_MVP_FOCUS:-$mvp_focus}"
  non_goals="${HW_NON_GOALS:-$non_goals}"
  project_summary="${HW_PROJECT_SUMMARY:-$project_summary}"
  primary_user_problem="${HW_PRIMARY_USER_PROBLEM:-$primary_user_problem}"
  product_promise="${HW_PRODUCT_PROMISE:-$product_promise}"
  success_criterion_1="${HW_SUCCESS_CRITERION_1:-$success_criterion_1}"
  success_criterion_2="${HW_SUCCESS_CRITERION_2:-$success_criterion_2}"
  success_criterion_3="${HW_SUCCESS_CRITERION_3:-$success_criterion_3}"
  in_scope_1="${HW_IN_SCOPE_1:-$in_scope_1}"
  in_scope_2="${HW_IN_SCOPE_2:-$in_scope_2}"
  in_scope_3="${HW_IN_SCOPE_3:-$in_scope_3}"
  out_of_scope_1="${HW_OUT_OF_SCOPE_1:-$out_of_scope_1}"
  out_of_scope_2="${HW_OUT_OF_SCOPE_2:-$out_of_scope_2}"
  out_of_scope_3="${HW_OUT_OF_SCOPE_3:-$out_of_scope_3}"
  mvp_loop_step_1="${HW_MVP_LOOP_STEP_1:-$mvp_loop_step_1}"
  mvp_loop_step_2="${HW_MVP_LOOP_STEP_2:-$mvp_loop_step_2}"
  mvp_loop_step_3="${HW_MVP_LOOP_STEP_3:-$mvp_loop_step_3}"
  mvp_loop_step_4="${HW_MVP_LOOP_STEP_4:-$mvp_loop_step_4}"
  primary_flow_step_1="${HW_PRIMARY_FLOW_STEP_1:-$primary_flow_step_1}"
  primary_flow_step_2="${HW_PRIMARY_FLOW_STEP_2:-$primary_flow_step_2}"
  primary_flow_step_3="${HW_PRIMARY_FLOW_STEP_3:-$primary_flow_step_3}"
  primary_flow_step_4="${HW_PRIMARY_FLOW_STEP_4:-$primary_flow_step_4}"
  edge_flow_1="${HW_EDGE_FLOW_1:-$edge_flow_1}"
  edge_flow_2="${HW_EDGE_FLOW_2:-$edge_flow_2}"
  edge_flow_3="${HW_EDGE_FLOW_3:-$edge_flow_3}"
  core_loop_step_1="${HW_CORE_LOOP_STEP_1:-$core_loop_step_1}"
  core_loop_step_2="${HW_CORE_LOOP_STEP_2:-$core_loop_step_2}"
  core_loop_step_3="${HW_CORE_LOOP_STEP_3:-$core_loop_step_3}"
  core_loop_step_4="${HW_CORE_LOOP_STEP_4:-$core_loop_step_4}"
  feature_principle_1="${HW_FEATURE_PRINCIPLE_1:-$feature_principle_1}"
  feature_principle_2="${HW_FEATURE_PRINCIPLE_2:-$feature_principle_2}"
  feature_principle_3="${HW_FEATURE_PRINCIPLE_3:-$feature_principle_3}"
  field_1="${HW_FIELD_1:-$field_1}"
  field_2="${HW_FIELD_2:-$field_2}"
  field_3="${HW_FIELD_3:-$field_3}"
  product_question_1="${HW_PRODUCT_QUESTION_1:-$product_question_1}"
  product_question_2="${HW_PRODUCT_QUESTION_2:-$product_question_2}"
  product_question_3="${HW_PRODUCT_QUESTION_3:-$product_question_3}"
  technical_question_1="${HW_TECHNICAL_QUESTION_1:-$technical_question_1}"
  technical_question_2="${HW_TECHNICAL_QUESTION_2:-$technical_question_2}"
  technical_question_3="${HW_TECHNICAL_QUESTION_3:-$technical_question_3}"
  generic_failure_mode="${HW_GENERIC_FAILURE_MODE:-$generic_failure_mode}"
  primary_user_goal="${HW_PRIMARY_USER_GOAL:-$primary_user_goal}"
  content_review_status_rule="${HW_CONTENT_REVIEW_STATUS_RULE:-$content_review_status_rule}"
  feedback_reasoning_rule="${HW_FEEDBACK_REASONING_RULE:-$feedback_reasoning_rule}"
}

project_name=""
domain=""
primary_user=""
mvp_focus=""
non_goals=""
project_summary=""
primary_user_problem=""
product_promise=""
success_criterion_1=""
success_criterion_2=""
success_criterion_3=""
in_scope_1=""
in_scope_2=""
in_scope_3=""
out_of_scope_1=""
out_of_scope_2=""
out_of_scope_3=""
mvp_loop_step_1=""
mvp_loop_step_2=""
mvp_loop_step_3=""
mvp_loop_step_4=""
primary_flow_step_1=""
primary_flow_step_2=""
primary_flow_step_3=""
primary_flow_step_4=""
edge_flow_1=""
edge_flow_2=""
edge_flow_3=""
core_loop_step_1=""
core_loop_step_2=""
core_loop_step_3=""
core_loop_step_4=""
feature_principle_1=""
feature_principle_2=""
feature_principle_3=""
field_1=""
field_2=""
field_3=""
product_question_1=""
product_question_2=""
product_question_3=""
technical_question_1=""
technical_question_2=""
technical_question_3=""
generic_failure_mode="a generic app"
primary_user_goal=""
content_review_status_rule="explicit review status"
feedback_reasoning_rule="why the result or recommendation matters"
dry_run=0
target_dir=""
config_file=""
source_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

args=("$@")
while [[ $# -gt 0 ]]; do
  case "$1" in
    --config)
      require_value "$1" "${2-}"
      config_file="$2"
      load_config "$2"
      shift 2
      ;;
    --target)
      require_value "$1" "${2-}"
      target_dir="$2"
      shift 2
      ;;
    --dry-run)
      shift
      ;;
    *)
      shift
      ;;
  esac
done

apply_config_defaults
set -- "${args[@]}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --config)
      require_value "$1" "${2-}"
      shift 2
      ;;
    --target)
      require_value "$1" "${2-}"
      shift 2
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    --project-name)
      require_value "$1" "${2-}"
      project_name="$2"
      shift 2
      ;;
    --domain)
      require_value "$1" "${2-}"
      domain="$2"
      shift 2
      ;;
    --primary-user)
      require_value "$1" "${2-}"
      primary_user="$2"
      shift 2
      ;;
    --mvp-focus)
      require_value "$1" "${2-}"
      mvp_focus="$2"
      shift 2
      ;;
    --generic-failure-mode)
      require_value "$1" "${2-}"
      generic_failure_mode="$2"
      shift 2
      ;;
    --primary-user-goal)
      require_value "$1" "${2-}"
      primary_user_goal="$2"
      shift 2
      ;;
    --content-review-status-rule)
      require_value "$1" "${2-}"
      content_review_status_rule="$2"
      shift 2
      ;;
    --feedback-reasoning-rule)
      require_value "$1" "${2-}"
      feedback_reasoning_rule="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1"
      usage
      exit 1
      ;;
  esac
done

check_required "HW_PROJECT_NAME or --project-name" "$project_name"
check_required "HW_DOMAIN or --domain" "$domain"
check_required "HW_PRIMARY_USER or --primary-user" "$primary_user"
check_required "HW_MVP_FOCUS or --mvp-focus" "$mvp_focus"

if [[ "$missing_required" -ne 0 ]]; then
  usage
  exit 1
fi

if [[ -z "$primary_user_goal" ]]; then
  primary_user_goal="$mvp_focus"
fi

non_goals="${non_goals:-TODO: define explicit non-goals}"
project_summary="${project_summary:-a $domain project}"
primary_user_problem="${primary_user_problem:-TODO: define the primary user problem}"
product_promise="${product_promise:-TODO: define the product promise}"
success_criterion_1="${success_criterion_1:-TODO: define success criterion 1}"
success_criterion_2="${success_criterion_2:-TODO: define success criterion 2}"
success_criterion_3="${success_criterion_3:-TODO: define success criterion 3}"
in_scope_1="${in_scope_1:-TODO: define in-scope item 1}"
in_scope_2="${in_scope_2:-TODO: define in-scope item 2}"
in_scope_3="${in_scope_3:-TODO: define in-scope item 3}"
out_of_scope_1="${out_of_scope_1:-TODO: define out-of-scope item 1}"
out_of_scope_2="${out_of_scope_2:-TODO: define out-of-scope item 2}"
out_of_scope_3="${out_of_scope_3:-TODO: define out-of-scope item 3}"
mvp_loop_step_1="${mvp_loop_step_1:-TODO: define MVP loop step 1}"
mvp_loop_step_2="${mvp_loop_step_2:-TODO: define MVP loop step 2}"
mvp_loop_step_3="${mvp_loop_step_3:-TODO: define MVP loop step 3}"
mvp_loop_step_4="${mvp_loop_step_4:-TODO: define MVP loop step 4}"
primary_flow_step_1="${primary_flow_step_1:-TODO: define primary flow step 1}"
primary_flow_step_2="${primary_flow_step_2:-TODO: define primary flow step 2}"
primary_flow_step_3="${primary_flow_step_3:-TODO: define primary flow step 3}"
primary_flow_step_4="${primary_flow_step_4:-TODO: define primary flow step 4}"
edge_flow_1="${edge_flow_1:-TODO: define edge flow 1}"
edge_flow_2="${edge_flow_2:-TODO: define edge flow 2}"
edge_flow_3="${edge_flow_3:-TODO: define edge flow 3}"
core_loop_step_1="${core_loop_step_1:-TODO: define core loop step 1}"
core_loop_step_2="${core_loop_step_2:-TODO: define core loop step 2}"
core_loop_step_3="${core_loop_step_3:-TODO: define core loop step 3}"
core_loop_step_4="${core_loop_step_4:-TODO: define core loop step 4}"
feature_principle_1="${feature_principle_1:-TODO: define feature principle 1}"
feature_principle_2="${feature_principle_2:-TODO: define feature principle 2}"
feature_principle_3="${feature_principle_3:-TODO: define feature principle 3}"
field_1="${field_1:-fieldOne}"
field_2="${field_2:-fieldTwo}"
field_3="${field_3:-fieldThree}"
product_question_1="${product_question_1:-TODO: define product question 1}"
product_question_2="${product_question_2:-TODO: define product question 2}"
product_question_3="${product_question_3:-TODO: define product question 3}"
technical_question_1="${technical_question_1:-TODO: define technical question 1}"
technical_question_2="${technical_question_2:-TODO: define technical question 2}"
technical_question_3="${technical_question_3:-TODO: define technical question 3}"

if [[ "$dry_run" -eq 1 ]]; then
  print_plan
  exit 0
fi

if [[ -n "$target_dir" ]]; then
  if [[ ! -d "$source_root/templates/project" ]]; then
    echo "Project template does not exist: $source_root/templates/project"
    exit 1
  fi
  if [[ -e "$target_dir" && ! -d "$target_dir" ]]; then
    echo "Target exists and is not a directory: $target_dir"
    exit 1
  fi
  if [[ -d "$target_dir" && -n "$(find "$target_dir" -mindepth 1 -maxdepth 1 -print -quit)" ]]; then
    echo "Target directory is not empty: $target_dir"
    exit 1
  fi

  mkdir -p "$target_dir"
  cp -R "$source_root/templates/project/." "$target_dir/"
  mkdir -p "$target_dir/scripts"
  cp "$source_root/scripts/init-project.sh" "$target_dir/scripts/init-project.sh"
  cp "$source_root/scripts/verify.sh" "$target_dir/scripts/verify.sh"
  chmod +x "$target_dir/scripts/init-project.sh" "$target_dir/scripts/verify.sh"
  work_root="$(cd "$target_dir" && pwd)"
  if [[ -n "$config_file" ]]; then
    cp "$config_file" "$work_root/init-project.env"
  fi
else
  work_root="$source_root"
  if [[ -d "$work_root/templates/project" && -f "$work_root/VERSION" ]]; then
    echo "Refusing to initialize the HarnessWeaver source repository in place."
    echo "Pass --target path/to/new-project."
    exit 1
  fi
fi

export HW_PROJECT_NAME="$project_name"
export HW_DOMAIN="$domain"
export HW_PRIMARY_USER="$primary_user"
export HW_MVP_FOCUS="$mvp_focus"
export HW_NON_GOALS="$non_goals"
export HW_PROJECT_SUMMARY="$project_summary"
export HW_PRIMARY_USER_PROBLEM="$primary_user_problem"
export HW_PRODUCT_PROMISE="$product_promise"
export HW_SUCCESS_CRITERION_1="$success_criterion_1"
export HW_SUCCESS_CRITERION_2="$success_criterion_2"
export HW_SUCCESS_CRITERION_3="$success_criterion_3"
export HW_IN_SCOPE_1="$in_scope_1"
export HW_IN_SCOPE_2="$in_scope_2"
export HW_IN_SCOPE_3="$in_scope_3"
export HW_OUT_OF_SCOPE_1="$out_of_scope_1"
export HW_OUT_OF_SCOPE_2="$out_of_scope_2"
export HW_OUT_OF_SCOPE_3="$out_of_scope_3"
export HW_MVP_LOOP_STEP_1="$mvp_loop_step_1"
export HW_MVP_LOOP_STEP_2="$mvp_loop_step_2"
export HW_MVP_LOOP_STEP_3="$mvp_loop_step_3"
export HW_MVP_LOOP_STEP_4="$mvp_loop_step_4"
export HW_PRIMARY_FLOW_STEP_1="$primary_flow_step_1"
export HW_PRIMARY_FLOW_STEP_2="$primary_flow_step_2"
export HW_PRIMARY_FLOW_STEP_3="$primary_flow_step_3"
export HW_PRIMARY_FLOW_STEP_4="$primary_flow_step_4"
export HW_EDGE_FLOW_1="$edge_flow_1"
export HW_EDGE_FLOW_2="$edge_flow_2"
export HW_EDGE_FLOW_3="$edge_flow_3"
export HW_CORE_LOOP_STEP_1="$core_loop_step_1"
export HW_CORE_LOOP_STEP_2="$core_loop_step_2"
export HW_CORE_LOOP_STEP_3="$core_loop_step_3"
export HW_CORE_LOOP_STEP_4="$core_loop_step_4"
export HW_FEATURE_PRINCIPLE_1="$feature_principle_1"
export HW_FEATURE_PRINCIPLE_2="$feature_principle_2"
export HW_FEATURE_PRINCIPLE_3="$feature_principle_3"
export HW_FIELD_1="$field_1"
export HW_FIELD_2="$field_2"
export HW_FIELD_3="$field_3"
export HW_PRODUCT_QUESTION_1="$product_question_1"
export HW_PRODUCT_QUESTION_2="$product_question_2"
export HW_PRODUCT_QUESTION_3="$product_question_3"
export HW_TECHNICAL_QUESTION_1="$technical_question_1"
export HW_TECHNICAL_QUESTION_2="$technical_question_2"
export HW_TECHNICAL_QUESTION_3="$technical_question_3"
export HW_GENERIC_FAILURE_MODE="$generic_failure_mode"
export HW_PRIMARY_USER_GOAL="$primary_user_goal"
export HW_CONTENT_REVIEW_STATUS_RULE="$content_review_status_rule"
export HW_FEEDBACK_REASONING_RULE="$feedback_reasoning_rule"

find "$work_root/AGENTS.md" "$work_root/README.md" "$work_root/README.zh-CN.md" "$work_root/docs" \
  -type f -name '*.md' -print0 |
  xargs -0 perl -0pi -e '
    s/\{PROJECT_NAME\}/$ENV{HW_PROJECT_NAME}/g;
    s/\{DOMAIN\}/$ENV{HW_DOMAIN}/g;
    s/\{PRIMARY_USER\}/$ENV{HW_PRIMARY_USER}/g;
    s/\{MVP_FOCUS\}/$ENV{HW_MVP_FOCUS}/g;
    s/\{NON_GOALS\}/$ENV{HW_NON_GOALS}/g;
    s/\{PROJECT_SUMMARY\}/$ENV{HW_PROJECT_SUMMARY}/g;
    s/\{PRIMARY_USER_PROBLEM\}/$ENV{HW_PRIMARY_USER_PROBLEM}/g;
    s/\{PRODUCT_PROMISE\}/$ENV{HW_PRODUCT_PROMISE}/g;
    s/\{SUCCESS_CRITERION_1\}/$ENV{HW_SUCCESS_CRITERION_1}/g;
    s/\{SUCCESS_CRITERION_2\}/$ENV{HW_SUCCESS_CRITERION_2}/g;
    s/\{SUCCESS_CRITERION_3\}/$ENV{HW_SUCCESS_CRITERION_3}/g;
    s/\{IN_SCOPE_1\}/$ENV{HW_IN_SCOPE_1}/g;
    s/\{IN_SCOPE_2\}/$ENV{HW_IN_SCOPE_2}/g;
    s/\{IN_SCOPE_3\}/$ENV{HW_IN_SCOPE_3}/g;
    s/\{OUT_OF_SCOPE_1\}/$ENV{HW_OUT_OF_SCOPE_1}/g;
    s/\{OUT_OF_SCOPE_2\}/$ENV{HW_OUT_OF_SCOPE_2}/g;
    s/\{OUT_OF_SCOPE_3\}/$ENV{HW_OUT_OF_SCOPE_3}/g;
    s/\{MVP_LOOP_STEP_1\}/$ENV{HW_MVP_LOOP_STEP_1}/g;
    s/\{MVP_LOOP_STEP_2\}/$ENV{HW_MVP_LOOP_STEP_2}/g;
    s/\{MVP_LOOP_STEP_3\}/$ENV{HW_MVP_LOOP_STEP_3}/g;
    s/\{MVP_LOOP_STEP_4\}/$ENV{HW_MVP_LOOP_STEP_4}/g;
    s/\{PRIMARY_FLOW_STEP_1\}/$ENV{HW_PRIMARY_FLOW_STEP_1}/g;
    s/\{PRIMARY_FLOW_STEP_2\}/$ENV{HW_PRIMARY_FLOW_STEP_2}/g;
    s/\{PRIMARY_FLOW_STEP_3\}/$ENV{HW_PRIMARY_FLOW_STEP_3}/g;
    s/\{PRIMARY_FLOW_STEP_4\}/$ENV{HW_PRIMARY_FLOW_STEP_4}/g;
    s/\{EDGE_FLOW_1\}/$ENV{HW_EDGE_FLOW_1}/g;
    s/\{EDGE_FLOW_2\}/$ENV{HW_EDGE_FLOW_2}/g;
    s/\{EDGE_FLOW_3\}/$ENV{HW_EDGE_FLOW_3}/g;
    s/\{CORE_LOOP_STEP_1\}/$ENV{HW_CORE_LOOP_STEP_1}/g;
    s/\{CORE_LOOP_STEP_2\}/$ENV{HW_CORE_LOOP_STEP_2}/g;
    s/\{CORE_LOOP_STEP_3\}/$ENV{HW_CORE_LOOP_STEP_3}/g;
    s/\{CORE_LOOP_STEP_4\}/$ENV{HW_CORE_LOOP_STEP_4}/g;
    s/\{FEATURE_PRINCIPLE_1\}/$ENV{HW_FEATURE_PRINCIPLE_1}/g;
    s/\{FEATURE_PRINCIPLE_2\}/$ENV{HW_FEATURE_PRINCIPLE_2}/g;
    s/\{FEATURE_PRINCIPLE_3\}/$ENV{HW_FEATURE_PRINCIPLE_3}/g;
    s/\{FIELD_1\}/$ENV{HW_FIELD_1}/g;
    s/\{FIELD_2\}/$ENV{HW_FIELD_2}/g;
    s/\{FIELD_3\}/$ENV{HW_FIELD_3}/g;
    s/\{PRODUCT_QUESTION_1\}/$ENV{HW_PRODUCT_QUESTION_1}/g;
    s/\{PRODUCT_QUESTION_2\}/$ENV{HW_PRODUCT_QUESTION_2}/g;
    s/\{PRODUCT_QUESTION_3\}/$ENV{HW_PRODUCT_QUESTION_3}/g;
    s/\{TECHNICAL_QUESTION_1\}/$ENV{HW_TECHNICAL_QUESTION_1}/g;
    s/\{TECHNICAL_QUESTION_2\}/$ENV{HW_TECHNICAL_QUESTION_2}/g;
    s/\{TECHNICAL_QUESTION_3\}/$ENV{HW_TECHNICAL_QUESTION_3}/g;
    s/\{GENERIC_FAILURE_MODE\}/$ENV{HW_GENERIC_FAILURE_MODE}/g;
    s/\{PRIMARY_USER_GOAL\}/$ENV{HW_PRIMARY_USER_GOAL}/g;
    s/\{CONTENT_REVIEW_STATUS_RULE\}/$ENV{HW_CONTENT_REVIEW_STATUS_RULE}/g;
    s/\{FEEDBACK_REASONING_RULE\}/$ENV{HW_FEEDBACK_REASONING_RULE}/g;
  '

echo "Replaced common HarnessWeaver placeholders."
echo "Project path: $work_root"
echo "Next: run bash scripts/verify.sh --instance."
echo "If TODO values remain, resolve them before running bash scripts/verify.sh --strict-instance."
