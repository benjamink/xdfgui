import subprocess
import tempfile
import shutil
from pathlib import Path


class XdfTool:
    def __init__(self, xdftool_cmd="xdftool"):
        self.cmd = xdftool_cmd

    def _run(self, image: str, args: list, capture=False):
        full = [self.cmd, image] + args
        if capture:
            res = subprocess.run(full, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return res.returncode, res.stdout, res.stderr
        else:
            res = subprocess.run(full, check=True)
            return res.returncode, None, None

    def create(self, image_path: str):
        return self._run(image_path, ["create"])

    def format(self, image_path: str, volume_name: str = "NewDisk", dos_type: str = "ofs"):
        # format will implicitly create if missing
        return self._run(image_path, ["format", volume_name, dos_type])

    def list(self, image_path: str, ami_path: str = None, all_flag=False, info=False):
        args = ["list"]
        if ami_path:
            args.append(ami_path)
        if all_flag:
            args.append("all")
        if info:
            args.append("info")
        return self._run(image_path, args, capture=True)

    def info(self, image_path: str):
        return self._run(image_path, ["info"], capture=True)

    def read(self, image_path: str, ami_path: str, sys_path: str = None):
        args = ["read", ami_path]
        if sys_path:
            args.append(sys_path)
        return self._run(image_path, args)

    def write(self, image_path: str, sys_path: str, ami_path: str = None):
        args = ["write", sys_path]
        if ami_path:
            args.append(ami_path)
        return self._run(image_path, args)

    def delete(self, image_path: str, ami_path: str, all_flag: bool = False):
        args = ["delete", ami_path]
        if all_flag:
            args.append("all")
        return self._run(image_path, args)

    def makedir(self, image_path: str, ami_path: str):
        return self._run(image_path, ["makedir", ami_path])

    def relabel(self, image_path: str, new_name: str):
        return self._run(image_path, ["relabel", new_name])

    def rename(self, image_path: str, src_ami: str, dst_ami: str):
        # No direct rename in xdftool: implement via temp copy to host, write, delete.
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.close()
        try:
            # extract to tmp
            self._run(image_path, ["read", src_ami, tmp.name])
            # write back under new name
            self._run(image_path, ["write", tmp.name, dst_ami])
            # delete original
            self._run(image_path, ["delete", src_ami])
        finally:
            try:
                Path(tmp.name).unlink()
            except Exception:
                pass

    def move(self, image_path: str, src_ami: str, dst_ami: str):
        return self.rename(image_path, src_ami, dst_ami)
