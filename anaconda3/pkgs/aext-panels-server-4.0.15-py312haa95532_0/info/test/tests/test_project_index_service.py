from aext_panels_server.services.project_index import project_index_service


async def test_get_project_info_file():
    project_index_path = project_index_service.get_project_index_file_path()
    assert project_index_path == ".projects/index.json"

    project_index_path = project_index_service.get_project_index_file_path(include_root_path=True)

    assert project_index_path == "/var/www/panels/.projects/index.json"
