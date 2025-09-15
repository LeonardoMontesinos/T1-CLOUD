

# T1-CLOUD

CRUD API con **FastAPI** y **SQLite**, desplegable en **AWS Fargate** usando diferentes herramientas de IaC: **CDK**, **CloudFormation**, **Pulumi** y **Terraform**.

## 📁 Estructura del proyecto

```
lazheart-t1-cloud/
├── README.md
├── app.py                  # API CRUD FastAPI
├── Dockerfile              # Contenedor de la API
├── requirements.txt        # Dependencias Python
├── CDK/                    # Infraestructura con AWS CDK
├── CloudFormation/         # Plantilla YAML de CloudFormation
├── Pulumi/                 # Infraestructura con Pulumi
├── Terraform/              # Infraestructura con Terraform
└── tests/                  # Scripts de prueba
```

---

## 📝 Descripción de la API

* Endpoints CRUD para `items`:

  * `POST /items/` → Crear item
  * `GET /items/{id}` → Leer item
  * `PUT /items/{id}` → Actualizar item
  * `DELETE /items/{id}` → Eliminar item
* Base de datos: SQLite (`items.db`)

Ejemplo de JSON para crear/actualizar:

```json
{
  "name": "Laptop",
  "description": "Mi primera prueba"
}
```

---

## 🐳 Uso local con Docker

1. Construir imagen:

```bash
docker build -t crud-api .
```

2. Ejecutar contenedor:

```bash
docker run -d -p 8000:8000 crud-api
```

3. Acceder a la API en `http://localhost:8000`.

4. Probar endpoints:

```bash
curl -X POST http://localhost:8000/items/ -H "Content-Type: application/json" -d '{"name":"Laptop","description":"Mi primera prueba"}'
```

---

## ⚡ Despliegue en AWS Fargate

### 🔹 Usando AWS CDK

1. Instalar dependencias:

```bash
cd CDK
pip install -r requirements.txt
```

2. Desplegar stack:

```bash
cdk deploy --require-approval never
```

> Esto creará: VPC (existente), cluster ECS, Fargate Task Definition, Security Group y Fargate Service.

---

### 🔹 Usando CloudFormation

1. Editar `CloudFormation/ecs-fargate-crud.yml` con tu VPC y Subnets.
2. Desplegar:

```bash
aws cloudformation deploy \
  --template-file CloudFormation/ecs-fargate-crud.yml \
  --stack-name ecs-fargate-crud \
  --capabilities CAPABILITY_NAMED_IAM
```

---

### 🔹 Usando Pulumi

1. Editar `Pulumi/__main__.py` con:

   * `aws_account_id`
   * `subnets`
   * `security_groups`

2. Inicializar proyecto:

```bash
cd Pulumi
pulumi stack init dev
pulumi up
```

---

### 🔹 Usando Terraform

1. Editar `Terraform/variables.tf` con tu imagen, subnets y security group.
2. Inicializar Terraform:

```bash
cd Terraform
terraform init
terraform apply
```

---

## 🧪 Pruebas de la API

Script de prueba `tests/test_api.sh`:

```bash
./tests/test_api.sh <PUBLIC_IP_DEL_SERVICIO>
```

Esto realiza:

* Crear item
* Leer item
* Actualizar item
* Leer item actualizado
* Eliminar item
* Verificar eliminación

---

## 🔗 Notas adicionales

* API expuesta en el puerto `8000`.
* Roles de IAM usados: `LabRole` (ejecución de contenedores).
* Contenedor subido a ECR y usado en Fargate.

---
