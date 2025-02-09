import os
from datetime import datetime
from pdm.backend.hooks.version import SCMVersion
from pdm.backend._vendor.packaging.version import Version


def format_version(version: SCMVersion) -> str:

    # SCMVersion
    # Note: There are cases where `Version('0.0')` is obtained when specified via git.
    semver_tokens =list([int(n) for n in str(version.version).split(".")])
    if len(semver_tokens) < 3:
        semver_tokens += [0] * (3 - len(semver_tokens))
    major, minor, patch = semver_tokens

    dirty = f"+{datetime.utcnow():%Y%m%d.%H%M%S}" if version.dirty else ""
    if version.distance is None:
        return f"{major}.{minor}.{patch}{dirty}"
    else:
        return f"{major}.{minor}.{patch}.dev{version.distance}{dirty}"


def pdm_build_initialize(context):
    version = Version(context.config.metadata["version"])

    # This is done in a PDM build hook without specifying `dynamic = [..., "version"]` to put all
    # of the static metadata into pyproject.toml. Tools other than PDM will not execute this script
    # and will use the generic version of the documentation URL (which redirects to /latest).
    if version.is_prerelease:
        url_version = "latest"
    else:
        url_version = f"v{version}"
    context.config.metadata["urls"]["Documentation"] += url_version
