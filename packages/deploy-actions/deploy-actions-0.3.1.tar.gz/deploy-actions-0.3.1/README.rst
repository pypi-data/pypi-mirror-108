deploy-actions
==============

|Build Status| |Docs Status| |Deploy Status|

|PyPI Downloads| |Docker Pulls|

|License: MIT|

Repository template with CI/CD for Python apps.

Deployments:

- Docs for GitHub Pages
- Docker build and publish on DockerHub
- PyPI test server publish
- PyPI publish

Required secrets:

- DOCS_TOKEN
- PYPI_TEST_USERNAME
- PYPI_TEST_PASSWORD
- PYPI_USERNAME
- PYPI_PASSWORD
- DOCKERHUB_USERNAME
- DOCKERHUB_TOKEN

.. |Build Status| image:: https://img.shields.io/github/workflow/status/desty2k/deploy-actions/build?style=flat-square
   :target: https://github.com/desty2k/deploy-actions/actions?workflow=build
.. |Docs Status| image:: https://img.shields.io/github/workflow/status/desty2k/deploy-actions/docs?label=docs&style=flat-square
   :target: https://desty2k.github.io/deploy-actions/
.. |Deploy Status| image:: https://img.shields.io/github/workflow/status/desty2k/deploy-actions/deploy?label=deploy&style=flat-square
   :target: https://github.com/desty2k/deploy-actions/actions?workflow=deploy-pypi

.. |PyPI Downloads| image:: https://img.shields.io/pypi/dd/deploy-actions?label=PyPI%20Downloads&style=flat-square
   :target: https://pypi.org/project/deploy-actions/
.. |Docker Pulls| image:: https://img.shields.io/docker/pulls/desty2k/deploy-actions?style=flat-square
   :target: https://hub.docker.com/repository/docker/desty2k/deploy-actions

.. |License: MIT| image:: https://img.shields.io/pypi/l/deploy-actions?color=lightgray&style=flat-square
   :target: https://opensource.org/licenses/MIT



