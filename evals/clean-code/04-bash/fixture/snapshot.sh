#!/usr/bin/env bash

snapshot() {
    cat $1 > $2
    printf '%s\n' 'saved'
}
