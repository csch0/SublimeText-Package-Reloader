import sublime, sublime_plugin

import imp, sys, os

try:
	from .package_reloader.tools import load_resource, save_resource, decode_value, encode_value, source_files
except ValueError:
	from package_reloader.tools import load_resource, save_resource, decode_value, encode_value, source_files

class PackageReloaderListener(sublime_plugin.EventListener):

	def on_post_save(self, view):
		if not view.match_selector(0, "source.python"):
			return []

		sublime.set_timeout(lambda: self.__on_post_save(view), 500)

	def __on_post_save(self, view):

		# Extract Package Name
		package_name = os.path.relpath(view.file_name(), sublime.packages_path()).split(os.sep, 1)[0]
		package_dir = os.path.join(sublime.packages_path(), package_name)

		# Check for .build
		if os.path.isfile(os.path.join(package_dir, ".build")):

			try:
				file_json = decode_value(load_resource("Packages/%s/.build" % package_name))

				# Check for empty .build
				if not file_json:
					file_json = {"automatic_order": True, "iterations": 1, "mods_load_order": []}

				# Checkf if .build is valid
				elif any([item not in file_json for item in ["automatic_order", "iterations", "mods_load_order"]]):
					raise IOError

			except (OSError, IOError, ValueError):
				print("Invalid .build format")
				return

			# Add source files, this is basically to check for new files and add them to the build
			items = [item for item in file_json["mods_load_order"] if os.path.isfile(os.path.join(package_dir, item.replace("/", os.sep)))]

			for item in source_files(package_dir):
				if item not in items:
					items += [item]

			# Write load order back to file_json
			if file_json["automatic_order"]:
				items = sorted(items, reverse = False)

			file_json["mods_load_order"] = items

			# Save resource
			save_resource("Packages/%s/.build" % package_name, encode_value(file_json, True))

			# change working dictionary to reload modules
			cwd = os.getcwd()
			os.chdir(package_dir)

			# Prefix is just required on ST3
			prefix = package_name + "." if sublime.version()[0] == "3" else ""

			# Reload current saved module first
			item = os.path.relpath(view.file_name(), package_dir)
			mod_name = prefix + item.replace(os.sep, ".")[:-3]
			if os.path.dirname(item) and mod_name and mod_name in sys.modules and sys.modules[mod_name]:
				print ("reloading plugin", mod_name)
				imp.reload(sys.modules[mod_name])

			# perform multiple iterations if requested
			for i in range(file_json["iterations"]):

				# Load modules
				for item in file_json["mods_load_order"]:
					mod_name = prefix + (item.replace("/", ".")[:-3] if item[-11:] != "__init__.py" else item.replace("/", ".")[:-12])

					# Check of mod_name available and not none
					if mod_name in sys.modules and sys.modules[mod_name]:
						print ("reloading plugin", mod_name)
						imp.reload(sys.modules[mod_name])

			# Change working dictionary back
			os.chdir(cwd)
