#!/bin/bash -x
ssh-add ~/.ssh/omef-demo.pem
bastionhost=34.236.98.76
rm -f sandbox.zip
zip a -r sandbox.zip conduit/libs
ssh centos@$bastionhost 'rm -rf ~centos/ksarabi;mkdir -p ~centos/ksarabi'
scp sandbox.zip centos@$bastionhost:~centos/ksarabi
cat <<EOF > run.sh
#!/bin/bash
cd ~/ksarabi
rm -rf sandbox
unzip -jd sandbox sandbox.zip
EOF
cat run.sh | ssh -o StrictHostKeyChecking=no -A centos@$bastionhost