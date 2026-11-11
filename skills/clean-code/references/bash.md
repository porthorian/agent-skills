# Bash

Honor the script's supported Bash version and platform commands. Keep shell tests in the repository's existing harness; the examples use plain Bash and caller-supplied fixture directories.

- Quote expansions that represent one argument, pass argument lists with `"$@"` or arrays, and avoid reconstructing commands with `eval`. Use an option terminator when the command supports it and an operand could look like an option.
- Make failure handling visible at meaningful boundaries. A successful final command can hide an earlier failure. For pipelines, choose whether upstream failures must propagate and account for the status of each relevant stage; `pipefail` changes the pipeline's contract. Treat expected nonzero statuses in conditions explicitly. Shell error options do not replace checking that contract.
- Keep sourceable functions from exiting their caller. Test stdout, stderr, status, and filesystem effects as relevant. Use independent fixture directories and cover paths containing spaces. Stub external commands at the process boundary when needed; keep real local file operations for tests of file behavior.

## Implementation: preserve arguments and propagate failure

The contract is to copy one report and print `copied` only on success. Here `cp` supports `--`.

Before:

```bash
copy_report() {
    cp $1 $2
    printf 'copied\n'
}
```

After:

```bash
copy_report() {
    local source=$1 destination=$2
    cp -- "$source" "$destination" || return "$?"
    printf '%s\n' 'copied'
}
```

Quoting preserves each path, and the explicit return preserves a failed copy's status. Keep this local operation direct; a generic command wrapper would add little. A command with a documented nonzero success-like result, such as a search with no matches, needs its own handling rather than blindly propagating every nonzero status.

## Testing: observe both successful and failed copies

The caller provides a fresh writable `case_dir`. The function under test is already sourced, and the test owns the files it creates in that directory.

Before:

```bash
copy_report $source $destination >/dev/null
test -f $destination
```

After:

```bash
check_copy_report() (
    local case_dir=$1
    local source="$case_dir/monthly report.txt"
    local destination="$case_dir/copied report.txt"
    printf '%s\n' 'report content' >"$source" || return 1

    copy_report "$source" "$destination" >"$case_dir/stdout" 2>"$case_dir/stderr" || return 1
    cmp -- "$source" "$destination" || return 1
    [[ $(<"$case_dir/stdout") == copied && ! -s "$case_dir/stderr" ]] || return 1

    local status=0
    copy_report "$case_dir/missing" "$destination" >"$case_dir/stdout" 2>"$case_dir/stderr" || status=$?
    [[ $status -ne 0 && ! -s "$case_dir/stdout" && -s "$case_dir/stderr" ]]
)
```

The revised test checks content and the observable success/failure contract. Capturing an expected failure in a condition keeps it testable even in a harness using `set -e`. It does not depend on a platform-specific error string. Add a controlled failing command when preserving a particular exit code is itself a requirement; a nonzero-only assertion would not establish that exact contract.

See the Bash manual on [quoting](https://www.gnu.org/software/bash/manual/html_node/Quoting.html) and [pipeline status](https://www.gnu.org/software/bash/manual/html_node/Pipelines.html).
