resource "aws_ecs_task_definition" "api_task" {
  family                   = var.container_name
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"

  execution_role_arn = "arn:aws:iam::310034235193:role/LabRole"

  container_definitions = jsonencode([
    {
      name      = var.container_name
      image     = var.image
      essential = true
      portMappings = [
        {
          containerPort = var.container_port
          hostPort      = var.container_port
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "api_service" {
  name            = var.container_name
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.api_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = ["subnet-0291c47f7c74c8b64"] # reemplazar con tus subnets
    security_groups = ["sg-0b546e2ac3353c9e8"]     # reemplazar con tu SG
    assign_public_ip = true
  }
}
