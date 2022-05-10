# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/)

The types of changes are:

* `Added` for new features.
* `Changed` for changes in existing functionality.
* `Developer Experience` for changes in developer workflow or tooling.
* `Deprecated` for soon-to-be removed features.
* `Breaking Changes` for updates that break public facing APIs
* `Docs` for documentation only changes.
* `Removed` for now removed features.
* `Fixed` for any bug fixes.
* `Security` in case of vulnerabilities.

## [Unreleased](https://github.com/ethyca/fidesops/compare/1.4.1...main)

### Added

* GET routes for users by @TheAndrewJackson in [#405](https://github.com/ethyca/fidesops/pull/405)
* Username based search on GET route by @TheAndrewJackson in [#444](https://github.com/ethyca/fidesops/pull/444)
* FIDESOPS__DEV_MODE for Easier SaaS Request Debugging by @pattisdr in [#363](https://github.com/ethyca/fidesops/pull/363)
* Track user privileges across sessions by @TheAndrewJackson in [#425](https://github.com/ethyca/fidesops/pull/425)
* Add first_name and last_name fields. Also add them along with created_at to FidesopsUser response by @seanpreston in [#465](https://github.com/ethyca/fidesops/pull/465)
* Denial reasons for DSR and user `AuditLog` by @TheAndrewJackson in [#463](https://github.com/ethyca/fidesops/pull/463)
* DRP action to Policy by @eastandwestwind and @conceptualshark in [#453](https://github.com/ethyca/fidesops/pull/453)
* `CHANGELOG.md` file by @TheAndrewJackson [#484](https://github.com/ethyca/fidesops/pull/484)


### Changed 
* Converted HTTP Status Codes to Starlette constant values by @sanders41 in [#438](https://github.com/ethyca/fidesops/pull/438)
* SaasConnector.send behavior on ignore_errors now returns raw response by @adamsachs in [#462](https://github.com/ethyca/fidesops/pull/462)
* Seed user permissions in `create_superuser.py` script by @TheAndrewJackson in [#468](https://github.com/ethyca/fidesops/pull/468) 
* User API Endpoints (update fields and reset user passwords) by @seanpreston in [#471](https://github.com/ethyca/fidesops/pull/471)
* Format tests with `black` by @seanpreston in [#466](https://github.com/ethyca/fidesops/pull/466)


### Breaking Changes
* Update masking API to take multiple input values by @adamssachs in [#443](https://github.com/ethyca/fidesops/pull/443

### Docs

* Added issue template for documentation updates by @cenceptualshark in [#442](https://github.com/ethyca/fidesops/pull/442)
* Clarify masking updates by @adamsachs in [#464](https://github.com/ethyca/fidesops/pull/464)
* Added dark mode by @conceptualshark in [#476](https://github.com/ethyca/fidesops/pull/476)


### Fixed

* Removed miradb test warning by @sanders41 in [#436](https://github.com/ethyca/fidesops/pull/436)
* Added missing import by @galvana in [#448](https://github.com/ethyca/fidesops/pull/448)
* Removed pypi badge pointing to wrong package by @TheAndrewJackson in [#452](https://github.com/ethyca/fidesops/pull/452)
* Audit imports and references by @seanpreston in [#479](https://github.com/ethyca/fidesops/pull/479)

