import subprocess
from typing import Any, Mapping
from arc import CLI, ExecutionError, CommandType as ct
from arc.color import fg, effects
from arc.utils import timer, logger
import yaml

# Intiialzie the CLI first, so
# that the arc_logger gets properly setup
cli = CLI(name="venture", version="2.0b1")

# pylint: disable=wrong-import-position
from .project_list import ProjectList
from .ui import get_ui_provider
from .ui.ui_provider import T
from . import util
from .tags import get_tags
from .config import config, Config, CONFIG_FILE
from .types import OpenContext


def pick(items: Mapping[str, T], pick_config: Config, open_context: OpenContext) -> T:
    provider_type = get_ui_provider(pick_config.ui, open_context)
    provider = provider_type(items, config)
    choice = provider.run()
    if not choice:
        raise ExecutionError("No Valid Option Picked")

    return choice


def execute(path: str, open_context: OpenContext):
    exec_str = config.get_exec(open_context)
    command = exec_str.format(path=util.resolve(path))
    logger.debug("Executing %s", command)
    subprocess.run(command, check=True, shell=True)


@timer("Project Loading")
def get_projects():
    if util.Cache.exists and config.browse.use_cache:
        projects: dict[str, str] = util.Cache.read()
    else:
        projects = ProjectList(config.browse.entries).projects
        if config.browse.use_cache:
            util.Cache.write(projects)

    return projects


@cli.base()
@cli.command()
def run():
    """Open the venture selection menu"""
    projects = get_projects()
    # The method to add the QuickLaunch to the Menu
    # is a little hacky.
    quick_launch_choice = "quicklaunch"
    if config.browse.show_quicklaunch:
        projects = {"\uf85b  QuickLaunch": quick_launch_choice, **projects}

    choice: str = pick(projects, config, OpenContext.BROWSE)
    if choice == quick_launch_choice:
        cli(quick_launch_choice)
    else:
        execute(choice, OpenContext.BROWSE)


@cli.command()
def dump(force: bool = False):
    """Dump Default Config to ~/.config/venture.yaml if it does not exist"""
    if config.exists and not force:
        raise ExecutionError(
            "Configuration already exists. Run again with --force to overwrite"
        )
    config.write(default=True)


@cli.command()
def quicklaunch():
    """Open the Quick Launch Menu"""
    choice = pick(config.quicklaunch.entries, config, OpenContext.QUICK_LAUNCH)
    execute(choice["path"], OpenContext.QUICK_LAUNCH)


@quicklaunch.subcommand("list")
def list_quicklaunch():
    """List quick-launch entries"""
    if len(config.quicklaunch.entries) == 0:
        print(
            "No quick-launch items, add one with "
            f"{fg.GREEN}quicklaunch:add{effects.CLEAR}"
        )
        return

    print("Quicklaunch Items:")
    for name, values in config.quicklaunch.entries.items():
        print(
            f"- {values['icon']}  {name} {fg.BLACK.bright}({values['path']}){effects.CLEAR}"
        )


DOT = "\uf192"


@quicklaunch.subcommand()
def add(
    name: str,
    path: str,
    icon: str = DOT,
    tags: str = None,
    no_default_tags: bool = False,
    icon_only: bool = False,
):
    """\
    Add a new quick-launch entry

    Arguments:
    name=NAME            Display name for the quick-launch entry
    path=PATH            File path to launch when the entry is picked
    icon=ICON            Icon to display along with the name, optional
    tags=TAG1,TAG2       Comma-seperated values to tag the entry with.
                         Will be displayed along with the name of the
                         entry. Icon substitution available.

    --no-default-tags    Disable the generation of default tags for this
                         quick-launch entry
    --icon-only          Automatic tag-generation will display icon-only rather
                         than icon + name
    """

    all_tags = get_tags(
        path,
        tags.split(",") if tags else [],
        icon_only,
        no_default_tags,
    )

    config.quicklaunch.entries[name] = {
        "path": path,
        "icon": icon,
        "tags": list(all_tags),
    }
    config.write()

    print(f"{fg.GREEN}{name} Added!{effects.CLEAR}")


@quicklaunch.subcommand(command_type=ct.POSITIONAL)
def remove(name: str):
    """\
    Remove a quick-launch entry

    `quicklaunch:remove <NAME>`
    """
    if name not in config.quicklaunch.entries:
        raise ExecutionError(f"{name} is not a quick-launch entry")

    config.quicklaunch.entries.pop(name)
    config.write()
    print(f"{fg.GREEN}{name} Removed!{effects.CLEAR}")


@cli.command()
def cache(enable: bool = False, disable: bool = False):
    """\
    Interact with the Venture cache. if no arguments are provided,
    will display the current state of the cache

    The cache stores the data generated to display the main listing.
    For most reasonably sized outputs, the cache isn't necessary, but
    can still speed things up (if only by a fraction of a second). If
    you find running refresh to be annoying, try disabling it and review
    your performance.

    Arguments:
    --enable  enables the cache
    --disable disables the cache
    """
    if all((enable, disable)):
        print("Cannot enable and disable the cache at the same time!")

    elif enable:
        config.browse.use_cache = True
        config.write()
        print("Cache Enabled")

    elif disable:
        config.browse.use_cache = False
        config.write()
        print("Cache Disabled")

    else:
        state = fg.GREEN + "enabled" if config.browse.use_cache else fg.RED + "disabled"
        print(f"Cache is {state}{effects.CLEAR}")
        print("Cache is present" if util.Cache.exists else "Cache empty")


@cache.subcommand()
def refresh():
    """Refreshes the contents of the cache"""
    projects = ProjectList(config.browse.entries).projects
    util.Cache.write(projects)
    print("Cache Refreshed")


@cli.subcommand("update_config")
def update():
    """Checks if the config file needs to be updated"""
    with open(CONFIG_FILE, "r") as f:
        data: dict[str, Any] = yaml.load(f.read(), Loader=yaml.CLoader)

    if data.get("directories"):
        should_update = util.confirm(
            "Looks like you're using an old version of the "
            "config, would you like to update it?"
        )
        if should_update:
            updated = Config.update_config(data)
            updated.write()
            print("Config updated, you should be good to go!")
        else:
            print(
                "Ok, but until you update only ",
                "the default configuration will apply",
            )
    else:
        print("No updates needed!")
