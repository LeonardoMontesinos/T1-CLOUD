from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_iam as iam,
    CfnOutput,
)
from constructs import Construct

class CrudStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC existente (default)
        vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)

        # Cluster ECS
        cluster = ecs.Cluster(self, "CrudCluster", vpc=vpc)

        # Security Group (solo puerto 8000 abierto)
        sg = ec2.SecurityGroup(
            self, "CrudSG",
            vpc=vpc,
            allow_all_outbound=True,
            description="Permitir acceso HTTP a la API CRUD"
        )
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(8000), "Allow HTTP")

        # Task Definition (usando LabRole existente)
        task_def = ecs.FargateTaskDefinition(
            self, "CrudTaskDef",
            cpu=256,
            memory_limit_mib=512,
            execution_role=iam.Role.from_role_arn(
                self, "LabRoleExec",
                role_arn="arn:aws:iam::153265898954:role/LabRole"
            ),
        )

        # Contenedor
        task_def.add_container(
            "CrudContainer",
            image=ecs.ContainerImage.from_registry(
                "153265898954.dkr.ecr.us-east-1.amazonaws.com/crud-sqlite-api:latest"
            ),
            port_mappings=[ecs.PortMapping(container_port=8000)]
        )

        # ECS Service
        service = ecs.FargateService(
            self, "CrudService",
            cluster=cluster,
            task_definition=task_def,
            desired_count=1,
            assign_public_ip=True,
            security_groups=[sg],
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
        )

        # Outputs para que sea más fácil buscar la IP
        CfnOutput(self, "ClusterName", value=cluster.cluster_name)
        CfnOutput(self, "ServiceName", value=service.service_name)
        CfnOutput(self, "SecurityGroupId", value=sg.security_group_id)
