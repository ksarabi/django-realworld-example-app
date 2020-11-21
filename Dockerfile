FROM quay.io/eclipse/che-python-3.7:7.20.1

## Install Helm

# Note: Latest version of kubectl may be found at: # https://aur.archlinux.org/packages/kubectl-bin/ 
ARG KUBE_LATEST_VERSION="v1.19.4" 
# Note: Latest version of helm may be found at: # https://github.com/kubernetes/helm/releases 
ARG HELM_VERSION="v3.4.1" 
USER root
ENV HELM_HOME="/usr/local/bin/"
ENV HELM_BINARY="/usr/local/bin/helm"
RUN mkdir -p /usr/local/bin/plugins
RUN apt update && apt install bash wget curl openssl -y \
    && wget -q https://storage.googleapis.com/kubernetes-release/release/${KUBE_LATEST_VERSION}/bin/linux/amd64/kubectl -O /usr/local/bin/kubectl \
    && chmod +x /usr/local/bin/kubectl \
    && wget -q https://get.helm.sh/helm-${HELM_VERSION}-linux-amd64.tar.gz -O - | tar -xzO linux-amd64/helm > /usr/local/bin/helm \
    && chmod +x /usr/local/bin/helm
RUN apt update  && apt install git -y
RUN helm plugin install https://github.com/Microsoft/helm-json-output --version master
COPY . app
RUN pip install -r app/requirements.txt && pip install  ptvsd
RUN chown -R 10001:root app /home/user &&  chmod 775 -R app /home/user
EXPOSE 7000
USER 10001
WORKDIR app
CMD ["./start.sh"]