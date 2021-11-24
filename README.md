# Build, check and deploy Gradle Action

A highly configurable composite action taking care of running a complete CI pipeline on a Gradle project

The workflow is the following:

1. Setup java at the version specified by the input parameter `java-version` from the distributor `java-distribution`, configuring also the information for Maven by populating the server username using input `maven-central-username`, the server password using `maven-central-password`, the gpg private key using `signing-key`, and the gpg passphrase using `signing-password`.
2. If the runner is Windows, configure the page file
3. Enable caching for gradle
4. Run `build-command` inside `working-directory`
5. Run `check-command` inside `working-directory`
6. If `should-run-codecov` is set to `true`, then upload coverage informatio to codecov.io
7. if `should-deploy` is set to `true`, run `deploy-command` inside `working-directory`
8. Run `clean-command` inside `working-directory`
9. Turn off the gradle daemon gracefully by running `gradle-termination-command` inside `working-directory`
10. Force kill remaining daemons
11. Cleanup the Gradle cache

## Example

In the following examples, all values but secrets are set to their default. If you are fine with the default value, just omit the parameter.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2.4.0
      - uses: DanySK/build-check-deploy-gradle-action@1.0.0
        with:
          build-command: ./gradlew assemble --parallel
          check-command: ./gradlew check --parallel
          clean-command: 'true'
          deploy-command: ./gradlew publish --parallel
          gradle-termination-command: ./gradlew --stop
          java-distribution: temurin
          java-version: '17'
          should-run-codecov: 'true'
          should-deploy: 'false'
          maven-central-username: 'danysk'
          working-directory: '.'
          custom-secret-0: ''
          custom-secret-1: ''
          custom-secret-2: ''
          custom-secret-3: ''
          custom-secret-4: ''
          github-token: ${{ github.token }}
          gradle-publish-secret:
          gradle-publish-key:
          maven-central-password:
          signing-key:
          signing-password:
```
