import brozzler
import doublethink
import pytest

from brozzleradmin.database import DataBaseAccess


@pytest.fixture(scope="module")
def database():
    return DataBaseAccess()


def test_add_page_to_site(database):
    rr = doublethink.Rethinker(servers=['localhost:28015'], db='brozzler')
    frontier = brozzler.RethinkDbFrontier(rr)

    job_conf = {'seeds': [
        {'url': 'https://example.org'}]
    }

    job = brozzler.new_job(frontier, job_conf)
    sites = sorted(list(frontier.job_sites(job.id)), key=lambda x: x.seed)

    url = "http://example.org/new_page"
    page = database.add_page_to_site(siteid=sites[0].id, url=url)
    result = list(rr.table('pages').filter({"id": page.id}).run())
    assert len(result) == 1


def test_get_site(database):
    rr = doublethink.Rethinker(servers=['localhost:28015'], db='brozzler')
    frontier = brozzler.RethinkDbFrontier(rr)
    job = sorted(list(frontier.active_jobs()), key=lambda x: x.id)[0]

    site = database.get_site(job.id, 'https://example.org')
    assert site