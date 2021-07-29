#!/bin/sh

set -ex
kubectl apply -f deploy/crd.yaml
kubectl create ns mongodb
kubectl config set-context --current --namespace=mongodb
kubectl apply -f deploy/rbac.yaml -n mongodb
kubectl apply -f deploy/secrets.yaml -n mongodb
kubectl apply -f deploy/operator.yaml -n mongodb
kubectl apply -f deploy/cr.yaml -n mongodb
