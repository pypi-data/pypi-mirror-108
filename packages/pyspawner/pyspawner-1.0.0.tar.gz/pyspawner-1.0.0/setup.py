# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyspawner']

package_data = \
{'': ['*']}

install_requires = \
['pyroute2.minimal>=0.6.4,<0.7.0']

setup_kwargs = {
    'name': 'pyspawner',
    'version': '1.0.0',
    'description': 'Clone sandboxed Python processes quickly and securely, on Linux.',
    'long_description': 'Clone sandboxed Python processes quickly and securely.\n\nDocumentation\n=============\n\nDocumentation is available at `https://pyspawner.readthedocs.io\n<https://pyspawner.readthedocs.io/>`_.\n\nUsage\n=====\n\nCreate a ``pyspawner.Client`` that imports the "common" Python imports\nyour sandboxed code will run. (These ``import`` statements aren\'t sandboxed,\nso be sure you trust the Python modules.)\n\nThen call ``pyspawner.Client.spawn_child()`` each time you want to create\na new child. It will invoke the pyspawner\'s ``child_main`` function with the\ngiven arguments.\n\nHere\'s pseudo-code for invoking the pyspawner part::\n\n    import pyspawner\n\n    # pyspawner.Client() is slow; ideally, you\'ll just call it during startup.\n    with pyspawner.Client(\n        child_main="mymodule.main",\n        environment={"LC_ALL": "C.UTF-8"},\n        preload_imports=["pandas"],  # put all your slow imports here\n    ) as cloner:\n        # cloner.spawn_child() is fast; call it as many times as you like.\n        child_process: pyspawner.ChildProcess = cloner.spawn_child(\n            args=["arg1", "arg2"],  # List of picklable Python objects\n            process_name="child-1",\n            sandbox_config=pyspawner.SandboxConfig(\n                chroot_dir=Path("/path/to/chroot/dir"),\n                network=pyspawner.NetworkConfig()\n            )\n        )\n\n        # child_process has .pid, .stdin, .stdout, .stderr.\n        # Read from its stdout and stderr, and then wait for it.\n\nFor each child, read from stdout and stderr until end-of-file; then wait() for\nthe process to exit. Reading from two pipes at once is a standard exercise in\nUNIX, so the minutae are left as an exercise. A safe approach:\n\n1. Register both stdout and stderr in a ``selectors.DefaultSelector``\n2. loop, calling ``selectors.BaseSelector.select()`` and reading from\n   whichever file descriptors have data. Unregister whichever file descriptors\n   reach EOF; and read but _ignore_ data past a predetermined buffer size. Kill\n   the child process if this is taking too long. (Keep reading after killing\n   the child to avoid deadlock.)\n3. Wait for the child process (using ``os.waitpid()``) to clean up its\n   system resources.\n\nSetting up your environment\n===========================\n\nYour system must have ``libcap.so.2`` installed.\n\nPyspawner relies on Linux\'s ``clone()`` system call to create child-process\ncontainers. If you\'re using pyspawner from a Docker container, subcontainer\nare disabled by default. Run Docker with\n``--seccomp-opt=/path/to/pyspawner/docker/pyspawner-seccomp-profile.json`` to\nallow creating subcontainers.\n\nBy default, sandboxed children cannot access the Internet. If you want to\nenable networking for child processes, ensure your process has the\n``CAP_NET_ADMIN`` capability. (``docker run --cap-add NET_ADMIN ...``).\nAlso, you\'ll need to configure NAT in the parent-process environment ...\nwhich is beyond the scope of this README. Finally, you may want to supply a\n``chroot_dir`` to give child processes a custom ``/etc/resolv.conf``.\n\nIdeally, sandboxed children would not be able to write anywhere on the main\nfilesystem. Unfortunately, the ``umount()`` and ``pivot_root()`` system calls\nare restricted in many environments. As a placeholder, you\'re encouraged to\nsupply a ``chroot_dir`` to provide an environment for your sandboxed child\ncode. ``chroot_dir`` must be in a separate filesystem from the root filesystem.\n(In the future, when the Linux container ecosystem evolves enough,\n``chroot_dir`` will make children unmount the root filesystem.) Again, chroot\nis beyond the scope of this README.\n\n\nDeveloping\n==========\n\nThe test suite depends on Docker. (Security tests involve temporary files\noutside of temporary directories, iptables rules and setuid-0 files.)\n\nRun ``./test.sh`` to test.\n\nTo add or fix features:\n\n1. Write a test in ``tests/`` that breaks.\n2. Write code in ``pyspawner/`` that makes the test pass.\n3. Submit a pull request.\n\n\nReleasing\n=========\n\n1. Run ``./test.sh`` and ``sphinx-build docs docs/build`` to check for errors.\n2. Write a ``CHANGELOG.rst`` entry.\n3. ``git commit``\n4. ``git tag VERSION`` (use semver with a ``v`` -- e.g., ``v1.2.3``)\n5. ``git push --tags && git push``\n6. ``poetry build``\n7. ``poetry publish``\n\n\nLicense\n=======\n\nMIT. See ``LICENSE.txt``.\n',
    'author': 'Adam Hooper',
    'author_email': 'adam@adamhooper.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CJWorkbench/pyspawner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
