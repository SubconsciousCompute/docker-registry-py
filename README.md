# Docker Registry Py


This is a simple python program to manage containers to upload, download and delete in private container regitry



To Install `docker-registry-py` use

````
pip install docker_registry_py
````

To use in your py program:

````
from docker_registry import container_registry
````

create an object with class `Docker_registry` in `container_registry` 
example:
````
x = container_registry.Docker_registry()
````






list of functions in container_registry.Docker_registry

|Function                 |     Description                                                                                          |    parameters                    |
|-----------------------  |    ------------------------------------------------------------------------------------------------      |  --------------------            |
|`is_container_running()` | return status true or false whether a container is running with given name or not                        |   container_name:str             |
|`check_repo_in_pvt_reg()`| prints the repos in private registry                                                                     |                                  |
|`setup_pvt_registry()`   | starts private registry with a given conatiner name as class object                                      |                                  |
|`pull_image()`           | Pulls image from docker hub if --no-private-reg or pulls image from private-container-registry by default|  image:str, private_reg: bool    |
|`push_image()`           | Push image to private_container_registry                                                                 | image: str                       |
|`delete_image()`         | Deletes image from private_containe_registry by default                                                  |   image: str,  private_reg:bool  |




