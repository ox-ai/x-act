from pathlib import Path
from oxdb.core import Oxdb

from xact.compose.types import CodeSchema

CUSTOM_CODE_PLUGIN = Path.home() / "ox-xact" / "plugin.xact"
CODE_INDEX = Path.home() / "ox-xact" / "xact.oxdb"

CUSTOM_CODE_PLUGIN.mkdir(parents=True, exist_ok=True)
CODE_INDEX.mkdir(parents=True, exist_ok=True)


db = Oxdb(db_path=CODE_INDEX)
db.clean_up(db_path=db.db_path)
db.get_doc("index-xact")



class xcomposer:

    def schema():
        pass

    def compose(schema_map: CodeSchema = None, schema_map_path=None):
        if schema_map:
            hid = db.doc.push(
                data=schema_map.description,
                uid=schema_map.code,
                description=schema_map.model_dump(),
            )
        elif schema_map_path:
            pass

        return hid

    def search(order):
        res = db.doc.search(query=order, topn=1)

        schema_map = res["description"]
        return schema_map

    def add():
        pass

    def delete():
        pass

    def build():
        pass

    def test():
        pass

    def codes():
        pass
