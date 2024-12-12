def _load_year(path, package_name):
    from pkgutil import iter_modules

    for module_finder, task_package_name, ispkg in iter_modules(
        [path + "/" + package_name]
    ):
        if not ispkg and task_package_name.startswith("task_"):
            module_finder.find_spec(task_package_name).loader.load_module(
                task_package_name
            )


def _load_all_years():
    from pathlib import Path
    from pkgutil import iter_modules

    path = Path(__file__).parent.stem
    for _, package_name, ispkg in iter_modules([path]):
        if ispkg and package_name.startswith("year_"):
            _load_year(path, package_name)


_load_all_years()
