import typing as T
import docker
import subprocess
import pathlib
import logging

pwd: str = pathlib.Path().absolute()

docker_client = docker.from_env()
logging.basicConfiglevel=(logging.INFO)

class Docker_registry:
    def __init__(self, container_name:T.Optional[str]="dockerregistry", ippr:T.Optional[str]="localhost", port:T.Optional[str]="5000"):
        self.container_name=container_name
        self.ippr=ippr
        self.port=port

    def is_container_running(self,container_name:T.Optional[str]="dockerregistry")-> bool:
        """Verify the status of a container by it's name
        :param container_name: the name of the container
        :return: boolean or None
        """
        print(f'Checking if container {container_name} is running or not')
        RUNNING = "running"

        try:
            container = docker_client.containers.get(container_name)
        except docker.errors.NotFound as exc:
            print(f"Check container name!\n{exc.explanation}")
            return False
        else:
            container_state = container.attrs["State"]
            return container_state["Status"] == RUNNING


    def check_repo_in_pvt_reg(self):
        """
        prints containers or images in private container registry
        """
        running = self.is_container_running(self.container_name)

        check_repos = f"curl -X GET localhost:{self.port}/v2/_catalog"
        if not running:
            print(
                f"""Container {self.container_name} is not running, 
                    First start the container and check repos in private registry"""
            )
        else:
            print(f"Container {self.container_name} is running and now checking repos in private registry")
            res =subprocess.Popen(check_repos.split(), stdout=subprocess.PIPE)
            q,w=res.communicate()
            print("Repo's in private container registry are:",q.decode())
    
    def setup_pvt_registry(self):
        """
        Setup private registry in given port

        """

        if not self.is_container_running(self.container_name):
            print(f"Container {self.container_name} is not running")
            print("Starting docker private container registry")
            docker_client.containers.run(
                "registry:latest",
                detach=True,
                ports={self.port: self.port},
                restart_policy={"Name": "always"},
                name=self.container_name,
                environment={"REGISTRY_STORAGE_DELETE_ENABLED": "true"},
                volumes=[f"{pwd}/docker-container/:/var/lib/registry"],
                stdout=True,
            )
            if self.is_container_running(self.container_name):
                print(
                    f"Container {self.container_name} Started succesfully in port {self.port}"
                )
        else:
            print(
                f"A Container is already in use with the name {self.container_name},Try with other name"
            )


    def pull_image(
        self, image: str, private_reg: T.Optional[bool] = True, tag: T.Optional[str] = "latest"
    ):
        """
        Pull images from private container registry.
        """
        
        if private_reg:
            print(f"Pulling image {image} from Local container registry")
            img = docker_client.images.pull(f"{self.ippr}:{self.port}/{image}:{tag}")
        else:
            print(f"Pulling image {image} from DOCKER HUB")
            img = docker_client.images.pull(f"{image}:{tag}")
        print(img)
        print(f"Succesfuly pulled image {image}")


    def push_image(self, image: str, tag: T.Optional[str] = "latest"):
        """
        Upload images to the Private conatainer registry
        """

        try:
            x = docker_client.images.get(image)
            print(f"Tagging image {image} to {self.ippr}:{self.port}/{image}")
            y = x.tag(f"{self.ippr}:{self.port}/{image}:{tag}")
        except:
            print("Image not found ")

        if y:
            print(
                f"""Tagged Succesfully!!
                        Now trying to push image {self.ippr}:{self.port}/{image} to local Container registry
                         """
            )
            docker_client.images.push(f"{self.ippr}:{self.port}/{image}:{tag}")
            print(f"Pushed image {image} to private container Succesfully")


    def delete_image(
        self, image: str, private_reg: T.Optional[bool] = True, tag: T.Optional[str] = "latest"
    ):
        """
        Delete Images from private container registry
        """
        if not private_reg:
            print(f"Deleting image {image} ")
            x = docker_client.images.remove(image)
            print(f"Deleted {image} Succesfully")
        else:
            print("Deleting image from Private container registry")
            hash = subprocess.run(
                [
                    f"""curl -v --silent -H "Accept: application/vnd.docker.distribution.manifest.v2+json" -X GET http://{self.ippr}:{self.port}/v2/{image}/manifests/{tag} 2>&1 | grep Docker-Content-Digest"""
                ],
                shell=True,
                stdout=subprocess.PIPE,
            )
            out = hash.stdout
            print(out)

            asd = out.split()[2].decode()
            l = subprocess.run(
                [f"curl -v -X DELETE http://{self.ippr}:{self.port}/v2/{image}/manifests/{asd}"],
                stdout=subprocess.PIPE,
                shell=True,
            )
            print(l.stdout)
            print("Deleted image Succesfully")


