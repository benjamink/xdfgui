import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
from xdfgui.xdftool_wrapper import XdfTool
from xdfgui.lha_split import split_file, DEFAULT_ADF_CAPACITY
from pathlib import Path
import os
import threading


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("xdfgui")
        self.xd = XdfTool()
        self.image_path = None

        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True)

        top = tk.Frame(frame)
        top.pack(fill=tk.X)

        tk.Button(top, text="Open Image", command=self.open_image).pack(side=tk.LEFT)
        tk.Button(top, text="Create Blank ADF", command=self.create_adf).pack(side=tk.LEFT)
        tk.Button(top, text="Format ADF", command=self.format_adf).pack(side=tk.LEFT)
        tk.Button(top, text="Split LHA -> ADFs", command=self.split_lha_to_adfs).pack(side=tk.LEFT)

        self.listbox = tk.Listbox(frame, width=80, height=20)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        bottom = tk.Frame(frame)
        bottom.pack(fill=tk.X)
        tk.Button(bottom, text="Refresh", command=self.refresh).pack(side=tk.LEFT)
        tk.Button(bottom, text="Add File", command=self.add_file).pack(side=tk.LEFT)
        tk.Button(bottom, text="Extract File", command=self.extract_file).pack(side=tk.LEFT)
        tk.Button(bottom, text="Delete", command=self.delete_file).pack(side=tk.LEFT)
        tk.Button(bottom, text="Rename/Move", command=self.rename_file).pack(side=tk.LEFT)

        # Status bar and progress
        status_frame = tk.Frame(root)
        status_frame.pack(fill=tk.X)
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(status_frame, textvariable=self.status_var, anchor="w")
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.progress = ttk.Progressbar(status_frame, mode="indeterminate")
        self.progress.pack(side=tk.RIGHT)

    def set_status(self, text: str):
        self.status_var.set(text)

    def run_task(self, func, *args, **kwargs):
        def target():
            try:
                self.progress.start(10)
                self.set_status("Running...")
                func(*args, **kwargs)
                self.set_status("Done")
            except Exception as e:
                self.set_status(f"Error: {e}")
                messagebox.showerror("Error", str(e))
            finally:
                self.progress.stop()

        t = threading.Thread(target=target, daemon=True)
        t.start()

    def open_image(self):
        p = filedialog.askopenfilename(title="Select ADF/HDF image")
        if p:
            self.image_path = p
            self.root.title(f"xdfgui - {os.path.basename(p)}")
            self.refresh()

    def create_adf(self):
        p = filedialog.asksaveasfilename(defaultextension=".adf", title="Create ADF file")
        if p:
            def work():
                self.xd.create(p)
                self.set_status(f"Created: {p}")

            self.run_task(work)

    def format_adf(self):
        if not (p := self.image_path):
            messagebox.showwarning("No image", "Open or create an image first")
            return
        name = simpledialog.askstring("Volume name", "Enter volume name:", initialvalue="NewDisk")
        if name:
            def work():
                self.xd.format(p, name)
                self.set_status(f"Formatted {p} as {name}")
                self.refresh()

            self.run_task(work)

    def refresh(self):
        def work():
            self.listbox.delete(0, tk.END)
            if not self.image_path:
                return
            code, out, err = self.xd.list(self.image_path)
            if out:
                for line in out.splitlines():
                    self.listbox.insert(tk.END, line)
            else:
                self.listbox.insert(tk.END, "(no output)")

        self.run_task(work)

    def add_file(self):
        if not self.image_path:
            messagebox.showwarning("No image", "Open or create an image first")
            return
        src = filedialog.askopenfilename(title="Select host file to write into image")
        if src:
            ami = simpledialog.askstring("Target path", "Target Amiga path (e.g. c/myfile):", initialvalue="")

            def work():
                self.xd.write(self.image_path, src, ami if ami else None)
                self.refresh()

            self.run_task(work)

    def extract_file(self):
        if not self.image_path:
            messagebox.showwarning("No image", "Open or create an image first")
            return
        ami = simpledialog.askstring("Amiga path", "Path inside image to extract (e.g. c/myfile):")
        if not ami:
            return
        dst = filedialog.askdirectory(title="Select destination directory")
        if not dst:
            return

        def work():
            self.xd.read(self.image_path, ami, dst)

        self.run_task(work)

    def delete_file(self):
        if not self.image_path:
            messagebox.showwarning("No image", "Open or create an image first")
            return
        ami = simpledialog.askstring("Amiga path", "Path inside image to delete (e.g. c/myfile):")
        if not ami:
            return
        if messagebox.askyesno("Confirm", f"Delete {ami} from image?"):

            def work():
                self.xd.delete(self.image_path, ami)
                self.refresh()

            self.run_task(work)

    def rename_file(self):
        if not self.image_path:
            messagebox.showwarning("No image", "Open or create an image first")
            return
        src = simpledialog.askstring("Source path", "Existing Amiga path (e.g. c/oldfile):")
        if not src:
            return
        dst = simpledialog.askstring("Destination path", "New Amiga path (e.g. c/newfile):")
        if not dst:
            return

        def work():
            self.xd.rename(self.image_path, src, dst)
            self.refresh()

        self.run_task(work)

    def split_lha_to_adfs(self):
        # Split an LHA and create ADF images holding each part
        lha = filedialog.askopenfilename(title="Select .lha file to split")
        if not lha:
            return
        out_dir = filedialog.askdirectory(title="Choose output directory for parts and ADFs")
        if not out_dir:
            return
        base = simpledialog.askstring("Base name", "Base name for created ADFs (e.g. lha_parts)")
        if not base:
            base = Path(lha).stem

        part_size = simpledialog.askinteger("Part size bytes", "Max bytes per part (approx):", initialvalue=DEFAULT_ADF_CAPACITY - 20000)

        def work():
            parts = split_file(lha, part_size=part_size, out_dir=out_dir)
            created = []
            for idx, part in enumerate(parts, start=1):
                adf_name = os.path.join(out_dir, f"{base}-{idx:02d}.adf")
                self.xd.create(adf_name)
                self.xd.format(adf_name, f"{base}-{idx:02d}")
                self.xd.write(adf_name, part)
                created.append(adf_name)
            messagebox.showinfo("Done", f"Created {len(created)} ADFs in {out_dir}")

        self.run_task(work)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
