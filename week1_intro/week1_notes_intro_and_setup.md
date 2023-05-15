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
- Go to "IAM & Admin" (Identity and Access Management) --> Service Accounts
    - **Service account** = an account with limited permissions that is assigned to a service (ex: a server or VM)
        - Allows us to create a set of credentials that does not have full access to the owner/admin account
    - Create a service account: "mlops-zoom-user"
    - Grant access as "Basic" --> "Viewer"
        - We will fine tune the permissions in a later step
    - We do not need to "grant users access to this service account"
        - But this is useful in a PROD environment where it may be useful for multiple users to share the same permissions
    - To create a service account key, click the three dots under "Actions" --> "Manage keys"
    - Click "Add key" --> "Create new key" --> "JSON"
        - This downloads a *private* key JSON File
- Add permissions to our service account:
    - Click on "IAM" on the left
    - Click "Edit principal" pencil on the right for the user account we just created
    - Add "Storage Admin" to create and control the GCP data lake
        - Allows us to create and modify buckets and packets (Terraform) and files
        - In PROD, we'd actually create *custom* roles to limit user access to a particular bucket/certain resources
            - We'd create separate service accounts for Terraform, for the data pipeline, etc. (In this course we are only making *one* for simplicity's sake)
    - Add "Storage Object Admin" to add/control things within our bucket/data lake
    - Add "BigQuery Admin"
    - Click "Save"        
- Next, we need to enable API's
    - When the local environment interacts with the cloud enviroment, it does not interact *directly* with the resource
    - These API's are the form of communication
    - We have 2 API's for the IAM itself
        - Click on the 3 bars to the left of "Google Cloud" in the upper-left
        - Click "API's and Services" --> "Library" --> Search for "Identity and Access Management"
        - Choose "Identity and Access Management (IAM) API" --> "Enable"
        - Go back to the library and search for "IAM"
        - Choose "IAM Service Account Credentials API" (which may already be enabled)
    - Enable the Compute Engine API
- Create an instance using Compute Engine
    - Name it "mlops-zoom", select your region Region and Zone ("northamerica-northeast2 (Toronto)" and "northamerica-northeast2-a", respectively) 
    - Select an "N2" Series and "n2-standard-2" machine type with an "Ubuntu 22.04 LTS(x86/64)" boot disk image
    - For a firewall: Check both "Allow HTTP traffic" and "Allow HTTPS traffic"
- Assign a *static* public IP address
    - By default, if you stop your GCP VM and then start it again, you will have a different external IP address, which makes your SSH config on your local useless   
    - Click on the hamburger menu on the far right of the VM instance (next to "SSH")
    - Click "View network details"
    - Then, on the left-hand side, under "VPC Network", click "IP addresses", then "Reserve external static IP address"
    - Name the new static IP address "ml-zoom-ip", select the Network Service Tier ("Premium"), IP Version ("IPv4") and Type ("Regional")
    - Then select your region (*same as the VM*) and which VM to attach to (You will find it available in the drop-down if you use the same region)
    - Click "Reserve"
    - CLI way:
        - Run `gcloud compute addresses create ml-zoom-ip --project=<Project ID> --region=northamerica-northeast2`
        - Then run `gcloud compute instances add-access-config mlops-zoom --project=<Project ID> --zone=northamerica-northeast2-a --address=<IP_OF_THE_NEWLY_CREATED_STATIC_ADDRESS>`
- Enable SSH
    - https://cloud.google.com/compute/docs/connect/create-ssh-keys
    - Generate a SSH key via `ssh-keygen -t rsa -f ~/.ssh/mlops-zoom -C <VM username>`
    - Copy the content of the public key file `mlops-zoom.pub` into GCP under "Metadata" under "Compute Engine"
    - Click "Save" at the bottom on the page
- SSH into Instance
    - Replace the instance public IP address via `ssh -i ~/.ssh/mlops-zoom <VVM username>@<static IP address>` mlops-zoom-user@34.130.192.153
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
            - *Or* just run `source .bashrc` (executed every time we log into the machine)
    - Install Docker
        - Run `sudo apt install docker.io`
    - Install Docker-Compose
        - Run `sudo apt install docker-compose`
    - Add current user to Docker group *to run Docker without `sudo`:*
        - Run `sudo groupadd docker` to create the `docker` group (if it doesn't already exist)
        - Then run `sudo gpasswd -a $USER docker` (`$USER` adds current user to the group)
        - Then run `sudo service docker restart` to restart the Docker daemon
        - Then logout and log back (Ctrl + D or `exit`) so that we don't have to type `sudo` everytime we use a `docker` command
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