from horizon import tabs

from openstack_dashboard.dashboards.goldstone.logs \
    import tabs as logs_tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = logs_tabs.LogsTabs
    template_name = 'goldstone/logs/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context
