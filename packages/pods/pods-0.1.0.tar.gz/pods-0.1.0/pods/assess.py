import os


DATAPATH = os.path.expanduser(os.path.expandvars(config.get("datasets", "dir")))

def data_available(dataset_name=None):
    """Check if the data set is available on the local machine already."""
    dr = data_resources[dataset_name]
    if "dirs" in dr:
        for dirs, files in zip(dr["dirs"], dr["files"]):
            for dir, file in zip(dirs, files):
                if not os.path.exists(os.path.join(data_path, dataset_name, dir, file)):
                    return False
    else:
        for file_list in dr["files"]:
            for file in file_list:
                if not os.path.exists(os.path.join(data_path, dataset_name, file)):
                    return False
    return True


def pmlr_proceedings_list(data_set):
    proceedings_file = open(os.path.join(data_path, data_set, "proceedings.yaml"), "r")
    proceedings = yaml.load(proceedings_file, Loader=yaml.FullLoader)

def pmlr(data_set, refresh_data):
    """Download the yaml files for current PMLR proceedings."""
    if not access.data_available(data_set) and not refresh_data:
        download_data(data_set)


    # Create a new resources entry for downloading contents of proceedings.
    data_name_full_stub = "pmlr_volume_"
    for entry in proceedings:
        data_name_full = data_name_full_stub + "v" + str(entry["volume"])
        data_resources[data_name_full] = data_resources[data_set].copy()
        data_resources[data_name_full]["files"] = []
        data_resources[data_name_full]["dirs"] = []
        data_resources[data_name_full]["urls"] = []
        if volumes == "all" or entry["volume"] in volumes:
            file = entry["yaml"].split("/")[-1]
            proto, url = entry["yaml"].split("//")
            file = os.path.basename(url)
            dirname = os.path.dirname("/".join(url.split("/")[1:]))
            urln = proto + "//" + url.split("/")[0]
            data_resources[data_name_full]["files"].append([file])
            data_resources[data_name_full]["dirs"].append([dirname])
            data_resources[data_name_full]["urls"].append(urln)
        Y = []
        # Download the volume data
        if not access.data_available(data_name_full):
            download_data(data_name_full)
