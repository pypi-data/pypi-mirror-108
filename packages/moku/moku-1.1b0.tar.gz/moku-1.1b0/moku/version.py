import pkg_resources as pkr

# List of compatible firmware builds
compat_fw = [542]

# Official release name
release = pkr.get_distribution("moku").version
