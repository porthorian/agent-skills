#!/usr/bin/env bash
set -eu

source "$(dirname "${BASH_SOURCE[0]}")/snapshot.sh"
case_dir=${1:?supply a writable artifact directory}
mkdir -p "$case_dir"
printf '%s\n' 'payload' >"$case_dir/input"
snapshot "$case_dir/input" "$case_dir/output" >"$case_dir/stdout"
cmp "$case_dir/input" "$case_dir/output"
printf '%s\n' 'snapshot tests passed'
