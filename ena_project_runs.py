import requests
import sys
import xml.etree.ElementTree as ET
import re
import csv
import argparse

def get_all_runs(project_accession):
    """
    Given an ENA project accession
    return a CSV with the run accessions and their
    correspondint submitters Id.
    """
    print(f"Getting run accessions from {project_accession}...")
    project_tree = get_xml(project_accession)
    runs_url = get_url_submitted_files(project_tree)
    runs_list =  get_runs_in_table(runs_url)
    accessions = {}
    accessions["project"] = project_accession
    accessions["runs"] = {}
    print("Getting submitters Ids from run accessions...")
    for run_accession in runs_list:
        submitters_id = get_submitters_id(run_accession)
        accessions["runs"][run_accession] = submitters_id
    save_to_csv(accessions)
    print(f"Find results in {project_accession}_accessions.csv")
    print("End.")

def get_xml(accession):
    """
    Return an XML tree object
    for a given ENA accession.
    """
    base_url = "https://www.ebi.ac.uk/ena/browser/api/xml/"
    response = requests.get(f"{base_url}{accession}")
    assert response.status_code == 200, f"[ERROR]: Unable to access {base_url}{accession}"
    return ET.fromstring(response.text)

def get_url_submitted_files(project_tree):
    """
    Return an URL pointing to a table with 
    all the ENA run accessions and raw reads files submitted
    in a project.
    """
    link_list = project_tree.find("PROJECT").findall("PROJECT_LINKS/PROJECT_LINK")
    for item in link_list:
        db = item.find("XREF_LINK/DB").text
        if db == "ENA-SUBMITTED-FILES":
            return item.find("XREF_LINK/ID").text

def get_runs_in_table(url):
    response = requests.get(f"{url}")
    assert response.status_code == 200, f"[ERROR]: Unable to access {url}"
    raw_data = response.content.decode("utf/8")
    # delete first line with headers
    raw_data = re.sub(r"^.*\n", "", raw_data)
    return re.split("\t\t\t\t\n", raw_data.strip())

def get_submitters_id(run_accession):
    run_tree = get_xml(run_accession)
    return run_tree.find("RUN/EXPERIMENT_REF/IDENTIFIERS/SUBMITTER_ID").text

def save_to_csv(accessions):
    project = accessions["project"]
    headers = ["run_accession", "submitters_id"]
    with open(f"{project}_accessions.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for data in accessions["runs"].items():
            writer.writerow(data)
        f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = "Get INSDC run accessions and submitters Ids given a project accession", usage = "python3 ena_project_runs.py -p <project accession>")
    parser.add_argument("-p", "--project", type=str,  help = "INSDC project accession (e.g. PRJNA693894")
    args = parser.parse_args()
    get_all_runs(args.project)


