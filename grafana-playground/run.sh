#!/bin/bash

set -e

function run-docker {
	set -e

    # Check if Docker is running
	if ! docker info >/dev/null 2>&1; then
		echo "Docker is not running. Please start Docker Desktop and try again."
		exit 1
	fi

    docker compose up --remove-orphans --build
}


# print all functions in this file
function help {
	echo "$0 <task> <args>"
	echo "Tasks:"
	compgen -A function | cat -n
}

TIMEFORMAT="Task completed in %3lR"
time ${@:-help}