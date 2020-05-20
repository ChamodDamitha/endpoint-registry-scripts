from EndpointRegUtil import EndpointRegUtil

# Retrieve all registries
registries = EndpointRegUtil.getRegistries()
for reg in registries:
    # Delete the registry
    EndpointRegUtil.deleteRegistry(reg["id"])
print("Cleaned the registry")
