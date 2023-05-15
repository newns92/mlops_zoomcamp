## Intro
- **MLOps** is a set of best practices for putting ML models into production
- When designing a ML system, the job doesn't end with building the model (and achieving high accuracy and low validation error) 
- For a model to actually be helpful, you'll have to consider deployingment, as well as ensuring the model's performance does not degrade over time
- Our main example throughout this course will be predicting the length of a taxi trip
- In the absolute simplest manner, we can describe ML Projects as 3 stages
    - 1\. Design
        - Consider the problem at hand. Do we *really* need ML to solve this problem?
    - 2\. Train
        - i.e., Model development, experieentation, optimization, and selection
    - 3\. Operate
        - i.e., deployment and monitoring
        - If performance of the model degrades, can you retrain the model in a cost-effective manner?
        - How do you ensure the deployed model performs as expected
            - i.e., how do you monitor model performance *in production*?
        - What are the challenges associated with monitoring ML models?


## Environemnt setup
### Linux
- Download and install the **Anaconda** distribution of Python
    - `cd` to `~`
    - Run `wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh`
    - Then run `bash Anaconda3-2022.05-Linux-x86_64.sh`
    - Then remove the installer via `rm Anaconda3-2022.05-Linux-x86_64.sh`
    - Log out of your current SSH session with `exit`
    - Log back in and you should now see a `(base)` at the beginning of your command prompt
- Update existing packages
    - via `sudo apt update && sudo apt -y upgrade`
- Install **Docker**
    - via `sudo apt install docker.io`
    - Add current user to Docker group *to run Docker without `sudo`:*
        - Run `sudo groupadd docker`
        - Then run `sudo usermod -aG docker $USER`
- *In a separate directory*, install **Docker Compose**
    - Run `mkdir soft` then `cd` into it
    - To get the latest release of Docker Compose, go to https://github.com/docker/compose and download the release for your OS.
        - On Linux, via `wget https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-linux-x86_64 -O docker-compose`
    - Make it executable via `chmod +x docker-compose`
    - Add the `soft\` directory to `PATH`
    - Open the `.bashrc` file (via `nano` or not) and add the following line: `export PATH="${HOME}/soft:${PATH}"`
    - Save `.bashrc` and run the following to make sure the changes are applied via `source .bashrc`
- *Run* Docker
    - via `docker run hello-world`
        - If you get the `docker: Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Post "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/containers/create": dial unix /var/run/docker.sock: connect: permission denied.` error, restart your VM instance
        - If you get the `It is required that your private key files are NOT accessible by others. This private key will be ignored.` error, you should change permits on the downloaded key file to protect your private key via `chmod 400 <name-of-your-private-key-file>`

### GCP
- Log into GCP and create a new project named `mlops-zoom`
- Create an instance using Compute Engine
    - Name it \<something\>, select your region Region and Zone (\<something\> and \<something\>) 
    - Select an "N2" Series and "n2-standard-2" machine type with an "Ubuntu 22.04 LTS" boot disk image
    - For a firewall: Check both "Allow HTTP traffic" and "Allow HTTPS traffic"
- Assign a *static* public IP address
    - By default, if you stop your GCP VM and then start it again, you will have a different external IP address, which makes your SSH config on your local useless   
    - Click on the hamburger menu on the far right of the VM instance (next to "SSH")
    - Click "View network details"
    - Name the new static IP address, select the Network Service Tier ("Premium"), IP Version ("IPv4") and Type ("Regional")
    - Then select your region (*same as the VM*) and which VM to attach to (You will find it available in the drop-down if you use the same region)
    - Click "Reserve"
- Enable SSH
    - https://cloud.google.com/compute/docs/connect/create-ssh-keys
    - Generate a SSH key via `ssh-keygen -t rsa -f ~/.ssh/mlops-zoom -C <VM username>`
    - Copy the content of the public key file `mlops-zoom.pub` into GCP under "Metadata" under "Compute Engine"
- SSH into Instance
    - Replace the instance public IP address via `ssh -i ~/.ssh/mlops-zoom <VVM username>@<static IP address>`
        - Optional: Add host to hostname file for easy login
            - Open `~/.ssh/config` (via `nano` or not) and enter the following info:
                ```bash
                Host gcp-mlops-zoom
                    HostName <static public IP> # VM Public IP
                    User <VM user> # VM user
                    IdentityFile ~/.ssh/mlops-zoom # Private SSH key file
                    StrictHostKeyChecking no
                ```
            - Can now SSH in via `ssh mlops-zoom`
- Install dependencies on the VM
    - SSH into the VM
    - Run `sudo apt update && sudo apt -y upgrade` to update existing packages
    - Install Anaconda
        - `cd` to `~`
        - Run `wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh`
        - Then run `bash Anaconda3-2022.05-Linux-x86_64.sh`
        - Then remove the installer via `rm Anaconda3-2022.05-Linux-x86_64.sh`
        - Log out of your current SSH session with `exit`
        - Log back in and you should now see a `(base)` at the beginning of your command prompt
    - Install Docker
        - Run `sudo apt install docker.io`
    - Install Docker-Compose
        - Run `sudo apt install docker-compose`
    - Add current user to Docker group *to run Docker without `sudo`:*
        - Run `sudo groupadd docker` to create the `docker` group
        - Then run `sudo usermod -aG docker $USER` to add the user to the group
    - Verify Installation
        - Run `which python`
        - Run `which docker`
        - Run `which docker-compose`
    - Run Docker
        - Run `docker run hello-world`
    - Run Jupyter Notebook
        - Create a `notebooks` directory and `cd` into it
        - Run `jupyter notebook`
    - Open the host in VSCode and forward port `8888`
    - Can now start using Jupyter Notebook

### AWS (*Not free*)
- Log into the AWS Console (or create an account)
- Click "EC2"
- Start creating an instance by clicking "Launce instance" in the top-right
- Name it `mlops-zoom-aws`
- Select the Ubuntu OS and the "64-bit (x86) architecture (from Intel)
- Select "t2.xlarge" (16 GiB of memory) or "t2.large" (8 GiB of memory)
- Under "Key pair (login)", click "Create new key pair"
    - Enter the key pair name of "mlops-zoom-aws", select key pair type of "RSA" and private key file format of `.pem`
    - Place the key in `~/.ssh/`
- For "Configure storage", enter "30" GiB
    - Since we will be pulling a lot of Docker iamges and doing some data processing
- Finally, click "Launch instance" at the bottom of the page
- Once done, it will provide you with a link to the VM instance in the AWS Console
- Select the public IPv4 address
    - Set the instance public IP address via `ssh -i ~/.ssh/mlops-zoom-aws.pem ubuntu@<static public IP>`
        - Optional: Add host to hostname file for easy login
            - Open `~/.ssh/config` (via `nano` or not) and enter the following info:
                ```bash
                Host aws-mlops-zoom
                    HostName <static public IP> # VM Public IP
                    User ubuntu # VM user
                    IdentityFile ~/.ssh/mlops-zoom-aws.pem # Private SSH key file
                    StrictHostKeyChecking no
                ```
            - Can now SSH in via `ssh mlops-zoom-aws`
    - *This will need to be changed every time you stop and then start the instance again*
- SSH into the VM
- Download and install the **Anaconda** distribution of Python
    - `cd` to `~`
    - Run `wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh`
    - Then run `bash Anaconda3-2022.05-Linux-x86_64.sh`
    - Then remove the installer via `rm Anaconda3-2022.05-Linux-x86_64.sh`
    - Log out of your current SSH session with `exit`
    - Log back in and you should now see a `(base)` at the beginning of your command prompt
- Update existing packages
    - via `sudo apt update && sudo apt -y upgrade`
- Install **Docker**
    - via `sudo apt install docker.io`
    - Add current user to Docker group *to run Docker without `sudo`:*
        - Run `sudo groupadd docker` to create the `docker` group
        - Then run `sudo usermod -aG docker $USER` to add the user to the group
- *In a separate directory*, install **Docker Compose**
    - Run `mkdir soft` then `cd` into it
    - To get the latest release of Docker Compose, go to https://github.com/docker/compose and download the release for your OS.
        - On Linux, via `wget https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-linux-x86_64 -O docker-compose`
    - Make it executable via `chmod +x docker-compose`
    - Add the `soft\` directory to `PATH`
    - Open the `.bashrc` file (via `nano` or not) and add the following line: `export PATH="${HOME}/soft:${PATH}"`
    - Save `.bashrc` and run the following to make sure the changes are applied via `source .bashrc`
- *Run* Docker
    - via `docker run hello-world`
        - If you get the `docker: Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Post "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/containers/create": dial unix /var/run/docker.sock: connect: permission denied.` error, restart your VM instance
        - If you get the `It is required that your private key files are NOT accessible by others. This private key will be ignored.` error, you should change permits on the downloaded key file to protect your private key via `chmod 400 <name-of-your-private-key-file>.pem` (i.e., `chmod 400 mlops-zoom-aws.pem`)

### Azure
- 