import docker
import argparse

class ImageNotFound(Exception):
    pass

class MainObj:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Reverse Engineering on Docker Image')
        parser.add_argument('-b','--base-url', default='unix://var/run/docker.sock', help='Base URL to Docker socket')
        parser.add_argument('-i','--docker-image', default='', help='Docker Image ID')
        args = parser.parse_args()
        if args.base_url :
            base_url=args.base_url
        else:
            base_url='unix://var/run/docker.sock'

        if args.docker_image :
            docker_image=args.docker_image            

        super(MainObj, self).__init__()
        self.commands = []
        self.cli = docker.APIClient(base_url=base_url)
        self._get_image(docker_image)
        self.hist = self.cli.history(self.img['RepoTags'][0])
        self._parse_history()
        self.commands.reverse()
        self._print_commands()

    def _print_commands(self):
        for i in self.commands:
            print(i)

    def _get_image(self, img_hash):
        images = self.cli.images()
        for i in images:
            if img_hash in i['Id']:
                self.img = i
                return
        raise ImageNotFound("Image {} not found\n".format(img_hash))

    def _insert_step(self, step):
        if "#(nop)" in step:
            to_add = step.split("#(nop) ")[1]
        else:
            to_add = ("RUN {}".format(step))
        to_add = to_add.replace("&&", "\\\n    &&")
        self.commands.append(to_add.strip(' '))

    def _parse_history(self, rec=False):
        first_tag = False
        actual_tag = False
        for i in self.hist:
            if i['Tags']:
                actual_tag = i['Tags'][0]
                if first_tag and not rec:
                    break
                first_tag = True
            self._insert_step(i['CreatedBy'])
        if not rec:
            self.commands.append("FROM {}".format(actual_tag))

__main__ = MainObj()
