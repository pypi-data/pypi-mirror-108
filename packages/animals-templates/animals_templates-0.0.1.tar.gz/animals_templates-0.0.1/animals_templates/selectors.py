import importlib


def get_animal_by_name(name: str) -> str:
    """Get animal template by name

    :param name str name of the animal
    :return string animal template
    """
    module = importlib.import_module(f"animals_templates.{name}")
    return getattr(module, name)
