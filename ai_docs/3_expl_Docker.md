<!--
  docker_baleia2.md
  Project-specific Docker Compose reference for AI agents (Cursor, Hiperthink)
  Loaded automatically into memory by agents for code reasoning, orchestration, and infra planning.
  DO NOT REMOVE FROM ai_docs FOLDER
-->

# 🐳

This file documents advanced usage patterns, hidden behaviors, and orchestration logic used in our Docker Compose environments. It complements the official reference: https://docs.docker.com/compose/compose-file/

Agents should reference this file whenever:
- Generating or editing Docker Compose files
- Explaining service startup logic or inter-service dependencies
- Suggesting container orchestration or Docker-based infrastructure

## Core Docker Compose Concepts

### Services

A Compose file must declare a `services` top-level element as a map whose keys are service names, and values are service definitions.

#### Basic Example

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"

  db:
    image: postgres:13
    environment:
      POSTGRES_USER: example
      POSTGRES_DB: exampledb
```

#### Advanced Example

```yaml
services:
  proxy:
    image: nginx
    volumes:
      - type: bind
        source: ./proxy/nginx.conf
        target: /etc/nginx/conf.d/default.conf
        read_only: true
    ports:
      - 80:80
    depends_on:
      - backend

  backend:
    build:
      context: backend
      target: builder
```

### Profiles

Profiles allow you to define a set of active services for various environments.

```yaml
services:
  web:
    image: web_image

  test_lib:
    image: test_lib_image
    profiles:
      - test

  debug_lib:
    image: debug_lib_image
    depends_on:
      - test_lib
    profiles:
      - debug
```

- Services without a `profiles` attribute are always enabled
- If no profile is enabled, only services without profiles are included
- When a profile is enabled, it includes both profile-specific services and services without profiles
- Dependencies must be satisfied within active profiles

### Secrets

Secrets securely store sensitive data that is granted to specific services.

```yaml
secrets:
  server-certificate:
    file: ./server.cert
  token:
    environment: "OAUTH_TOKEN"
```

Services can only access secrets when explicitly granted by a `secrets` attribute:

```yaml
services:
  app:
    secrets:
      - server-certificate
      - source: my_secret
        target: /etc/secrets/my_secret
        uid: "103"
        gid: "103"
        mode: 0440
```

#### Secrets Management - Long Syntax

When defining secrets in services, the long syntax provides more control:

- `source`: The name of the secret as it exists on the platform
- `target`: The name of the file in `/run/secrets/` (defaults to `source`)
- `uid` and `gid`: The numeric IDs for file ownership (defaults to `USER`)
- `mode`: File permissions in octal notation (default: `0444` - world-readable)

```yaml
services:
  frontend:
    build:
      context: .
      secrets:
        - source: server-certificate
          target: server.cert
          uid: "103"
          gid: "103"
          mode: 0440
secrets:
  server-certificate:
    external: true
```

### Configs

Configs can be created from:
- `file`: Content from a file path
- `environment`: Content from an environment variable
- `content`: Inline content defined in the compose file
- `external`: Reference existing config on the platform

```yaml
configs:
  http_config:
    file: ./httpd.conf
  # OR
  app_config:
    content: |
      debug=${DEBUG}
      spring.application.name=${COMPOSE_PROJECT_NAME}
  # OR
  external_config:
    external: true
    name: "${CONFIG_KEY}"
```

Services can access configurations using similar syntax to secrets:

```yaml
services:
  redis:
    image: redis:latest
    configs:
      - my_config
      - source: my_other_config
        target: /redis_config
        uid: "103"
        gid: "103"
        mode: 0440
```

## Key Service Attributes

### `image`

Specifies the image to start the container from. Can be a repository/tag or a partial image ID.

```yml
image: redis
image: redis:5
image: registry.example.com/myapp:1.0
```

### `build`

Specifies the build configuration for creating a container image from source.

```yaml
build:
  context: ./dir  # Path to build context
  dockerfile: Dockerfile-alternate  # Alternate Dockerfile
  args:  # Build arguments
    GIT_COMMIT: cdc3b19
  ssh:  # SSH authentication for builds
    - default  # mount the default SSH agent
    # OR
    - myproject=~/.ssh/myproject.pem  # custom ID with path
```

The builder can then use SSH mounts during builds:

```console
RUN --mount=type=ssh,id=myproject git clone ...
```

### `command`

Overrides the default command declared by the container image:

```yaml
command: bundle exec thin -p 3000
```

Can be specified as a list:

```yaml
command: ["bundle", "exec", "thin", "-p", "3000"]
```

### `container_name`

Specifies a custom container name:

```yaml
container_name: my-web-container
```

Note: Services with custom container names cannot be scaled beyond one container.

### `depends_on`

Expresses startup and shutdown order between services.

Short syntax:
```yaml
depends_on:
  - db
  - redis
```

Long syntax:
```yaml
depends_on:
  db:
    condition: service_healthy
    restart: true
  redis:
    condition: service_started
```

Conditions:
- `service_started`: Wait for service to start (default)
- `service_healthy`: Wait for service to be "healthy" (needs `healthcheck`)
- `service_completed_successfully`: Wait for service to complete successfully

### `deploy`

Specifies configuration for deployment and service lifecycle.

```yaml
deploy:
  mode: replicated  # default - runs specified number of tasks
  replicas: 6
  # OR
  mode: global  # one task per physical node
  # OR
  mode: replicated-job  # job that runs to completion
  # OR
  mode: global-job  # job that runs once per node

  resources:
    limits:
      cpus: '0.50'
      memory: 50M
      pids: 1
    reservations:
      cpus: '0.25'
      memory: 20M
      devices:
        - capabilities: ["gpu"]
          count: 2  # OR device_ids: ["GPU-UUID"]
          driver: nvidia
          
  update_config:
    parallelism: 2  # containers updated at once
    delay: 10s      # time between updates
    order: stop-first  # or start-first
    failure_action: pause  # or continue, rollback
    monitor: 60s    # monitor time after update
    max_failure_ratio: 0.3

  rollback_config:
    parallelism: 1
    delay: 5s
    failure_action: continue  # or pause
    monitor: 20s
    max_failure_ratio: 0.2
    order: stop-first  # or start-first
    
  restart_policy:
    condition: on-failure  # or none, any
    delay: 5s
    max_attempts: 3
    window: 120s  # successful restart window
    
  endpoint_mode: vip  # or dnsrr
```

### `devices`

Defines device mappings:

```yaml
devices:
  - "/dev/ttyUSB0:/dev/ttyUSB0"
  - "/dev/sda:/dev/xvda:rwm"
  - "vendor1.com/device=gpu" # CDI syntax
```

### `dns`, `dns_opt`, `dns_search`

Configure DNS settings:

```yaml
dns:
  - 8.8.8.8
  - 9.9.9.9
dns_opt:
  - use-vc
  - no-tld-query
dns_search:
  - dc1.example.com
  - dc2.example.com
```

### `entrypoint`

Overrides the default entrypoint:

```yaml
entrypoint: /code/entrypoint.sh
# OR
entrypoint:
  - php
  - -d
  - zend_extension=/usr/local/lib/php/extensions/no-debug-non-zts-20100525/xdebug.so
  - vendor/bin/phpunit
```

### `env_file` and `environment`

Add environment variables from a file or directly:

```yaml
env_file:
  - ./a.env
  - ./b.env
# OR with attributes
env_file:
  - path: ./default.env
    required: true
  - path: ./override.env
    required: false
    format: raw
    
environment:
  # Map syntax
  RACK_ENV: development
  SHOW: "true"
  USER_INPUT:

  # Array syntax
  - RACK_ENV=development
  - SHOW=true
  - USER_INPUT
```

#### Env file format

```bash
# Comments start with #
RACK_ENV=development
VAR="quoted value"
EMPTY=
UNSET
```

### `expose`

Exposes ports without publishing to the host:

```yaml
expose:
  - "3000"
  - "8000"
  - "8080-8085/tcp"
```

### `extends`

Shares common configurations across files:

```yaml
extends:
  file: common.yml
  service: webapp
```

### `extra_hosts`

Adds hostname mappings:

```yaml
# List format
extra_hosts:
  - "somehost=162.242.195.82"
  - "otherhost=50.31.209.229"
  - "myhostv6=::1"

# Map format
extra_hosts:
  somehost: "162.242.195.82"
  otherhost: "50.31.209.229"
  myhostv6: "::1"
```

### `gpus`

Allocates GPU devices:

```yaml
gpus: all
# OR
gpus: 
  - driver: nvidia
    count: 2
```

### `healthcheck`

Specifies health checking:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost"]
  interval: 1m30s
  timeout: 10s
  retries: 3
  start_period: 40s
  start_interval: 5s
```

To disable healthcheck:

```yaml
healthcheck:
  disable: true
```

### `init`

Runs an init process (PID 1) inside the container that forwards signals and reaps processes.

```yml
services:
  web:
    image: alpine:latest
    init: true
```

### `labels`

Adds metadata to containers using either array or map format. Using reverse-DNS notation is recommended.

```yml
labels:
  com.example.description: "Accounting webapp"
  com.example.department: "Finance"
```

### `logging`

Configures logging for the service.

```yml
logging:
  driver: syslog
  options:
    syslog-address: "tcp://192.168.0.42:123"
```

### `network_mode`

Sets a service container's network mode.

```yml
network_mode: "host"
network_mode: "none"
network_mode: "service:[service name]"
```

### `networks`

Configures networks for services to connect to.

```yml
services:
  some-service:
    networks:
      - some-network
      - other-network
```

#### Network Configuration Options

- `aliases`: Alternative hostnames on the network
- `ipv4_address`, `ipv6_address`: Static IP addresses
- `link_local_ips`: List of link-local IPs
- `mac_address`: Sets Mac address for network connection
- `gw_priority`: Selects default gateway (highest takes precedence)
- `priority`: Connection priority order

### Complete Networks Example

```yaml
services:
  frontend:
    networks:
      - front-tier
      - back-tier

networks:
  front-tier:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.host_binding_ipv4: "127.0.0.1"
  back-tier:
    driver: custom-driver
    attachable: true
    enable_ipv6: true
    ipam:
      driver: default
      config:
        - subnet: 172.28.0.0/16
          gateway: 172.28.0.1
```

### `ports`

Exposes container ports to the host.

Short syntax:
```yml
ports:
  - "3000"
  - "8000:8000"
  - "127.0.0.1:8001:8001"
  - "6060:6060/udp"
```

Long syntax:
```yml
ports:
  - name: web
    target: 80
    host_ip: 127.0.0.1
    published: "8080"
    protocol: tcp
    app_protocol: http
    mode: host
```

### `post_start` and `pre_stop`

Lifecycle hooks that run after container start or before container stop.

```yaml
services:
  test:
    post_start:
      - command: ./do_something_on_startup.sh
        user: root
        privileged: true
        environment:
          - FOO=BAR
```

### `privileged`

Runs container with elevated privileges.

### `pull_policy`

Controls when images are pulled:
- `always`: Always pull
- `never`: Never pull, use cached only
- `missing`: Pull only if not in cache
- `build`: Always build the image
- `daily`, `weekly`, `every_<duration>`: Time-based pulls

### `restart`

Defines container restart policy.

```yml
restart: "no"
restart: always
restart: on-failure
restart: on-failure:3
restart: unless-stopped
```

### `volumes`

Mounts hosts paths or volumes.

Short syntax:
```yml
volumes:
  - /var/run/postgres/postgres.sock:/var/run/postgres/postgres.sock
  - db-data:/var/lib/postgresql/data
```

Long syntax:
```yml
volumes:
  - type: volume
    source: db-data
    target: /data
    volume:
      nocopy: true
  - type: bind
    source: ./config
    target: /etc/config
    read_only: true
```

## Volume Configuration

Defines reusable volumes that can be shared between services.

```yml
services:
  backend:
    image: example/database
    volumes:
      - db-data:/etc/data

  backup:
    image: backup-service
    volumes:
      - db-data:/var/lib/backup/data

volumes:
  db-data:
```

### Volume Attributes

- `driver`: Specifies volume driver
- `driver_opts`: Driver-specific options
- `external`: Use pre-existing volume
- `labels`: Metadata for volumes
- `name`: Custom volume name

```yml
volumes:
  db-data:
    driver: foobar
    driver_opts:
      type: "nfs"
      o: "addr=10.40.0.199,nolock,soft,rw"
      device: ":/docker/example"
    labels:
      com.example.description: "Database volume"
    name: "my-app-data"
```

## Development Workflows

### Watch Mode

```yaml
services:
  frontend:
    develop:
      watch:
        # Sync files without container restart
        - path: ./webapp/html
          action: sync
          target: /var/www
          ignore:
            - node_modules/
        
        # Rebuild image when files change
        - path: ./src
          action: rebuild
          
        # Sync files and restart container
        - path: ./config
          action: sync+restart
          target: /etc/config
          
        # Sync files and run command
        - path: ./scripts
          action: sync+exec
          target: /scripts
          exec:
            command: reload-app
            user: appuser
            working_dir: /app
```

## Advanced Features

### File Includes

Include other Compose files:

```yaml
# Short syntax
include:
  - ../common/compose.yaml
  - ./override.yaml

# Long syntax
include:
  - path: ../common/compose.yaml
    project_directory: ..
    env_file: ../common/.env
```

### Extensions & YAML Anchors

Use `x-` prefixed fields and YAML anchors for reuse:

```yaml
x-common-config: &common-config
  environment:
    LOG_LEVEL: info
  restart: always

services:
  service1:
    <<: *common-config
    image: example/service1
  
  service2:
    <<: *common-config
    image: example/service2
```

### Merge Behavior

When merging multiple Compose files:
- Mappings are merged by adding missing entries
- Sequences are appended
- Shell commands like `command` and `entrypoint` are replaced
- Use `!reset` to remove elements from the base file
- Use `!override` to completely replace a merged property

```yaml
# Override example
services:
  app:
    ports: !override
      - "8443:443"  # Replaces all ports in base file
    environment:
      DEBUG: !reset null  # Removes DEBUG var
```

### Variable Interpolation

```yaml
services:
  db:
    image: postgres:${POSTGRES_VERSION:-14}
    environment:
      PASSWORD: ${DB_PASSWORD:?required}
      DEBUG: ${ENABLE_DEBUG-false}
```

Formats:
- `${VAR}` - Direct substitution
- `${VAR:-default}` - Default if unset or empty
- `${VAR-default}` - Default if unset
- `${VAR:?error}` - Error if unset or empty
- `${VAR?error}` - Error if unset
- `${VAR:+alt}` - Alt if set and non-empty
- `${VAR+alt}` - Alt if set

## Docker Engine API

Docker provides an API for interacting with the Docker daemon (Docker Engine API), as well as SDKs for Go and Python.

The Docker Engine API is a RESTful API accessible via HTTP clients like `curl` or HTTP libraries in programming languages.

### API Version Compatibility

- The Docker daemon and client don't necessarily need to be the same version
- If the daemon is newer than the client, the client doesn't know about new features or deprecated API endpoints
- If the client is newer than the daemon, the client can request API endpoints that the daemon doesn't know about
- The Docker API is backward-compatible

### Checking API Version

To see the highest version of the API your Docker daemon and client support, use `docker version`:

```console
$ docker version
Client: Docker Engine - Community
 Version:           28.0.0
 API version:       1.48
 Go version:        go1.23.6
 Git commit:        f9ced58
 Built:             Wed Feb 19 22:11:04 2025
 OS/Arch:           linux/amd64
 Context:           default

Server: Docker Engine - Community
 Engine:
  Version:          28.0.0
  API version:      1.48 (minimum version 1.24)
  Go version:       go1.23.6
  Git commit:       af898ab
  Built:            Wed Feb 19 22:11:04 2025
  OS/Arch:          linux/amd64
```

### Specifying API Version

You can specify the API version to use in any of the following ways:

- When using the SDK, use the latest version or at least the version with the features you need
- When using `curl` directly, specify the version as the first part of the URL: `/v1.48/containers/`
- To force the Docker CLI or SDKs to use an older API version, set the environment variable `DOCKER_API_VERSION`
- For SDKs, you can specify the API version programmatically as a parameter to the `client` object

### Using the Docker API

#### Go SDK Example (Running a Container)

```go
package main

import (
	"context"
	"io"
	"os"

	"github.com/docker/docker/api/types/container"
	"github.com/docker/docker/api/types/image"
	"github.com/docker/docker/client"
	"github.com/docker/docker/pkg/stdcopy"
)

func main() {
	ctx := context.Background()
	cli, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	if err != nil {
		panic(err)
	}
	defer cli.Close()

	reader, err := cli.ImagePull(ctx, "docker.io/library/alpine", image.PullOptions{})
	if err != nil {
		panic(err)
	}

	defer reader.Close()
	io.Copy(os.Stdout, reader)

	resp, err := cli.ContainerCreate(ctx, &container.Config{
		Image: "alpine",
		Cmd:   []string{"echo", "hello world"},
		Tty:   false,
	}, nil, nil, nil, "")
	if err != nil {
		panic(err)
	}

	if err := cli.ContainerStart(ctx, resp.ID, container.StartOptions{}); err != nil {
		panic(err)
	}

	statusCh, errCh := cli.ContainerWait(ctx, resp.ID, container.WaitConditionNotRunning)
	select {
	case err := <-errCh:
		if err != nil {
			panic(err)
		}
	case <-statusCh:
	}

	out, err := cli.ContainerLogs(ctx, resp.ID, container.LogsOptions{ShowStdout: true})
	if err != nil {
		panic(err)
	}

	stdcopy.StdCopy(os.Stdout, os.Stderr, out)
}
```

#### Python SDK Example (Running a Container)

```python
import docker
client = docker.from_env()
print(client.containers.run("alpine", ["echo", "hello", "world"]))
```

#### HTTP API Example (Running a Container)

```console
$ curl --unix-socket /var/run/docker.sock -H "Content-Type: application/json" \
  -d '{"Image": "alpine", "Cmd": ["echo", "hello world"]}' \
  -X POST http://localhost/v1.48/containers/create
{"Id":"1c6594faf5","Warnings":null}

$ curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.48/containers/1c6594faf5/start

$ curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.48/containers/1c6594faf5/wait
{"StatusCode":0}

$ curl --unix-socket /var/run/docker.sock "http://localhost/v1.48/containers/1c6594faf5/logs?stdout=1"
hello world
```

### Listing Containers

#### Go Example

```go
package main

import (
	"context"
	"fmt"

	containertypes "github.com/docker/docker/api/types/container"
	"github.com/docker/docker/client"
)

func main() {
	ctx := context.Background()
	cli, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	if err != nil {
		panic(err)
	}
	defer cli.Close()

	containers, err := cli.ContainerList(ctx, containertypes.ListOptions{})
	if err != nil {
		panic(err)
	}

	for _, container := range containers {
		fmt.Println(container.ID)
	}
}
```

#### Python Example

```python
import docker
client = docker.from_env()
for container in client.containers.list():
  print(container.id)
```
