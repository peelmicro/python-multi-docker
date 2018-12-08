# Create the Docker Images
docker build -t peelmicro/python-multi-client:latest -t peelmicro/python-multi-client:$SHA -f ./client/Dockerfile ./client
docker build -t peelmicro/python-multi-server:latest -t peelmicro/python-multi-server:$SHA -f ./server/Dockerfile ./server
docker build -t peelmicro/python-multi-worker:latest -t peelmicro/python-multi-worker:$SHA -f ./worker/Dockerfile ./worker

# Take those images and push them to docker hub
docker push peelmicro/python-multi-client:latest
docker push peelmicro/python-multi-client:$SHA
docker push peelmicro/python-multi-server:latest
docker push peelmicro/python-multi-server:$SHA
docker push peelmicro/python-multi-worker:latest
docker push peelmicro/python-multi-worker:$SHA
# Apply all configs in the 'k8s' folder
kubectl apply -f k8s
# Imperatively set lastest images on each deployment
kubectl set image deployments/client-deployment client=peelmicro/python-multi-client:$SHA
kubectl set image deployments/server-deployment server=peelmicro/python-multi-server:$SHA
kubectl set image deployments/worker-deployment worker=peelmicro/python-multi-worker:$SHA