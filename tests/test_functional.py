import os
from os.path import join, abspath, dirname
from unittest import TestCase
from scrapter.run import execute

TEST_DIR = abspath(dirname(__file__))
PROJECT_DIR = join(join(TEST_DIR, 'project'), 'project')

class TestScrapter(TestCase):

    def test(self):
        start_directory = os.getcwd()
        os.chdir(PROJECT_DIR)
        execute()
        os.chdir(start_directory)