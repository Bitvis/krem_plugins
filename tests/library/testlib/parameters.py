#!/bin/env python
import os
from krempack.common import constants as c

#Paths
#EXPECTED_PROJECT_DIRECTORIES = c.PROJECT_DEFAULT_DIRS
TEST_PROJECT_LIBRARY_PATH = os.path.dirname(os.path.realpath(__file__))

TEST_PROJECT_ROOT_PATH = os.path.realpath(os.path.join(TEST_PROJECT_LIBRARY_PATH, "..",".."))

TEST_PROJECT_JOBS_DIR = os.path.join(TEST_PROJECT_ROOT_PATH, "jobs")
TEST_PROJECT_TASKS_DIR = os.path.join(TEST_PROJECT_ROOT_PATH, "tasks")
TEST_PROJECT_OUTPUT_DIR = os.path.join(TEST_PROJECT_ROOT_PATH, "output")

OUTPUT_LATEST_SYMLINK = "latest"

TEMP_PROJECT_NAME = "temp_project"
TEMP_PROJECT_PATH = os.path.abspath(os.path.join(TEST_PROJECT_ROOT_PATH, "output", TEMP_PROJECT_NAME))


