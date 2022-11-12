import django.db.models.base
import django.db.models.options
from django.db.models.options import Options as DjangoOptions

DEFAULT_SCYLLA_NAMES = (
    "comment",
    "read_repair_chance",
    "dclocal_read_repair_chance",
    "speculative_retry",
    "gc_grace_seconds",
    "tombstone_gc",
    "bloom_filter_fp_chance",
    "default_time_to_live",
    "compaction",
    "compression",
    "caching",
    "cdc",
)


class Options(DjangoOptions):
    def __init__(self, *args, **kwargs):
        """Add ScyllaDB table options from here: # https://docs.scylladb.com/stable/cql/ddl.html#other-table-options"""
        super().__init__(*args, **kwargs)
        for key in DEFAULT_SCYLLA_NAMES:
            setattr(self, key, None)


# monkey patch Options
django.db.models.base.Options = Options
django.db.models.options.DEFAULT_NAMES = tuple(
    list(django.db.models.options.DEFAULT_NAMES) + list(DEFAULT_SCYLLA_NAMES)
)
