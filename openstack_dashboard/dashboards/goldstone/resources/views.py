from horizon import tabs

from openstack_dashboard.dashboards.goldstone.resources \
    import tabs as resources_tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = resources_tabs.ResourcesTabs
    template_name = 'goldstone/resources/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context