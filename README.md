# Project Paperwork

This project provides a docker image that builds your project documentations.

## How to use it in your project ?

1. Install docker

- ![Ubuntu Documentation](https://docs.docker.com/engine/install/ubuntu/)

2. Just copy the script **ppaperwork.sh** in your project.

Go inside your project directory

```bash
wget https://raw.githubusercontent.com/ProjectPaperwork/ppaperwork/main/ppaperwork.sh
```

3. Then run it

```bash
source ppaperwork.sh
```

By default all the documentation is generated in 'documentation' directory

## Gitlab Job

To use ppaperwork to auto-generate your documentation into your pipeline, use this snippet

```yaml
# .gitlab-ci.yml
stages:
  - documentation

documentation:
  stage: documentation
  image: ghcr.io/projectpaperwork/ppaperwork:latest
  script:
    - work.sh
  artifacts:
    name: "documentation"
    paths:
      - documentation/
```

## Github Action

To use ppaperwork to auto-generate your documentation into a github action, use this snippet

```yaml
# .github/workflows/documentation.yml
name: Produce the documentation of the repository
on: [push]

jobs:
  SelfDocumentation:
    runs-on: ubuntu-latest
    steps:
      - name: Git checkout
        uses: actions/checkout@v2

      - run: chmod +x ./ppaperwork.sh && ./ppaperwork.sh -r

      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: documentation
          path: documentation

      - run: echo "🎉 finished !"
```

