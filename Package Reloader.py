import sublime, sublime_plugin
import imp, sys, os

class PackageReloaderListener(sublime_plugin.EventListener):

	def on_post_save(self, view):
		if not view.match_selector(0, "source.python"):
			return []

		sublime.set_timeout(lambda: self.__on_post_save(view), 500)

	def __on_post_save(self, view):

		# Extract Package Name
		package_name = os.path.relpath(view.file_name(), sublime.packages_path()).split(os.sep, 1)[0]
		package_dir = os.path.join(sublime.packages_path(), package_name)

		print(package_dir, package_name)

		# Check for .build
		if os.path.isfile(os.path.join(package_dir, ".build")):

			try:
				with open(os.path.join(package_dir, ".build"), "r", encoding = "utf-8") as f:
					file_json = sublime.decode_value(f.read())
					if not file_json:
						file_json = {"type": "reverse", "mods_load_order": []}
					elif "type" not in file_json or "mods_load_order" not in file_json:
						raise ValueError
			except ValueError as e:
				print("Invalid .build format")
				return

			# Clean non existing items
			items = [item for item in file_json["mods_load_order"] if item == package_name or os.path.isfile(os.path.join(sublime.packages_path(), item.replace(".", os.sep) + ".py"))]

			# Add source files, this is basically to check for new files and add them to the build
			items = [item for item in file_json["mods_load_order"]]
			for item in source_files(package_dir):
				if item not in items:
					items += [item]

			# Write load order back to file_json
			if file_json["type"] == "reverse":
				file_json["mods_load_order"] = sorted(items, reverse = True)
			else:
				file_json["mods_load_order"] = items

			with open(os.path.join(package_dir, ".build"), "w", encoding = "utf-8") as f:
				f.write(sublime.encode_value(file_json, True))

			modules = []
			for mod in file_json["mods_load_order"]:
				if mod in sys.modules and sys.modules[mod]:
					print (">>> reload", mod)
					imp.reload(sys.modules[mod])


def source_files(package_dir):
	items = [os.path.basename(package_dir)]
	for root, dir_names, file_names in os.walk(package_dir):
		items += [os.path.relpath(os.path.join(root, file_name), sublime.packages_path()).replace(os.sep, ".")[:-3] for file_name in file_names if file_name[-3:] == ".py"]
	return items