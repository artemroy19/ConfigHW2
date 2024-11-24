import subprocess
import os
import git
from git import Repo
import argparse

def get_commit_info(commit):
    """Извлекает информацию о коммите."""
    return f"({commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S')}, {commit.author.name})"


def generate_plantuml(repo_path, branch_name, output_file):
    """Генерирует код PlantUML для графа зависимостей."""

    try:
        repo = Repo(repo_path)
        commits = list(repo.iter_commits(branch_name))
    except git.exc.InvalidGitRepositoryError:
        print(f"Ошибка: '{repo_path}' не является Git репозиторием.")
        return None
    except git.exc.NoSuchPathError:
        print(f"Ошибка: Путь '{repo_path}' не существует.")
        return None
    except git.exc.GitCommandError as e:
        print(f"Ошибка Git: {e}")
        return None

    plantuml_code = "@startu  ml\n"
    for i, commit in enumerate(commits):
        plantuml_code += f"commit_{i} : {get_commit_info(commit)}\n"
        if i > 0:
            plantuml_code += f"commit_{i-1} --> commit_{i}\n"
    plantuml_code += "@enduml"

    with open(output_file, "w") as f:
        f.write(plantuml_code)
    return plantuml_code


def visualize_graph(plantuml_path, output_image_path, plantuml_code_file):
    """Визуализирует код PlantUML с помощью указанной программы."""
    try:
        command = ["java", "-jar", plantuml_path, "-tpng", plantuml_code_file, "-o", os.path.dirname(output_image_path)]
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Граф успешно создан и сохранен в {output_image_path}")
        return 0
    except FileNotFoundError:
        print(f"Ошибка: PlantUML не найден по пути: {plantuml_path} или Java не установлена.")
        return 1
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании графа: {e.stderr}")
        return 1
    except Exception as e:
        print(f"Произошла неизвестная ошибка: {e}")
        return 1



def main():
    parser = argparse.ArgumentParser(description="Визуализатор графа зависимостей Git репозитория.")
    parser.add_argument("plantuml_path", help="Путь к программе PlantUML (jar-файл)")
    parser.add_argument("repo_path", help="Путь к Git репозиторию")
    parser.add_argument("output_image_path", help="Путь к файлу с изображением графа (без расширения)")
    parser.add_argument("branch_name", help="Имя ветки")
    args = parser.parse_args()

    plantuml_code_file = args.output_image_path + ".puml"

    plantuml_code = generate_plantuml(args.repo_path, args.branch_name, plantuml_code_file)
    if plantuml_code:
        exit_code = visualize_graph(args.plantuml_path, args.output_image_path + ".png", plantuml_code_file)
        exit(exit_code)


if __name__ == "__main__":
    main()