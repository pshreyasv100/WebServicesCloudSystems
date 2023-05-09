### WebServicesCloudSystems assignment 2
### Group 30
- The repository contains the code for second assignment

- There are 2 services corresponding to to urlshortener and authentication

- To run the urlshortener service the urlshortener_service.py module needs to be executed <br/>
`$python urlshortener_service.py`

- To run the authentication service the authentication_service.py module needs to be exectud <br/>
`$python authentication_service.py`

Access endpoint for both <br/>
url shortener service at  http://127.0.0.1:5000  <br/>
authentication service at http://127.0.0.1:5001  <br/>


References

- https://www.tinystacks.com/blog-post/flask-crud-api-with-postgres/


- https://kubernetes.github.io/ingress-nginx/deploy/baremetal/

- https://metallb.universe.tf/installation/


to access on local microk8s 
- localhost:30001
- localhost:30002

- kubernetes flask 

- https://medium.com/@xcoulon/storing-data-into-persistent-volumes-on-kubernetes-fb155da16666
- https://medium.com/@xcoulon/managing-pod-configuration-using-configmaps-and-secrets-in-kubernetes-93a2de9449be
- https://medium.com/@xcoulon/deploying-your-first-web-app-on-minikube-6e98d2884b3a

- create a directory on vm (control node ) to be used for persistence

/opt/postgres/data


- deployment commands

kubectl apply -f postgres-config.yaml 
kubectl apply -f postgres-secret.yaml 
kubectl apply -f postgres-deployment.yaml 
kubectl apply -f postgres-service.yaml


kubectl apply -f deployment.yaml 
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml 


-- psql -h localhost -U postgresadmin --password -p 30010 postgresdb
- admin123