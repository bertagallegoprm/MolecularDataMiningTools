"""
Input: ENA project accession
Output: a CSV with the project accession as a name and two columns: 
    the ENA Run Id and the submitters Id.
    get_all_runs(project accession):
        project_tree = get_project_xml(project_accession)
        project_runs = get_runs_in_project(project_tree)
        project_runs_and_submitter_ids = get_submitters_id(project_runs)
        save_to_csv(project_runs_and_submitter_ids)
   
"""
