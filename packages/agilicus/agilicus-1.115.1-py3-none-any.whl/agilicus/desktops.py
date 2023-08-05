from . import context
from agilicus.agilicus_api import (
    DesktopResource,
    DesktopResourceSpec,
)

from .input_helpers import build_updated_model
from .input_helpers import get_org_from_input_or_ctx
from .input_helpers import strip_none
from .output.table import (
    spec_column,
    format_table,
    metadata_column,
)


def list_desktop_resources(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    print(kwargs)
    params = strip_none(kwargs)
    print(params)
    query_results = apiclient.app_services_api.list_desktop_resources(**params)
    return query_results.desktop_resources


def add_desktop_resource(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    spec = DesktopResourceSpec(**strip_none(kwargs))
    model = DesktopResource(spec=spec)
    return apiclient.app_services_api.create_desktop_resource(model).to_dict()


def _get_desktop_resource(ctx, apiclient, resource_id, **kwargs):
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.app_services_api.get_desktop_resource(resource_id, **kwargs)


def show_desktop_resource(ctx, resource_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return _get_desktop_resource(ctx, apiclient, resource_id, **kwargs).to_dict()


def delete_desktop_resource(ctx, resource_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.app_services_api.delete_desktop_resource(resource_id, **kwargs)


def update_desktop_resource(ctx, resource_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    get_args = {}
    get_args["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    mapping = _get_desktop_resource(ctx, apiclient, resource_id, **get_args)

    mapping.spec = build_updated_model(DesktopResourceSpec, mapping.spec, kwargs)
    return apiclient.app_services_api.replace_desktop_resource(
        resource_id, desktop_resource=mapping
    ).to_dict()


def format_desktops_as_text(ctx, resources):
    columns = [
        metadata_column("id"),
        spec_column("org_id"),
        spec_column("name"),
        spec_column("address"),
        spec_column("desktop_type"),
        spec_column("connector_id"),
    ]

    return format_table(ctx, resources, columns)
