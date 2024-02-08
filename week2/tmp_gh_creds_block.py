from prefect.filesystems import GitHub

block = GitHub(
    repository="https://github.com/pablosr11/data-engineering-camp",
)
# block.get_directory("folder-in-repo") # specify a subfolder of repo
block.save("gh-block")
