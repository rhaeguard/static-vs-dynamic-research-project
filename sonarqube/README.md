# Sonar Setup

## Sonarqube

We used Sonarqube 8.7 Community Edition. 

### Using Docker Compose

Docker compose version has a postgres database coming with it.

`docker-compose.yml` file has been provided in this folder. To start the server, all you need to do is:

```bash
docker-compose up --build  # in the folder of compose file
```

### Docker itself

This version relies on in-memory H2 database.

```bash
docker run -d --name sonarqube -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true -p 9000:9000 sonarqube:8.7-community
```

### Quality Profiles

Sonarqube provides built in quality profiles for each language. Those profiles contain X amount of rules. However, most of the time, those aren't all of the available rules. We enabled most of the deactivated ones for each language. In the quality-profiles folder, you can find the backup xml files for those quality gates; and using those you can restore the profiles we used for the experiment.

#### Making a quality profile the default one

Sonarqube picks the default quality profile automatically. So to make the newly added one the default one:

1. Go to `{SONARQUBE_URL}/profiles`
2. Click on _Restore_ button at the top right corner.
3. Import the xml file, that's it.
4. To use that quality profile:
    1. Go to `{SONARQUBE_URL}/profiles`
    2. Find the newly added quality profile
    3. Click on gear icon and click "Set as Default"


## Sonar Scanner

To run the scan, we need Sonar Scanner. It can be found here - https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/.

We used the version 4.5.

After downloading and setting it up (adding to PATH if needed), we need configure it as well. In the Sonar Scanner installation folder, locate to `/conf` and edit the `sonar-scanner.properties` file with the following information:

```text
sonar.host.url=<HOST_URL>
sonar.login=<LOGIN_TOKEN>
```

HOST_URL is the Sonarqube server address. LOGIN_TOKEN is a token provided by Sonarqube that can be used to access Sonarqube Web API, perform scans and all that. 

To get a login token:

1. Go to `{SONARQUBE_URL/account/security}`
2. Put a name in the Generate Tokens field, and press Generate.
3. Copy the token, and save it somewhere, because it won't be visible next time.
