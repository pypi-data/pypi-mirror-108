from simple_ddl_parser import DDLParser

ddl = """
CREATE TYPE my_status AS enum (
    'NEW',
    'IN_PROGRESS',
    'FINISHED'
);

CREATE TABLE foo
(
    entity_id        UUID PRIMARY KEY DEFAULT getId(),
    status           my_status
);
"""
result = DDLParser(ddl).run(group_by_type=True)

print(result)
