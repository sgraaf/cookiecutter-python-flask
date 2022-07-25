import json
import os
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Optional

from {{ cookiecutter.package_name }} import models
from {{ cookiecutter.package_name }}.database import Model

# see: https://github.com/nickjj/flask-db/issues/7#issuecomment-893874287
DB_DIR = Path(os.environ["PYTHONPATH"]).resolve() / "db"
FIXTURES_DIR = DB_DIR / "fixtures"


def create_record(model: Model, fixture: Dict[str, Any]) -> Optional[Model]:
    global models
    global date
    global datetime

    for k, v in list(fixture.items()):
        if hasattr(models, k):  # update relationships
            del fixture[k]
            fixture[k.lower()] = getattr(models, k).query.filter_by(name=v).first()
        elif k.endswith("_at"):  # update date(time)
            if v:
                if "T" in v:
                    fixture[k] = datetime.fromisoformat(v)
                else:
                    fixture[k] = date.fromisoformat(v)

    if (
        model.query.filter_by(
            **{k: v for k, v in fixture.items() if k != "password"}
        ).first()
        is None
    ):
        return model.create(**fixture)
    return None


for fixture_file in FIXTURES_DIR.glob("*.json"):
    # get the appropriate model
    model = getattr(models, fixture_file.stem.split("_")[1])

    # load the fixture(s)
    with open(fixture_file, encoding="utf-8") as fh:
        fixture_or_fixtures = json.load(fh)

        if isinstance(fixture_or_fixtures, list):  # multiple fixtures
            for fixture in fixture_or_fixtures:
                try:
                    create_record(model, fixture)
                except Exception as e:
                    print(e)
                    pass
        elif isinstance(fixture_or_fixtures, dict):  # single fixture
            create_record(model, fixture_or_fixtures)
