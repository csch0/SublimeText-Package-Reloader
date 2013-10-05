import sublime, sublime_plugin

import imp, os, sys

try:
	from .package_reloader import tools
except ValueError:
	from package_reloader import tools

class PackageReloaderListener(sublime_plugin.EventListener):

	def on_post_save(self, view):
		if not view.match_selector(0, "source.python"):
			return []
	
		# Extract Package Name
		package_name = os.path.relpath(view.file_name(), sublime.packages_path()).split(os.sep, 1)[0]
		package_dir = os.path.join(sublime.packages_path(), package_name)

		# Check for .build
		if os.path.isfile(os.path.join(package_dir, ".build")):

			try:
				file_json = tools.decode_value(tools.load_resource("Packages/%s/.build" % package_name))

				# Check for empty .build
				if not file_json:
					file_json = {"automatic_order": True, "iterations": 1, "mods_load_order": []}

				# Checkf if .build is valid
				elif any([item not in file_json for item in ["automatic_order", "iterations", "mods_load_order"]]):
					raise IOError

			except (OSError, IOError, ValueError) as e:
				logger.warning("Invalid .build format")
				return

			# Add source files, this is basically to check for new files and add them to the build
			items = [item for item in file_json["mods_load_order"] if os.path.isfile(os.path.join(package_dir, item.replace("/", os.sep)))]

			for item in tools.source_files(package_dir):
				if item not in items:
					items += [item]

			# Write load order back to file_json
			if file_json["automatic_order"]:
				items = sorted(items, reverse = True)

			file_json["mods_load_order"] = items

			# Save resource
			tools.save_resource("Packages/%s/.build" % package_name, tools.encode_value(file_json, True))

			# Wait fot the current file to reload
			sublime.set_timeout(lambda: sublime.run_command("package_reloader", {"package_name": package_name, "source": os.path.relpath(view.file_name(), package_dir), "items": items}), 500)

class PackageReloaderCommand(sublime_plugin.ApplicationCommand):

	def run(self, package_name, source, items):

		# Reload current file first if not in root dir
		if os.path.dirname(source):
			if sublime.version()[0] == "3":
				modulename = package_name + "." + (source.replace(os.sep, ".")[:-3] if source[-11:] != "__init__.py" else source.replace(os.sep, ".")[:-12])
			else:
				modulename = os.path.join(package_dir, source)

			print(modulename)

			# # Remove callbacks from subdirs before reloading the whole plugin
			for key, value in sublime_plugin.all_callbacks.items():
				for item in value:
					if item.__module__ == modulename:
						sublime_plugin.all_callbacks[key].remove(item)
			
			# Reload callbacks for file
			sublime_plugin.reload_plugin(modulename)
		
		print("Package Reloader - Reloading %s" % package_name)
		
		# Load modules
		for item in items:
			if sublime.version()[0] == "3":
				modulename = package_name + "." + (item.replace("/", ".")[:-3] if item[-11:] != "__init__.py" else item.replace("/", ".")[:-12])
			else:
				modulename = os.path.join(package_dir, item)
			
			# Reload module
			if modulename in sys.modules:
				print("reloading plugin", modulename)
				module = sys.modules[modulename]
				imp.reload(module)
			else:
				sublime_plugin.reload_plugin(modulename)
