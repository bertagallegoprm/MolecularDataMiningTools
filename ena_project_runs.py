"""
Input: ENA project accession
Output: a CSV with the project accession as a name and two columns: 
    the ENA Run Id and the submitters Id.
    get_all_runs(project accession)
        project_tree = get_xml(project_accession)
        project_runs = get_runs_in_project(project_tree)
        project_runs_and_submitter_ids = get_submitters_id(project_runs)
        save_to_csv(project_runs_and_submitter_ids)

    -------

    get_xml(string: project_accession): xml tree object
    {Uses the ENA API to request an xml with the project data}

    get_runs_in_project(xml tree: project_tree): dictionary 
        runs_url = get_submitted_files(project_tree)
        return get_runs_in_table(runs_url)

    get_submitters_id(inout dictionaty: project_runs): dictionary
        for run in project_runs:
            submitter_id = get_submitter_id(run)
            add_submitter_id(submitter_id)
        return project_runs
    
    save_to_csv(dictionary: project_runs_and_submitters_ids)
        {Save dictionary to CSV}

    -------

    get_submitted_files(xml tree object: project_tree): string
    {Get URL with the run accessions and file names in the project}

    get_runs_in_table(runs_url): dictionary
    {Parse the first column "run_accession" in txt
    and create a dictionary
    {project_accession: {ena_run_1, 
                         ena_run_2, 
                         ..., 
                         ena_run_n}
    }}

"""

def get_xml(accession):
    """
    Return an XML tree object
    for a given ENA accession.
    """
    base_url = "https://www.ebi.ac.uk/ena/browser/api/xml/"
    response = requests.get(f"{base_url}{accession}")
    assert response.status_code == 200, f"[ERROR]: Unable to access experiment data in {base_url}{accession}"
    return ET.fromstring(response.text)
