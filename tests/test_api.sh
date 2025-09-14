#!/bin/bash
# Script de pruebas CRUD para la API en Fargate usando curl

if [ -z "$1" ]; then
  echo "Uso: $0 <PUBLIC_IP>"
  exit 1
fi

API_URL="http://$1:8000"

echo "=== Creando item ==="
curl -s -X POST "$API_URL/items/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","description":"Mi primera prueba"}'
echo -e "\n"

echo "=== Leyendo item (ID=1) ==="
curl -s -X GET "$API_URL/items/1"
echo -e "\n"

echo "=== Actualizando item (ID=1) ==="
curl -s -X PUT "$API_URL/items/1" \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop Gamer","description":"Actualizado con curl"}'
echo -e "\n"

echo "=== Leyendo item actualizado (ID=1) ==="
curl -s -X GET "$API_URL/items/1"
echo -e "\n"

echo "=== Eliminando item (ID=1) ==="
curl -s -X DELETE "$API_URL/items/1"
echo -e "\n"

echo "=== Verificando que el item fue eliminado ==="
curl -s -X GET "$API_URL/items/1"
echo -e "\n"

echo "Pruebas finalizadas ✅"
