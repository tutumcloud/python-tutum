from base import RESTModel

class Application(RESTModel):

    endpoint = "/application"

    params_for_create = ('image_tag', 'name', 'container_size',
                         'run_command', 'entrypoint', 'target_num_containers',)

    params_for_update = ('name', 'container_size',)