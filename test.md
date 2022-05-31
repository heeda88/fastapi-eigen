Filebrowser on Docker
READ TIME (~ 20 MINS)
Filebrowser on Docker
What is Filebrowser and Why Filebrowser ?
Pre-requisites
Steps to Deploy Filebrowser on Docker
In this tutorial, you’ll be learning how to deploy “filebrowser” – a web-based file browser on docker

What is Filebrowser and Why Filebrowser ?
It is a web based file browser
It can be used to share content easily within your local network
It can used as create-your-own-cloud-kind of software where you can install it on a server, direct it to a path and then access your files through a nice web interface.
Pre-requisites
Docker should be installed and ready to use
For more blogs, visit: Blogs

Steps to Deploy Filebrowser on Docker
1. Setup folder to maintain the container data and navigate into it

# Create a directory for the project
mkdir -p projects/filebrowser
# Navigate into the created folder
cd projects/filebrowser
2. Create empty configuration files which will later be used by the container

# Create the required configuration files
touch filebrowser.db
touch .filebrowser.json
# Edit the json file using any editor (nano in this case)
nano .filebrowser.json
# Paste the below into it
{
  "port": 80,
  "baseURL": "",
  "address": "",
  "log": "stdout",
  "database": "/database.db",
  "root": "/srv"
}

# Save the file
3. Deploy the container using docker as shown

# -d flag specifies to run the container in detached state
# -v /home/pi:/srv - Here the path on the left side is the path that needs to be served on the filebrowser (pi home folder in this case)
# -p specifies the port mapping where the left side is the host port and the right side is the container port

docker run -d \
    -v /home/pi:/srv \
    -v /home/pi/filebrowser/filebrowser.db:/database.db \
    -v /home/pi/filebrowser/.filebrowser.json:/.filebrowser.json \
    --user $(id -u):$(id -g) \
    -p 9000:80 \
    filebrowser/filebrowser
4. Access the filebrowser by navigating to http://<ip>:<port> where IP is the IP of your machine and port is the Port on which the container was deployed. You will see a login screen as shown below. Log in using the following credentials:

Username: admin

Password: admin

Filebrowser
5. You should now be able to see the dashboard with the files served from the directory specified in the volume mount while deploying the docker container. (The home directory of the user pi in this case)

Filebrowser
6. Change the default password by accessing the User settings tab in settings as shown below. Click on the pen icon to edit the password

Filebrowser
7. Enter the new password and click on “Save”

Filebrowser
Congratulations!! You’ve successfully deployed Filebrowser on Docker