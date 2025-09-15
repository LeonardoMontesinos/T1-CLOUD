import pulumi
import pulumi_aws as aws
import pulumi_docker as docker
import json

# -----------------------------
# Configuración
# -----------------------------
aws_account_id = "<MI_CUENTA>"  # reemplazar
cluster_name = "pulumi-crud-cluster"
container_name = "api-crud"
container_port = 5000
execution_role_arn = "arn:aws:iam::478701513931:role/LabRole"

subnets = ["subnet-xxxxxx"]         # reemplazar
security_groups = ["sg-xxxxxx"]     # reemplazar

# -----------------------------
# Cluster ECS
# -----------------------------
cluster = aws.ecs.Cluster(cluster_name)

# -----------------------------
# Repositorio ECR
# -----------------------------
repo = aws.ecr.Repository(container_name)

# -----------------------------
# Construir y subir Docker automáticamente
# -----------------------------
image = docker.Image(
    "api-crud-image",
    build=docker.DockerBuild(context=".."),  # ruta donde está tu Dockerfile
    image_name=f"{repo.repository_url}:pulumi-latest",
    registry=docker.ImageRegistry(
        server=repo.repository_url,
        username=aws_account_id,
        password=aws.ecr.get_authorization_token().password
    )
)

# -----------------------------
# Task Definition
# -----------------------------
task_definition = aws.ecs.TaskDefinition(
    f"{container_name}-task",
    family=container_name,
    cpu="256",
    memory="512",
    network_mode="awsvpc",
    requires_compatibilities=["FARGATE"],
    execution_role_arn=execution_role_arn,
    container_definitions=image.image_name.apply(lambda img: json.dumps([{
        "name": container_name,
        "image": img,
        "essential": True,
        "portMappings": [{"containerPort": container_port, "hostPort": container_port}]
    }]))
)

# -----------------------------
# Service ECS
# -----------------------------
service = aws.ecs.Service(
    f"{container_name}-service",
    cluster=cluster.id,
    task_definition=task_definition.arn,
    desired_count=1,
    launch_type="FARGATE",
    network_configuration=aws.ecs.ServiceNetworkConfigurationArgs(
        subnets=subnets,
        security_groups=security_groups,
        assign_public_ip=True
    )
)

# -----------------------------
# Outputs
# -----------------------------
pulumi.export("cluster_name", cluster.name)
pulumi.export("service_name", service.name)
pulumi.export("ecr_repo", repo.repository_url)
pulumi.export("docker_image", image.image_name)
