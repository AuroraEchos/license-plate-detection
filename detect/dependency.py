import subprocess
import sys
import pkg_resources


class DependenciesInstaller:
    def __init__(self):
        print("===============================================")
        print("Welcome to Dependencies Installer")
        print("===============================================")
        missing_dependencies = self.check_dependencies()
        if missing_dependencies:
            print("\nMissing dependencies found, installing...")
            self.install_dependencies(missing_dependencies)
            print("\nDependencies installed.")
            print(" ")
        else:
            print("\nAll dependencies are already installed.")
            print(" ")

    def install_dependencies(self, dependencies):
        print("\nInstalling dependencies...")
        for dependency in dependencies:
            install_command = [sys.executable, "-m", "pip", "install", f"{dependency}", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"]
            subprocess.run(install_command, check=True)
        print("\nDependencies installation completed.")

    def check_dependencies(self):
        print("\nChecking required dependencies for the project...")
        dependencies = ['opencv-python==4.8.1.78', 'hyperlpr3==0.1.3','pillow==9.5.0','ultralytics==8.1.24']
        missing_dependencies = []
        
        for dependency in dependencies:
            dependency_name, *version = dependency.split('==')
            if not pkg_resources.get_distribution(dependency_name).version:
                missing_dependencies.append(dependency)
        
        print("Check completed.")
        return missing_dependencies
    
if __name__ == "__main__":
    installer = DependenciesInstaller()
