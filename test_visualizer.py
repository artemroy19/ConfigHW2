import unittest
import shutil
import os
from git import Repo
from visualizer import generate_plantuml, visualize_graph

TEST_REPO_PATH = "/Users/artem/Desktop/ConfigHW1"
TEST_OUTPUT_PATH = "test_output.png"
PLANTUML_JAR = "/Users/artem/Desktop/задание/Configuraz2/plantuml.jar"


class TestVisualizer(unittest.TestCase):

    def setUp(self):
        self.repo = Repo.init(TEST_REPO_PATH)
        with open(os.path.join(TEST_REPO_PATH,"README.md"), "w") as f:
            f.write("# Test Repo")
        self.repo.index.add(["README.md"])
        self.repo.index.commit("Initial commit")

    def tearDown(self):
        shutil.rmtree(TEST_REPO_PATH)
        if os.path.exists(TEST_OUTPUT_PATH):
          os.remove(TEST_OUTPUT_PATH)
        if os.path.exists(TEST_OUTPUT_PATH.replace(".png", ".puml")):
          os.remove(TEST_OUTPUT_PATH.replace(".png", ".puml"))


    def test_generate_plantuml_valid_repo(self):
        plantuml_code = generate_plantuml("/Users/artem/Desktop/Yandex-Project1","main", "temp.puml")
        self.assertTrue(plantuml_code is not None)


    def test_generate_plantuml_invalid_repo(self):
        plantuml_code = generate_plantuml("none", "main", "temp.puml")
        self.assertTrue(plantuml_code is None)

    @unittest.skipIf(not os.path.exists(PLANTUML_JAR), "Файл PlantUML jar не найден")
    def test_visualize_graph(self):
        plantuml_code = generate_plantuml(TEST_REPO_PATH,"main", "test_output.puml")
        if plantuml_code:
            exit_code = visualize_graph(PLANTUML_JAR, TEST_OUTPUT_PATH, "test_output.puml")
            self.assertEqual(exit_code, 0)
            self.assertTrue(os.path.exists(TEST_OUTPUT_PATH))


if __name__ == '__main__':
    unittest.main()